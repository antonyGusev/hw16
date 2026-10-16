import re

import pytest
import serial

from lib import ensure_wifi_connected, has_active_wifi_connection, read_firmware, wait_for_condition


@pytest.mark.regression
@pytest.mark.negative
def test_ota_interrupt_wifi_by_k3_button(connected_device, hil):
  device = connected_device
  original_version, original_partition, original_state = read_firmware(device)

  assert original_state.lower() == 'valid'
  ensure_wifi_connected(device)

  try:
    response = device.ota.install(
      str(original_version),
      force=True,
      until='[OTA] progress: 10%',
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
      hil.buttons.k3()
      wait_for_condition(
        lambda: has_active_wifi_connection(device),
        timeout=10,
        interval=0.5,
        error_message='Wi-Fi did not reconnect after K3.',
      )

  assert has_active_wifi_connection(device)

  response = device.ota.install(str(original_version), force=True)
  output = '\n'.join(response)

  assert re.search(
    rf'\[OTA\] success:\s*{re.escape(str(original_version))}'
    rf'\s*->\s*{re.escape(str(original_version))}'
    rf'\s+in\s+\d+\s+s\. Rebooting\.\.\.',
    output,
  ), f'OTA retry failed: {response}'

  device.wait_for_log("ready. Type 'help' for commands", timeout=60)

  restored_version, restored_partition, restored_state = read_firmware(device)

  assert restored_version == original_version
  assert restored_partition != original_partition
  assert restored_state.lower() == 'valid'


@pytest.mark.regression
@pytest.mark.negative
def test_ota_interrupt_power(connected_device, hil):
  device = connected_device
  connector = device._connector

  original_version, original_partition, original_state = read_firmware(device)

  assert original_state.lower() == 'valid'

  response = device.ota.install(
    str(original_version),
    force=True,
    until='[OTA] progress: 10%',
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
