import pytest

from config import OTA_CORRUPTED_IMAGES
from lib import read_firmware


@pytest.mark.tc('TC-OTA-027')
@pytest.mark.regression
@pytest.mark.negative
def test_ota_rejects_corrupted_firmware(ota_connected_device):
  device = ota_connected_device

  original_version, original_partition, original_state = read_firmware(device)
  image_url = OTA_CORRUPTED_IMAGES.get(str(original_version))

  if not image_url:
    version_key = str(original_version).replace('.', '_')
    pytest.skip(f'OTA_CORRUPTED_IMAGE_{version_key} is not configured')

  assert original_state.lower() == 'valid'

  response = device.ota.url(image_url)
  output = '\n'.join(response)

  assert '[OTA] failed: image validation failed (corrupted image)' in output, (
    f'Expected corrupted image validation error: {response}'
  )

  assert '[OTA] success:' not in output

  current_version, current_partition, current_state = read_firmware(device)

  assert current_version == original_version
  assert current_partition == original_partition
  assert current_state.lower() == 'valid'
