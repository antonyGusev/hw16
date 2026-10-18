import re

import pytest
import serial
from packaging.version import Version

from lib import (
  DeviceTimeoutError,
  ensure_wifi_connected,
  has_active_wifi_connection,
  read_firmware,
  wait_for_condition,
)


def recover_dut(device, hil):
  connector = device._connector
  connector.close()

  hil.power_cycle()

  def reconnect_uart():
    try:
      connector.open()
      return True
    except (serial.SerialException, OSError):
      return False

  wait_for_condition(
    reconnect_uart,
    timeout=30,
    interval=0.5,
    error_message='DUT UART did not recover after power cycle.',
  )

  def is_ready():
    try:
      return any('state:' in line for line in device.version())
    except DeviceTimeoutError:
      return False

  wait_for_condition(
    is_ready,
    timeout=30,
    interval=0.5,
    error_message='DUT did not respond after recovery.',
  )


@pytest.mark.regression
@pytest.mark.negative
def test_ota_interrupt_wifi_by_k3_button(ota_connected_device, hil):
  device = ota_connected_device
  original_version, original_partition, original_state = read_firmware(device)

  assert original_state.lower() == 'valid'

  available = (Version('1.3.0'), Version('1.4.0'), Version('1.5.0'))
  newer = [version for version in available if version > original_version]

  if not newer:
    pytest.skip(f'No firmware newer than {original_version} is available')

  target_version = newer[0]
  ensure_wifi_connected(device)

  try:
    try:
      response = device.ota.install(
        str(target_version),
        until=('[OTA] progress: 10%', '[OTA] error:', '[OTA] failed:'),
      )

      assert any('[OTA] progress: 10%' in line for line in response), (
        f'OTA did not reach 10%: {response}'
      )

      hil.buttons.k3()

      response = device.wait_for_log(
        '[OTA] failed: download interrupted (ESP_FAIL)',
        timeout=60,
      )

      assert any('[K3] wifi disconnect' in line for line in response), (
        f'Wi-Fi disconnect command was not confirmed: {response}'
      )
      assert any('wifi station: disconnected' in line for line in response), (
        f'Wi-Fi disconnection was not confirmed: {response}'
      )
      assert any('[OTA] failed: download interrupted (ESP_FAIL)' in line for line in response), (
        f'OTA interruption was not confirmed: {response}'
      )

      current_version, current_partition, state = read_firmware(device)

      assert current_version == original_version
      assert current_partition == original_partition
      assert state.lower() == 'valid'

    finally:
      if not has_active_wifi_connection(device):
        device.wifi.connect()
        wait_for_condition(
          lambda: has_active_wifi_connection(device),
          timeout=10,
          interval=0.5,
          error_message='Wi-Fi did not reconnect after K3.',
        )

    try:
      assert has_active_wifi_connection(device)

      response = device.ota.install(str(target_version))
      output = '\n'.join(response)

      assert re.search(
        rf'\[OTA\] success:\s*{re.escape(str(original_version))}'
        rf'\s*->\s*{re.escape(str(target_version))}'
        rf'\s+in\s+\d+\s+s\. Rebooting\.\.\.',
        output,
      ), f'OTA retry failed: {response}'

      device.wait_for_log("ready. Type 'help' for commands", timeout=60)

      updated_version, updated_partition, updated_state = read_firmware(device)

      assert updated_version == target_version
      assert updated_partition != original_partition
      assert updated_state.lower() == 'valid'

    finally:
      current_version, _, _ = read_firmware(device)

      if current_version != original_version:
        ensure_wifi_connected(device)

        response = device.ota.install(str(original_version), force=True)

        assert '[OTA] success:' in '\n'.join(response), (
          f'Failed to restore original firmware: {response}'
        )

        device.wait_for_log("ready. Type 'help' for commands", timeout=60)

        restored_version, _, restored_state = read_firmware(device)

        assert restored_version == original_version
        assert restored_state.lower() == 'valid'

  except AssertionError:
    recover_dut(device, hil)
    raise


@pytest.mark.regression
@pytest.mark.negative
def test_ota_interrupt_power(ota_connected_device, hil):
  device = ota_connected_device
  connector = device._connector

  try:
    original_version, original_partition, original_state = read_firmware(device)

    assert original_state.lower() == 'valid'

    response = device.ota.install(
      str(original_version),
      force=True,
      until=('[OTA] progress: 10%', '[OTA] error:', '[OTA] failed:'),
    )

    assert any('[OTA] progress: 10%' in line for line in response), (
      f'OTA did not reach 10%: {response}'
    )

    def reconnect_uart():
      try:
        connector.open()
        return True
      except (serial.SerialException, OSError):
        return False

    connector.close()

    try:
      response = hil.power_cycle()

      assert any('[HIL] DUT power: OFF' in line for line in response), (
        f'DUT power OFF was not confirmed: {response}'
      )
      assert any('[HIL] DUT power: ON' in line for line in response), (
        f'DUT power ON was not confirmed: {response}'
      )
    finally:
      wait_for_condition(
        reconnect_uart,
        timeout=30,
        interval=0.5,
        error_message='DUT UART did not recover after power cycle.',
      )

    current_version, current_partition, state = read_firmware(device)

    assert current_version == original_version
    assert current_partition == original_partition
    assert state.lower() == 'valid'

  except AssertionError:
    recover_dut(device, hil)
    raise
