import pytest
import serial
from packaging.version import Version

from config import SSID
from lib import ensure_wifi_connected, has_active_wifi_connection, read_firmware, wait_for_condition


@pytest.mark.regression
@pytest.mark.positive
def test_ota_pending_verify_to_valid(connected_device):
  device = connected_device

  original_version, original_partition, original_state = read_firmware(device)

  assert original_state.lower() == 'valid'

  available = (Version('1.3.0'), Version('1.4.0'), Version('1.5.0'))
  newer = [version for version in available if version > original_version]

  if not newer:
    pytest.skip(f'No newer firmware available for {original_version}')

  target_version = newer[0]
  expected_partition = 'ota_1' if original_partition == 'ota_0' else 'ota_0'

  try:
    ensure_wifi_connected(device)

    response = device.ota.install(str(target_version))
    output = '\n'.join(response)

    assert '[OTA] success:' in output, f'OTA installation failed: {response}'

    boot_logs = device.wait_for_log(
      "ready. Type 'help' for commands",
      timeout=60,
    )

    boot_output = '\n'.join(boot_logs)

    pending_log = '[OTA] new firmware, state PENDING_VERIFY - running self-check...'
    valid_log = '[OTA] self-check passed, firmware marked VALID'

    assert pending_log in boot_output, f'PENDING_VERIFY transition missing: {boot_logs}'

    assert valid_log in boot_output, f'VALID transition missing: {boot_logs}'

    assert boot_output.index(pending_log) < boot_output.index(valid_log), (
      'Firmware was marked VALID before entering PENDING_VERIFY'
    )

    installed_version, installed_partition, installed_state = read_firmware(device)

    assert installed_version == target_version
    assert installed_partition == expected_partition
    assert installed_state.lower() == 'valid'

  finally:
    current_version, _, _ = read_firmware(device)

    if current_version != original_version:
      ensure_wifi_connected(device)

      response = device.ota.install(str(original_version), force=True)

      assert '[OTA] success:' in '\n'.join(response), f'Firmware restore failed: {response}'

      device.wait_for_log("ready. Type 'help' for commands", timeout=60)

      restored_version, _, restored_state = read_firmware(device)

      assert restored_version == original_version
      assert restored_state.lower() == 'valid'


@pytest.mark.regression
@pytest.mark.negative
def test_ota_rollback_broken_image(connected_device):
  device = connected_device

  original_version, original_partition, original_state = read_firmware(device)
  original_lamp = device.lamp.status()

  assert original_state.lower() == 'valid'

  expected_rgb = (12, 34, 56)
  expected_brightness = 37
  expected_mode = 'breathe'

  scenes = [
    (1, (255, 0, 0), 25, 'solid'),
    (2, (0, 255, 0), 50, 'blink'),
    (3, (0, 0, 255), 75, 'breathe'),
  ]

  try:
    ensure_wifi_connected(device)

    device.lamp.set_rgb(*expected_rgb)
    device.lamp.set_brightness(expected_brightness)
    device.lamp.set_mode(expected_mode)

    status = device.lamp.status()

    assert status.color == expected_rgb
    assert status.brightness == expected_brightness
    assert status.mode == expected_mode

    if original_version >= Version('1.5.0'):
      for scene, rgb, brightness, mode in scenes:
        device.lamp.set_rgb(*rgb)
        device.lamp.set_brightness(brightness)
        device.lamp.set_mode(mode)
        device.lamp.save_scene(scene)

      device.lamp.set_rgb(*expected_rgb)
      device.lamp.set_brightness(expected_brightness)
      device.lamp.set_mode(expected_mode)

    device._connector.write_command('ota broken')

    response = device.wait_for_log(
      'rolling back to previous firmware...',
      timeout=120,
    )

    output = '\n'.join(response)

    assert 'self-check FAILED' in output, (
      f'Firmware self-check failure was not detected: {response}'
    )

    assert 'rolling back to previous firmware...' in output, (
      f'Automatic rollback was not detected: {response}'
    )

    device.wait_for_log("ready. Type 'help' for commands", timeout=60)

    current_version, current_partition, current_state = read_firmware(device)

    assert current_version == original_version
    assert current_partition == original_partition
    assert current_state.lower() == 'valid'

    status = device.lamp.status()

    assert status.color == expected_rgb
    assert status.brightness == expected_brightness
    assert status.mode == expected_mode

    if has_active_wifi_connection(device):
      assert device.wifi.disconnect(), 'Failed to disconnect Wi-Fi'

    result = device.wifi.connect()

    assert result.connected, f'Saved Wi-Fi credentials were not restored: {result.response}'

    assert device.wifi.status().ssid == SSID

    if original_version >= Version('1.5.0'):
      for scene, rgb, brightness, mode in scenes:
        device.lamp.set_rgb(1, 2, 3)
        device.lamp.set_brightness(10)
        device.lamp.set_mode('solid')

        response = device.lamp.load_scene(scene)
        status = device.lamp.status()

        assert any(f'[LAMP] scene {scene} loaded' in line for line in response), (
          f'Scene {scene} was not restored: {response}'
        )

        assert status.color == rgb
        assert status.brightness == brightness
        assert status.mode == mode

  finally:
    device.lamp.set_rgb(*original_lamp.color)
    device.lamp.set_brightness(original_lamp.brightness)
    device.lamp.set_mode(original_lamp.mode)

    if original_lamp.is_on:
      device.lamp.on()
    else:
      device.lamp.off()


@pytest.mark.regression
@pytest.mark.negative
def test_ota_reset_during_pending_verify(connected_device, hil):
  device = connected_device
  connector = device._connector

  original_version, original_partition, original_state = read_firmware(device)

  assert original_state.lower() == 'valid'

  available = (Version('1.3.0'), Version('1.4.0'), Version('1.5.0'))
  newer = [version for version in available if version > original_version]

  if not newer:
    pytest.skip(f'No newer firmware available for {original_version}')

  target_version = newer[0]

  def reconnect_uart():
    try:
      connector.open()
      return True
    except (serial.SerialException, OSError):
      connector.close()
      return False

  try:
    ensure_wifi_connected(device)

    response = device.ota.install(str(target_version))

    assert '[OTA] success:' in '\n'.join(response), f'OTA installation failed: {response}'

    response = device.wait_for_log(
      '[OTA] new firmware, state PENDING_VERIFY - running self-check...',
      timeout=60,
    )

    assert any('PENDING_VERIFY' in line for line in response), (
      f'PENDING_VERIFY was not detected: {response}'
    )

    connector.close()

    try:
      power_response = hil.power_cycle()

      assert any('[HIL] DUT power: OFF' in line for line in power_response), (
        f'DUT power OFF was not confirmed: {power_response}'
      )

      assert any('[HIL] DUT power: ON' in line for line in power_response), (
        f'DUT power ON was not confirmed: {power_response}'
      )

    finally:
      wait_for_condition(
        reconnect_uart,
        timeout=30,
        interval=0.5,
        error_message='DUT UART did not recover after power cycle.',
      )

    device.wait_for_log(
      "ready. Type 'help' for commands",
      timeout=60,
    )

    current_version, current_partition, current_state = read_firmware(device)

    assert current_version == original_version, (
      f'Expected rollback to {original_version}, got {current_version}'
    )

    assert current_partition == original_partition, (
      f'Expected rollback to {original_partition}, got {current_partition}'
    )

    assert current_state.lower() == 'valid'

  finally:
    if connector.ser is not None and connector.ser.is_open:
      current_version, _, _ = read_firmware(device)

      if current_version != original_version:
        ensure_wifi_connected(device)

        response = device.ota.install(str(original_version), force=True)

        assert '[OTA] success:' in '\n'.join(response), (
          f'Failed to restore original firmware: {response}'
        )

        device.wait_for_log(
          "ready. Type 'help' for commands",
          timeout=60,
        )
