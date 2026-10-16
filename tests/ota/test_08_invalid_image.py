import pytest

from config import OTA_INVALID_IMAGE_HEADER
from lib import read_firmware


@pytest.mark.regression
@pytest.mark.negative
def test_ota_rejects_invalid_image_header(connected_device):
  device = connected_device

  if not OTA_INVALID_IMAGE_HEADER:
    pytest.skip('OTA_INVALID_IMAGE_URL is not configured')

  original_version, original_partition, original_state = read_firmware(device)

  assert original_state.lower() == 'valid'

  response = device.ota.url(OTA_INVALID_IMAGE_HEADER)
  output = '\n'.join(response)

  assert '[OTA] failed: invalid image header' in output, (
    f'Expected invalid image header error: {response}'
  )

  assert '[OTA] success:' not in output

  current_version, current_partition, current_state = read_firmware(device)

  assert current_version == original_version
  assert current_partition == original_partition
  assert current_state.lower() == 'valid'
