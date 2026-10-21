import re

import pytest
from packaging.version import Version

from config import PASSWORD, SSID
from lib import has_active_wifi_connection, read_firmware


def check_channels(device):
  response = device.ota.check()
  output = '\n'.join(response)
  current = re.search(r'\[OTA\] current version:\s*(\d+\.\d+\.\d+)', output)
  stable = re.search(r'\[OTA\] stable channel:\s*(\d+\.\d+\.\d+)', output)
  beta = re.search(r'\[OTA\] beta channel:\s*(\d+\.\d+\.\d+)', output)
  version, _, _ = read_firmware(device)

  assert current is not None, f'Current version missing: {response}'
  assert stable is not None, f'Stable channel version missing: {response}'
  assert beta is not None, f'Beta channel version missing: {response}'
  assert Version(current.group(1)) == version

  return output, Version(stable.group(1)), Version(beta.group(1))


def install_firmware(device, target):
  if not has_active_wifi_connection(device):
    result = device.wifi.connect(SSID, PASSWORD)
    assert result.connected, f'Wi-Fi connection failed: {result.response}'

  response = device.ota.install(str(target), force=True)
  assert '[OTA] success:' in '\n'.join(response), f'OTA install failed: {response}'

  device.wait_for_log("ready. Type 'help' for commands", timeout=60)

  version, _, _ = read_firmware(device)
  assert version == target

  if not has_active_wifi_connection(device):
    result = device.wifi.connect(SSID, PASSWORD)
    assert result.connected, f'Wi-Fi reconnection after OTA failed: {result.response}'
  

@pytest.mark.tc('TC-OTA-003')
@pytest.mark.ota_gatekeeper
@pytest.mark.positive
def test_ota_check_reports_stable_and_beta_versions(ota_connected_device, ota_versions):
  device = ota_connected_device

  print(f'Wi-Fi before version: {device.wifi.status()}')

  version_response = device.version()
  print(f'Version response: {version_response}')

  print(f'Wi-Fi after version: {device.wifi.status()}')

  original_version, _, _ = read_firmware(device)

  print(f'Wi-Fi before OTA check: {device.wifi.status()}')

  output, stable, beta = check_channels(device)
  assert stable <= beta, f'Stable channel {stable} newer than beta {beta}: {output}'

  available = sorted(set(ota_versions.values()))
  older = [version for version in available if version < stable]
  if not older:
    pytest.skip(f'No firmware older than stable {stable} is available')

  try:
    install_firmware(device, older[-1])
    output, reported_stable, reported_beta = check_channels(device)
    assert reported_stable == stable
    assert reported_beta == beta
    assert "[OTA] update available. Type 'ota update'" in output, output

    install_firmware(device, stable)
    output, reported_stable, reported_beta = check_channels(device)
    assert reported_stable == stable
    assert reported_beta == beta
    assert '[OTA] up to date (stable)' in output, output
  finally:
    version, _, _ = read_firmware(device)
    
    if version != original_version:
      install_firmware(device, original_version)
