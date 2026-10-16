import pytest

from lib import ensure_wifi_connected, has_active_wifi_connection, read_firmware


@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.parametrize(
  'command',
  [
    'ota check',
    'ota update',
    'ota update beta',
    'ota install {version}',
    'ota install {version} force',
    'ota broken',
    'ota https://example.com/firmware.bin',
    'ota-test-server',
  ],
)
def test_ota_without_wifi(disconnected_device, command):
  device = disconnected_device
  original_version, original_partition, original_state = read_firmware(device)

  assert original_state.lower() == 'valid'
  assert not has_active_wifi_connection(device)

  command = command.format(version=original_version)

  try:
    response = device._connector.execute_command(
      command,
      until="[OTA] failed: WiFi not connected. Use 'connect' first.",
      timeout=10,
    )

    output = '\n'.join(response)

    assert "[OTA] failed: WiFi not connected. Use 'connect' first." in output, (
      f'Expected OTA Wi-Fi error for {command}: {response}'
    )

    assert '[OTA] downloading:' not in output
    assert '[OTA] success:' not in output

    current_version, current_partition, state = read_firmware(device)

    assert current_version == original_version
    assert current_partition == original_partition
    assert state.lower() == 'valid'
    assert not has_active_wifi_connection(device)

  finally:
    ensure_wifi_connected(device)
