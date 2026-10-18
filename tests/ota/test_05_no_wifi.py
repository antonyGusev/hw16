import pytest

from lib import ensure_wifi_connected, has_active_wifi_connection, read_firmware


@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.parametrize(
  'case',
  [
    {'method': 'check', 'args': {}, 'id': 'ota check'},
    {'method': 'update', 'args': {}, 'id': 'ota update'},
    {'method': 'update', 'args': {'beta': True}, 'id': 'ota update beta'},
    {'method': 'install', 'args': {}, 'id': 'ota install'},
    {'method': 'install', 'args': {'force': True}, 'id': 'ota install force'},
    {'method': 'broken', 'args': {}, 'id': 'ota broken'},
    {'method': 'url', 'args': {'url': 'https://example.com/firmware.bin'}, 'id': 'ota url'},
    {'method': 'test_server', 'args': {}, 'id': 'ota-test-server'},
  ],
  ids=lambda case: case['id'],
)
def test_ota_without_wifi(rebooted_device, case):
  device = rebooted_device
  original_version, original_partition, original_state = read_firmware(device)

  assert original_state.lower() == 'valid'
  assert not has_active_wifi_connection(device)

  expected_error = "[OTA] failed: WiFi not connected. Use 'connect' first."

  kwargs = case['args'].copy()

  if case['method'] == 'install':
    kwargs['version'] = str(original_version)

  kwargs['until'] = (
    expected_error,
    '[OTA] check failed:',
    '[OTA] failed:',
    '[OTA] error:',
    '=== OTA Update Started ===',
  )
  kwargs['timeout'] = 30

  try:
    response = getattr(device.ota, case['method'])(**kwargs)
    output = '\n'.join(response)

    assert expected_error in output, f'Expected OTA Wi-Fi error for {case["id"]}: {response}'

    assert '[OTA] downloading:' not in output
    assert '[OTA] success:' not in output

    current_version, current_partition, state = read_firmware(device)

    assert current_version == original_version
    assert current_partition == original_partition
    assert state.lower() == 'valid'
    assert not has_active_wifi_connection(device)

  finally:
    ensure_wifi_connected(device)


@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.parametrize(
  'beta',
  [
    pytest.param(False, id='stable'),
    pytest.param(True, id='beta'),
  ],
)
def test_ota_after_wifi_disconnect(ota_connected_device, beta):
  device = ota_connected_device
  original_version, original_partition, original_state = read_firmware(device)

  assert original_state.lower() == 'valid'
  assert has_active_wifi_connection(device)

  expected_error = "[OTA] failed: WiFi not connected. Use 'connect' first."

  try:
    assert device.wifi.disconnect(), 'Wi-Fi disconnect was not confirmed.'
    assert not has_active_wifi_connection(device)

    response = device.ota.update(
      beta=beta,
      until=(
        expected_error,
        '[OTA] check failed:',
        '[OTA] error:',
        '[OTA] success:',
      ),
      timeout=30,
    )

    assert expected_error in '\n'.join(response), (
      f'OTA did not reject update after Wi-Fi disconnect: {response}'
    )

    current_version, current_partition, state = read_firmware(device)

    assert current_version == original_version
    assert current_partition == original_partition
    assert state.lower() == 'valid'
    assert not has_active_wifi_connection(device)

  finally:
    ensure_wifi_connected(device)
