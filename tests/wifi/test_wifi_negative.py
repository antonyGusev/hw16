import pytest

from config import PASSWORD, SSID

WRONG_PASSWORD = f'{PASSWORD}_wrong'
SHORT_PASSWORD = 'qwe'
NONEXISTENT_SSID = 'nonexistent_test_network'

@pytest.mark.negative
def test_wrong_password(device):
  result = device.wifi.connect(SSID, WRONG_PASSWORD)
  
  assert not result.connected
  assert result.error == 'connection_failed'
  assert any('connect to the AP fail' in line for line in result.response)

@pytest.mark.negative
def test_short_password(device):
  result = device.wifi.connect(SSID, SHORT_PASSWORD)

  assert not result.connected
  assert result.error == 'password_too_short'
  assert any('password too short' in line for line in result.response)
  assert not any('connecting to SSID:' in line for line in result.response)

@pytest.mark.negative
def test_nonexistent_ssid(device):
  result = device.wifi.connect(NONEXISTENT_SSID, PASSWORD)
  
  assert not result.connected
  assert result.error == 'connection_timeout'

  # A completed failed connection attempt must return control to the CLI.
  # Verify that the device is still alive and accepts the next command.
  assert device.help()
  
@pytest.mark.negative
def test_try_to_connect_after_3_failed_attempts(rebooted_device):
    result = rebooted_device.wifi.connect(SSID, WRONG_PASSWORD)
    assert not result.connected

    result = rebooted_device.wifi.connect(SSID, SHORT_PASSWORD)
    assert not result.connected

    result = rebooted_device.wifi.connect(NONEXISTENT_SSID, PASSWORD)
    assert not result.connected

    result = rebooted_device.wifi.connect(SSID, PASSWORD)

    assert result.connected
