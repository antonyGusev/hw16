import re

import pytest

from config import PASSWORD, SSID
from lib import ensure_wifi_connected, has_active_wifi_connection, read_firmware


@pytest.mark.regression
@pytest.mark.positive
def test_ota_preserves_wifi_and_lamp_settings(ota_connected_device, hil, ota_versions):
  device = ota_connected_device

  original_version, _, original_state = read_firmware(device)
  original_lamp = device.lamp.status()

  assert original_state.lower() == 'valid'
  assert has_active_wifi_connection(device)

  available = sorted(set(ota_versions.values()))
  newer = [version for version in available if version > original_version]

  if not newer:
    pytest.skip(f'No newer firmware available for {original_version}')

  target_version = newer[0]

  expected_rgb = (12, 34, 56)
  expected_brightness = 37
  expected_mode = 'breathe'

  try:
    device.lamp.set_rgb(*expected_rgb)
    device.lamp.set_brightness(expected_brightness)
    device.lamp.set_mode(expected_mode)

    before = device.lamp.status()

    assert before.color == expected_rgb
    assert before.brightness == expected_brightness
    assert before.mode == expected_mode

    response = device.ota.install(str(target_version))
    output = '\n'.join(response)

    assert '[OTA] success:' in output, f'OTA upgrade failed: {response}'

    device.wait_for_log("ready. Type 'help' for commands", timeout=60)

    updated_version, _, updated_state = read_firmware(device)

    assert updated_version == target_version
    assert updated_state.lower() == 'valid'

    after = device.lamp.status()

    assert after.color == expected_rgb
    assert after.brightness == expected_brightness
    assert after.mode == expected_mode

    if has_active_wifi_connection(device):
      assert device.wifi.disconnect(), 'Failed to disconnect Wi-Fi'

    result = device.wifi.connect()

    assert result.connected, f'Failed to reconnect using saved credentials: {result.response}'

    wifi_status = device.wifi.status()

    assert has_active_wifi_connection(device)
    assert wifi_status.ssid == SSID

    device.lamp.on()

    hil.camera.photo.verify(
      'rgb',
      name='persisted_color_after_ota',
      expected_rgb=expected_rgb,
    )

    hil.camera.video.verify(
      'breathe',
      name='persisted_breathe_after_ota',
    )

  finally:
    current_version, _, _ = read_firmware(device)

    if current_version != original_version:
      if not has_active_wifi_connection(device):
        result = device.wifi.connect(SSID, PASSWORD)
        assert result.connected, f'Failed to restore Wi-Fi connection: {result.response}'

      response = device.ota.install(str(original_version), force=True)

      assert '[OTA] success:' in '\n'.join(response), f'Firmware restore failed: {response}'

      device.wait_for_log("ready. Type 'help' for commands", timeout=60)

      restored_version, _, restored_state = read_firmware(device)

      assert restored_version == original_version
      assert restored_state.lower() == 'valid'

    device.lamp.off()
    device.lamp.set_rgb(*original_lamp.color)
    device.lamp.set_brightness(original_lamp.brightness)
    device.lamp.set_mode(original_lamp.mode)

    if original_lamp.is_on:
      device.lamp.on()


@pytest.mark.fw_min('1.4.0')
@pytest.mark.regression
@pytest.mark.positive
def test_ota_preserves_settings_after_force_downgrade(ota_connected_device, ota_versions):
  device = ota_connected_device

  original_version, _, original_state = read_firmware(device)
  original_lamp = device.lamp.status()

  assert original_state.lower() == 'valid'
  assert has_active_wifi_connection(device)

  available = sorted(set(ota_versions.values()))
  older = [version for version in available if version < original_version]

  if not older:
    pytest.skip(f'No older firmware available for {original_version}')

  target_version = older[-1]

  expected_rgb = (12, 34, 56)
  expected_brightness = 37
  expected_mode = 'breathe'

  try:
    device.lamp.set_rgb(*expected_rgb)
    device.lamp.set_brightness(expected_brightness)
    device.lamp.set_mode(expected_mode)

    before = device.lamp.status()

    assert before.color == expected_rgb
    assert before.brightness == expected_brightness
    assert before.mode == expected_mode

    response = device.ota.install(str(target_version), force=True)
    output = '\n'.join(response)

    assert '[OTA] success:' in output, f'OTA downgrade failed: {response}'

    device.wait_for_log("ready. Type 'help' for commands", timeout=60)

    downgraded_version, _, downgraded_state = read_firmware(device)

    assert downgraded_version == target_version
    assert downgraded_state.lower() == 'valid'

    after = device.lamp.status()

    assert after.color == expected_rgb
    assert after.brightness == expected_brightness
    assert after.mode == expected_mode

    if has_active_wifi_connection(device):
      assert device.wifi.disconnect(), 'Failed to disconnect Wi-Fi'

    result = device.wifi.connect()

    assert result.connected, f'Failed to reconnect using saved credentials: {result.response}'

    wifi_status = device.wifi.status()

    assert has_active_wifi_connection(device)
    assert wifi_status.ssid == SSID

  finally:
    current_version, _, _ = read_firmware(device)

    if current_version != original_version:
      if not has_active_wifi_connection(device):
        result = device.wifi.connect()
        assert result.connected, f'Failed to restore Wi-Fi connection: {result.response}'

      response = device.ota.install(str(original_version), force=True)

      assert '[OTA] success:' in '\n'.join(response), f'Firmware restore failed: {response}'

      device.wait_for_log("ready. Type 'help' for commands", timeout=60)

      restored_version, _, restored_state = read_firmware(device)

      assert restored_version == original_version
      assert restored_state.lower() == 'valid'

    device.lamp.off()
    device.lamp.set_rgb(*original_lamp.color)
    device.lamp.set_brightness(original_lamp.brightness)
    device.lamp.set_mode(original_lamp.mode)

    if original_lamp.is_on:
      device.lamp.on()


@pytest.mark.fw_only('1.5.0')
@pytest.mark.regression
@pytest.mark.positive
def test_ota_preserves_scenes_after_reinstall(ota_connected_device):
  device = ota_connected_device

  original_version, original_partition, original_state = read_firmware(device)
  original_lamp = device.lamp.status()

  assert original_state.lower() == 'valid'

  scenes = [
    (1, (255, 0, 0), 25, 'solid'),
    (2, (0, 255, 0), 50, 'blink'),
    (3, (0, 0, 255), 75, 'breathe'),
  ]

  try:
    for scene, rgb, brightness, mode in scenes:
      device.lamp.set_rgb(*rgb)
      device.lamp.set_brightness(brightness)
      device.lamp.set_mode(mode)

      response = device.lamp.save_scene(scene)

      assert any(f'[LAMP] scene {scene} saved' in line for line in response), (
        f'Failed to save scene {scene}: {response}'
      )

    response = device.ota.install(str(original_version), force=True)
    output = '\n'.join(response)

    assert re.search(
      rf'\[OTA\] success:\s*{re.escape(str(original_version))}'
      rf'\s*->\s*{re.escape(str(original_version))}'
      rf'\s+in\s+\d+\s+s\. Rebooting\.\.\.',
      output,
    ), f'OTA reinstall failed: {response}'

    device.wait_for_log("ready. Type 'help' for commands", timeout=60)

    current_version, current_partition, current_state = read_firmware(device)

    assert current_version == original_version
    assert current_partition != original_partition
    assert current_state.lower() == 'valid'

    for scene, rgb, brightness, mode in scenes:
      device.lamp.set_rgb(1, 2, 3)
      device.lamp.set_brightness(10)
      device.lamp.set_mode('solid')

      response = device.lamp.load_scene(scene)
      status = device.lamp.status()

      assert any(f'[LAMP] scene {scene} loaded' in line for line in response), (
        f'Failed to load scene {scene} after OTA: {response}'
      )

      assert status.color == rgb, f'Scene {scene}: RGB mismatch'
      assert status.brightness == brightness, f'Scene {scene}: brightness mismatch'
      assert status.mode == mode, f'Scene {scene}: mode mismatch'

  finally:
    device.lamp.set_rgb(*original_lamp.color)
    device.lamp.set_brightness(original_lamp.brightness)
    device.lamp.set_mode(original_lamp.mode)

    if original_lamp.is_on:
      device.lamp.on()
    else:
      device.lamp.off()
