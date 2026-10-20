import pytest

from config import OTA_INVALID_IMAGE_HEADER
from lib import read_firmware


@pytest.mark.regression
@pytest.mark.negative
def test_ota_rejects_invalid_image_header(ota_connected_device):
  device = ota_connected_device

  if not OTA_INVALID_IMAGE_HEADER:
    pytest.skip('OTA_INVALID_IMAGE_URL is not configured')

  original_version, original_partition, original_state = read_firmware(device)
  assert original_state.lower() == 'valid'

  try:
    response = device.ota.url(OTA_INVALID_IMAGE_HEADER)
    output = '\n'.join(response)

    assert '[OTA] failed: download interrupted (ESP_ERR_OTA_VALIDATE_FAILED)' in output, (
      f'Expected invalid OTA image validation error: {response}'
    )

    assert '[OTA] success:' not in output

    current_version, current_partition, current_state = read_firmware(device)

    assert current_version == original_version
    assert current_partition == original_partition
    assert current_state.lower() == 'valid'

  finally:
    device.reboot()


@pytest.mark.regression
@pytest.mark.negative
def test_ota_install_after_invalid_image(ota_connected_device):
  device = ota_connected_device

  if not OTA_INVALID_IMAGE_HEADER:
    pytest.skip('OTA_INVALID_IMAGE_URL is not configured')

  original_version, original_partition, original_state = read_firmware(device)
  assert original_state.lower() == 'valid'

  installation_completed = False

  try:
    response = device.ota.url(OTA_INVALID_IMAGE_HEADER)

    assert '[OTA] failed: download interrupted (ESP_ERR_OTA_VALIDATE_FAILED)' in '\n'.join(
      response
    ), f'Invalid image was not rejected as expected: {response}'

    response = device.ota.install(str(original_version), force=True)
    output = '\n'.join(response)

    assert '[OTA] error: update already in progress' not in output, (
      f'OTA remained locked after invalid image: {response}'
    )

    assert '[OTA] success:' in output, f'OTA installation failed after invalid image: {response}'

    device.wait_for_log("ready. Type 'help' for commands", timeout=60)

    current_version, current_partition, current_state = read_firmware(device)

    assert current_version == original_version
    assert current_partition != original_partition
    assert current_state.lower() == 'valid'

    installation_completed = True

  finally:
    if not installation_completed:
      device.reboot()
