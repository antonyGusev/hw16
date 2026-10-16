import re

import pytest
from packaging.version import Version

from lib import ensure_wifi_connected, read_firmware


def restore_firmware(device, original_version):
  current_version, _, _ = read_firmware(device)

  if current_version == original_version:
    return

  ensure_wifi_connected(device)

  response = device.ota.install(str(original_version), force=True)
  output = '\n'.join(response)

  assert '[OTA] success:' in output, f'Firmware restore failed: {response}'

  device.wait_for_log("ready. Type 'help' for commands", timeout=60)

  restored_version, _, state = read_firmware(device)

  assert restored_version == original_version
  assert state.lower() == 'valid'


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.parametrize('channel', ['stable', 'beta'])
def test_ota_update(connected_device, channel):
  device = connected_device

  original_version, original_partition, original_state = read_firmware(device)

  assert original_state.lower() == 'valid'

  check = '\n'.join(device.ota.check())
  target = re.search(
    rf'\[OTA\] {channel} channel:\s*(\d+\.\d+\.\d+)',
    check,
  )

  assert target is not None, f'{channel} version missing: {check}'

  target_version = Version(target.group(1))

  if original_version >= target_version:
    pytest.skip(f'{channel} update requires firmware older than {target_version}')

  try:
    ensure_wifi_connected(device)

    response = device.ota.update(beta=(channel == 'beta'))
    output = '\n'.join(response)

    assert re.search(
      rf'\[OTA\] success:\s*{re.escape(str(original_version))}'
      rf'\s*->\s*{re.escape(str(target_version))}'
      rf'\s+in\s+\d+\s+s\. Rebooting\.\.\.',
      output,
    ), f'OTA {channel} update failed: {response}'

    device.wait_for_log("ready. Type 'help' for commands", timeout=60)

    updated_version, updated_partition, state = read_firmware(device)

    assert updated_version == target_version
    assert updated_partition != original_partition
    assert state.lower() == 'valid'

  finally:
    restore_firmware(device, original_version)


@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.parametrize('channel', ['stable', 'beta'])
def test_ota_update_when_already_current(connected_device, channel):
  device = connected_device
  original_version, _, original_state = read_firmware(device)
  assert original_state.lower() == 'valid'

  check = '\n'.join(device.ota.check())
  target = re.search(rf'\[OTA\] {channel} channel:\s*(\d+\.\d+\.\d+)', check)
  assert target is not None, f'{channel} channel version missing: {check}'
  target_version = Version(target.group(1))

  try:
    if original_version != target_version:
      ensure_wifi_connected(device)
      response = device.ota.install(str(target_version), force=True)
      assert '[OTA] success:' in '\n'.join(response), f'Setup install failed: {response}'
      device.wait_for_log("ready. Type 'help' for commands", timeout=60)

    current_version, current_partition, state = read_firmware(device)
    assert current_version == target_version
    assert state.lower() == 'valid'
    ensure_wifi_connected(device)

    response = device.ota.update(beta=(channel == 'beta'))
    output = '\n'.join(response)
    assert '[OTA] already up to date' in output, f'Unexpected {channel} response: {response}'
    assert '[OTA] downloading:' not in output
    assert '[OTA] success:' not in output
    assert 'Rebooting...' not in output

    updated_version, updated_partition, updated_state = read_firmware(device)
    assert updated_version == current_version
    assert updated_partition == current_partition
    assert updated_state == state
  finally:
    restore_firmware(device, original_version)
