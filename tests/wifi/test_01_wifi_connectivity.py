import pytest

from config import PASSWORD, SSID
from lib import has_active_wifi_connection

WRONG_PASSWORD = f'{PASSWORD}_wrong'
SHORT_PASSWORD = 'qwe'
NONEXISTENT_SSID = 'nonexistent_test_network'


@pytest.mark.smoke
@pytest.mark.positive
def test_connect_using_ssid(device):
  result = device.wifi.connect(SSID, PASSWORD)

  assert result.connected
  assert any(f'successfully connected to SSID:{SSID}' in line for line in result.response)


@pytest.mark.regression
@pytest.mark.positive
def test_connect_using_network_number(disconnected_device):
  result = disconnected_device.wifi.connect(
    SSID,
    PASSWORD,
    by_number=True,
  )

  assert result.connected


@pytest.mark.smoke
@pytest.mark.positive
def test_connect_using_saved_credentials(disconnected_device):
  result = disconnected_device.wifi.connect()

  assert result.connected
  assert any(f'successfully connected to SSID:{SSID}' in line for line in result.response)


@pytest.mark.smoke
@pytest.mark.positive
def test_disconnect_active_connection(connected_device):
  disconnected = connected_device.wifi.disconnect()

  assert disconnected


@pytest.mark.smoke
@pytest.mark.positive
def test_scan_reports_rssi_and_channel(device):
  networks = device.wifi.scan()

  network = next(
    (network for network in networks if network.ssid == SSID),
    None,
  )

  assert network is not None
  assert isinstance(network.rssi, int)
  assert isinstance(network.channel, int)
  assert network.channel > 0


@pytest.mark.regression
@pytest.mark.negative
def test_wrong_password(rebooted_device):
  result = rebooted_device.wifi.connect(SSID, WRONG_PASSWORD)

  assert not result.connected
  assert result.error in ('connection_failed', 'connection_timeout'), (
    f'Unexpected connection result: {result.response}'
  )
  assert not has_active_wifi_connection(rebooted_device)


@pytest.mark.regression
@pytest.mark.negative
def test_short_password(rebooted_device):
  result = rebooted_device.wifi.connect(SSID, SHORT_PASSWORD)

  assert not result.connected
  assert result.error == 'password_too_short'
  assert any('password too short' in line for line in result.response)
  assert not any('connecting to SSID:' in line for line in result.response)


@pytest.mark.regression
@pytest.mark.negative
def test_nonexistent_ssid(rebooted_device):
  result = rebooted_device.wifi.connect(NONEXISTENT_SSID, PASSWORD)

  assert not result.connected
  assert result.error == 'connection_timeout'

  # A completed failed connection attempt must return control to the CLI.
  # Verify that the device is still alive and accepts the next command.
  assert rebooted_device.help()


@pytest.mark.regression
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
