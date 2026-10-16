import pytest

from config import OTA_CORRUPTED_IMAGE
from lib import read_firmware


@pytest.mark.regression
@pytest.mark.negative
def test_ota_rejects_corrupted_firmware(connected_device):
  device = connected_device

  if not OTA_CORRUPTED_IMAGE:
    pytest.skip('OTA_CORRUPTED_IMAGE_URL is not configured')

  original_version, original_partition, original_state = read_firmware(device)

  assert original_state.lower() == 'valid'

  response = device.ota.url(OTA_CORRUPTED_IMAGE)
  output = '\n'.join(response)

  assert '[OTA] failed: image validation failed (corrupted image)' in output, (
    f'Expected corrupted image validation error: {response}'
  )

  assert '[OTA] success:' not in output

  current_version, current_partition, current_state = read_firmware(device)

  assert current_version == original_version
  assert current_partition == original_partition
  assert current_state.lower() == 'valid'
