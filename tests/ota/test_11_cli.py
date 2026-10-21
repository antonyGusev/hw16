import re

import pytest

from lib import read_firmware


@pytest.mark.tc('TC-OTA-025')
@pytest.mark.regression
@pytest.mark.positive
def test_ota_cli_busy_during_download(ota_connected_device):
  device = ota_connected_device

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

  # Send another CLI command without waiting for its response.
  device.version(wait=False)

  response = device.wait_for_log('[OTA] success:', timeout=300)
  output = '\n'.join(response)

  assert '[OTA] success:' in output, f'OTA did not complete successfully: {response}'

  progress = [
    int(match.group(1))
    for line in response
    if (match := re.search(r'\[OTA\] progress:\s*(\d+)%', line))
  ]

  assert progress, 'No OTA progress was received after sending version.'
  assert any(percent < 100 for percent in progress), (
    'OTA download may have completed before the CLI probe.'
  )

  assert not re.search(r'FW:\s*v\d+\.\d+\.\d+', output), (
    f'CLI version command was executed during OTA: {response}'
  )

  device.wait_for_log("ready. Type 'help' for commands", timeout=60)

  current_version, current_partition, current_state = read_firmware(device)

  assert current_version == original_version
  assert current_partition != original_partition
  assert current_state.lower() == 'valid'
