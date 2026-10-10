import re

import pytest

from config import PASSWORD, SSID
from lib import wait_for_condition
from test_data import SUPPORTED_COLORS

"""
Test helpers
"""


def has_active_wifi_connection(device):
  # Firmware currently may report `connected=True` after disconnect.
  # SSID/IP/RSSI still describe whether an active connection actually exists.
  status = device.wifi.status()

  return status.ssid == SSID and status.ip not in (None, '', '0.0.0.0') and status.rssi != 0


def wait_for_led_color(hil, expected_color, timeout=5):
  expected_rgb = SUPPORTED_COLORS[expected_color]
  hil.camera.wait_for_rgb_color(expected_color, expected_rgb, timeout=timeout)


"""
Tests
"""


@pytest.mark.positive
def test_wifi_not_connected_led_is_red(device, hil):
  wait_for_led_color(hil, 'red')


@pytest.mark.positive
def test_connect_using_ssid(device):
  result = device.wifi.connect(SSID, PASSWORD)

  assert result.connected
  assert any(f'successfully connected to SSID:{SSID}' in line for line in result.response)


@pytest.mark.positive
def test_connect_using_network_number(disconnected_device):
  result = disconnected_device.wifi.connect(
    SSID,
    PASSWORD,
    by_number=True,
  )

  assert result.connected


@pytest.mark.positive
def test_connect_using_saved_credentials(disconnected_device):
  result = disconnected_device.wifi.connect()

  assert result.connected
  assert any(f'successfully connected to SSID:{SSID}' in line for line in result.response)


@pytest.mark.positive
def test_disconnect_active_connection(connected_device):
  disconnected = connected_device.wifi.disconnect()

  assert disconnected


@pytest.mark.positive
def test_saved_credentials_persist_after_reboot(rebooted_device):
  result = rebooted_device.wifi.connect()

  assert result.connected


@pytest.mark.positive
def test_status_reports_connected_details(connected_device):
  status = connected_device.wifi.status()

  assert status.connected
  assert status.ssid == SSID
  assert status.ip is not None
  assert re.fullmatch(r'\d+\.\d+\.\d+\.\d+', status.ip)
  assert status.rssi is not None


@pytest.mark.positive
def test_status_reports_disconnected(disconnected_device):
  status = disconnected_device.wifi.status()

  assert status.connected is False


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


@pytest.mark.positive
def test_k3_disconnects_wifi(connected_device, hil):
  hil.buttons.k3()

  wait_for_condition(
    lambda: not has_active_wifi_connection(connected_device),
    timeout=5,
    error_message='DUT did not disconnect from Wi-Fi after K3 press.',
  )

  assert not has_active_wifi_connection(connected_device)


@pytest.mark.positive
def test_k3_reconnects_wifi_after_rebooting(rebooted_device, hil):
  hil.buttons.k3()

  wait_for_condition(
    lambda: has_active_wifi_connection(rebooted_device),
    timeout=10,
    error_message='DUT did not reconnect to Wi-Fi after K3 press.',
  )

  assert has_active_wifi_connection(rebooted_device)


@pytest.mark.positive
def test_k3_reconnects_wifi_after_disconnection(disconnected_device, hil):
  hil.buttons.k3()

  wait_for_condition(
    lambda: has_active_wifi_connection(disconnected_device),
    timeout=10,
    error_message='DUT did not reconnect to Wi-Fi after K3 press.',
  )

  assert has_active_wifi_connection(disconnected_device)


@pytest.mark.positive
def test_wifi_connected_led_is_green(connected_device, hil):
  wait_for_led_color(hil, 'green')


@pytest.mark.positive
def test_wifi_disconnected_led_is_red(disconnected_device, hil):
  wait_for_led_color(hil, 'red')
