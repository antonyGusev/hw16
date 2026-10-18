import pytest
from packaging.version import Version

from config import OTA_HTTPS_URL, OTA_HTTPS_VERSION
from lib import ensure_wifi_connected, read_firmware


@pytest.mark.regression
@pytest.mark.positive
def test_ota_install_from_https_url(ota_connected_device):
  device = ota_connected_device

  if not OTA_HTTPS_URL or not OTA_HTTPS_VERSION:
    pytest.skip('OTA_HTTPS_URL or OTA_HTTPS_VERSION is not configured')

  assert OTA_HTTPS_URL.lower().startswith('https://'), f'Expected HTTPS URL, got: {OTA_HTTPS_URL}'

  target_version = Version(OTA_HTTPS_VERSION)

  original_version, original_partition, original_state = read_firmware(device)

  assert original_state.lower() == 'valid'

  if target_version <= original_version:
    pytest.skip(
      f'Requires newer firmware than {original_version}, configured target is {target_version}'
    )

  try:
    response = device.ota.url(OTA_HTTPS_URL)
    output = '\n'.join(response)

    assert '[OTA] downloading:' in output, f'Firmware download was not started: {response}'

    assert '[OTA] success:' in output, f'OTA installation failed: {response}'

    device.wait_for_log("ready. Type 'help' for commands", timeout=60)

    current_version, current_partition, current_state = read_firmware(device)

    assert current_version == target_version
    assert current_partition != original_partition
    assert current_state.lower() == 'valid'

  finally:
    current_version, _, _ = read_firmware(device)

    if current_version != original_version:
      ensure_wifi_connected(device)

      response = device.ota.install(str(original_version), force=True)

      assert '[OTA] success:' in '\n'.join(response), (
        f'Failed to restore firmware {original_version}: {response}'
      )

      device.wait_for_log("ready. Type 'help' for commands", timeout=60)

      restored_version, _, restored_state = read_firmware(device)

      assert restored_version == original_version
      assert restored_state.lower() == 'valid'
