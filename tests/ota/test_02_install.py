import re

import pytest

from lib import ensure_wifi_connected, read_firmware


@pytest.mark.tc('TC-OTA-006')
@pytest.mark.ota_gatekeeper
@pytest.mark.positive
@pytest.mark.parametrize('channel', ['stable', 'beta'])
def test_ota_install(ota_connected_device, ota_versions, channel):
  device = ota_connected_device
  original_version, original_partition, original_state = read_firmware(device)
  target_version = ota_versions[channel]
  target = str(target_version)

  assert original_version < target_version, (
    f'Expected target firmware {target_version} to be newer than '
    f'current firmware {original_version}'
  )

  assert original_state.lower() == 'valid'

  ensure_wifi_connected(device)

  response = device.ota.install(target)
  output = '\n'.join(response)

  assert re.search(
    rf'\[OTA\] success:\s*{re.escape(str(original_version))}'
    rf'\s*->\s*{re.escape(target)}\s+in\s+\d+\s+s\. Rebooting\.\.\.',
    output,
  ), f'OTA install failed: {response}'

  device.wait_for_log("ready. Type 'help' for commands", timeout=60)

  installed_version, installed_partition, state = read_firmware(device)

  assert installed_version == target_version
  assert installed_partition != original_partition
  assert state.lower() == 'valid'


@pytest.mark.tc('TC-OTA-008')
@pytest.mark.ota_gatekeeper
@pytest.mark.positive
@pytest.mark.parametrize('channel', ['stable', 'current'])
def test_ota_install_force(ota_connected_device, ota_versions, channel):
  device = ota_connected_device
  original_version, original_partition, original_state = read_firmware(device)
  target_version = ota_versions[channel]
  target = str(target_version)

  assert original_version > target_version
  assert original_state.lower() == 'valid'

  ensure_wifi_connected(device)

  response = device.ota.install(target, force=True)
  output = '\n'.join(response)

  assert re.search(
    rf'\[OTA\] success:\s*{re.escape(str(original_version))}'
    rf'\s*->\s*{re.escape(target)}\s+in\s+\d+\s+s\. Rebooting\.\.\.',
    output,
  ), f'OTA force install failed: {response}'

  device.wait_for_log("ready. Type 'help' for commands", timeout=60)

  installed_version, installed_partition, state = read_firmware(device)

  assert installed_version == target_version
  assert installed_partition != original_partition
  assert state.lower() == 'valid'


@pytest.mark.tc('TC-OTA-007')
@pytest.mark.regression
@pytest.mark.negative
def test_ota_install_downgrade_without_force(connected_device, ota_versions):
  device = connected_device

  original_version, original_partition, original_state = read_firmware(device)

  available = sorted(set(ota_versions.values()))
  older_versions = [version for version in available if version < original_version]

  if not older_versions:
    pytest.skip(f'No older firmware available for {original_version}')

  target = older_versions[-1]

  assert original_state.lower() == 'valid'

  ensure_wifi_connected(device)

  response = device.ota.install(str(target))
  output = '\n'.join(response)

  assert '[OTA] downgrade blocked:' in output, f'Downgrade was not blocked: {response}'
  assert '[OTA] success:' not in output

  installed_version, installed_partition, state = read_firmware(device)

  assert installed_version == original_version
  assert installed_partition == original_partition
  assert state.lower() == 'valid'


@pytest.mark.tc('TC-OTA-009')
@pytest.mark.regression
@pytest.mark.positive
def test_ota_install_force_reinstall_same_version(connected_device):
  device = connected_device

  original_version, original_partition, original_state = read_firmware(device)

  assert original_state.lower() == 'valid'

  ensure_wifi_connected(device)

  response = device.ota.install(str(original_version), force=True)
  output = '\n'.join(response)

  assert '[OTA] downloading:' in output, f'OTA download was not started: {response}'

  assert re.search(
    rf'\[OTA\] success:\s*{re.escape(str(original_version))}'
    rf'\s*->\s*{re.escape(str(original_version))}'
    rf'\s+in\s+\d+\s+s\. Rebooting\.\.\.',
    output,
  ), f'OTA force reinstall failed: {response}'

  device.wait_for_log("ready. Type 'help' for commands", timeout=60)

  installed_version, installed_partition, state = read_firmware(device)

  assert installed_version == original_version
  assert installed_partition != original_partition
  assert state.lower() == 'valid'


@pytest.mark.tc('TC-OTA-010')
@pytest.mark.regression
@pytest.mark.positive
def test_ota_install_uses_inactive_partition(connected_device, ota_versions):
  device = connected_device
  original_version, original_partition, original_state = read_firmware(device)
  assert original_state.lower() == 'valid'

  available = sorted(set(ota_versions.values()))
  targets = [version for version in available if version != original_version]
  assert targets, f'No alternative firmware available for {original_version}'
  first_target = targets[-1]

  try:
    for target in (first_target, original_version):
      current_version, current_partition, state = read_firmware(device)
      assert state.lower() == 'valid'
      expected_partition = 'ota_1' if current_partition == 'ota_0' else 'ota_0'
      ensure_wifi_connected(device)

      response = device.ota.install(str(target), force=True)
      output = '\n'.join(response)
      target_partition = re.search(r'\[OTA\] target partition:\s*(ota_[01])', output)
      assert target_partition is not None, f'Target partition missing: {response}'
      assert target_partition.group(1) == expected_partition
      assert '[OTA] success:' in output, f'OTA installation failed: {response}'

      device.wait_for_log("ready. Type 'help' for commands", timeout=60)
      installed_version, installed_partition, installed_state = read_firmware(device)
      assert installed_version == target
      assert installed_partition == expected_partition
      assert installed_state.lower() == 'valid'

    restored_version, restored_partition, restored_state = read_firmware(device)
    assert restored_version == original_version
    assert restored_partition == original_partition
    assert restored_state.lower() == 'valid'
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


@pytest.mark.tc('TC-OTA-011')
@pytest.mark.regression
@pytest.mark.positive
def test_ota_install_reports_complete_progress(connected_device):
  device = connected_device
  original_version, original_partition, original_state = read_firmware(device)

  assert original_state.lower() == 'valid'

  ensure_wifi_connected(device)

  response = device.ota.install(str(original_version), force=True)
  output = '\n'.join(response)

  expected_partition = 'ota_1' if original_partition == 'ota_0' else 'ota_0'

  assert re.search(
    rf'\[OTA\] current version:\s*{re.escape(str(original_version))}'
    rf'\s*\(partition {original_partition}\)',
    output,
  ), f'Current version or partition missing: {response}'

  assert f'[OTA] target partition: {expected_partition}' in output

  assert re.search(
    rf'\[OTA\] downloading:\s*https://\S+/v{re.escape(str(original_version))}/\S+\.bin',
    output,
  ), f'Download URL missing: {response}'

  assert 'Certificate validated' in output
  assert 'Starting OTA...' in output
  assert f'Writing to <{expected_partition}> partition' in output
  assert f'[OTA] new version: {original_version}' in output

  progress = re.findall(
    r'\[OTA\] progress:\s*(\d+)%\s*\((\d+)\s*/\s*(\d+)\s*bytes\)',
    output,
  )

  assert len(progress) == 10, f'Expected 10 progress records: {progress}'

  previous_bytes = 0
  total_bytes = None

  for index, (percent, downloaded, total) in enumerate(progress, start=1):
    percent = int(percent)
    downloaded = int(downloaded)
    total = int(total)

    assert percent == index * 10
    assert downloaded > previous_bytes
    assert downloaded <= total

    if total_bytes is None:
      total_bytes = total

    assert total == total_bytes

    previous_bytes = downloaded

  assert previous_bytes == total_bytes

  assert re.search(
    rf'\[OTA\] success:\s*{re.escape(str(original_version))}'
    rf'\s*->\s*{re.escape(str(original_version))}'
    rf'\s+in\s+\d+\s+s\. Rebooting\.\.\.',
    output,
  ), f'OTA success message missing: {response}'

  device.wait_for_log("ready. Type 'help' for commands", timeout=60)

  installed_version, installed_partition, state = read_firmware(device)

  assert installed_version == original_version
  assert installed_partition == expected_partition
  assert state.lower() == 'valid'
