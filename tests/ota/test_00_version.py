import re

import pytest


@pytest.mark.tc('TC-OTA-001')
@pytest.mark.ota_gatekeeper
@pytest.mark.positive
def test_version_reports_firmware_partition_and_state(ota_device):
  response = ota_device.version()
  output = '\n'.join(response)

  firmware = re.search(
    r'FW:\s*v(\d+\.\d+\.\d+)\s+\(build\s+([^)]+)\)',
    output,
  )
  partition = re.search(
    r'partition:\s*(ota_[01])\s*@\s*(0x[0-9a-fA-F]+),\s*state:\s*([^\r\n]+)',
    output,
  )

  assert firmware is not None, f'Invalid FW version/build format: {response}'
  assert firmware.group(2).strip(), f'Firmware build date is empty: {response}'
  assert partition is not None, f'Invalid OTA partition/state format: {response}'
  assert int(partition.group(2), 16) > 0, f'Invalid OTA partition address: {response}'
  assert partition.group(3).strip(), f'OTA image state is empty: {response}'


@pytest.mark.tc('TC-OTA-002')
@pytest.mark.regression
@pytest.mark.positive
def test_firmware_version_matches_boot_log_and_ota_check(connected_device):
  version_response = connected_device.version()
  check_response = connected_device.ota.check()
  boot_log = connected_device.reboot()

  def extract_version(lines, pattern, source):
    match = re.search(pattern, '\n'.join(lines))
    assert match is not None, f'{source} version not found: {lines}'
    return match.group(1)

  boot_version = extract_version(boot_log, r'App version:\s*v?(\d+\.\d+\.\d+)', 'Boot log')
  firmware_version = extract_version(version_response, r'FW:\s*v(\d+\.\d+\.\d+)', 'version')
  ota_version = extract_version(
    check_response, r'\[OTA\] current version:\s*v?(\d+\.\d+\.\d+)', 'ota check'
  )

  assert boot_version == firmware_version == ota_version, (
    f'Firmware version mismatch: boot={boot_version}, '
    f'version={firmware_version}, ota check={ota_version}'
  )
