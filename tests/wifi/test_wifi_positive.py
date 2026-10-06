import re

from config import PASSWORD, SSID
from lib import wait_for_condition


def has_active_wifi_connection(device):
  # Firmware currently may report `connected=True` after disconnect.
  # SSID/IP/RSSI still describe whether an active connection actually exists.
  status = device.wifi.status()

  return (
    status.ssid == SSID
    and status.ip not in (None, '', '0.0.0.0')
    and status.rssi != 0
  )
  

def wait_for_led_color(hil, expected_color, timeout=5):
  # Poll without writing an image on every camera request. Artifacts are captured
  # once after polling, regardless of whether the expected color was reached.
  error = None

  try:
    wait_for_condition(
      lambda: hil.camera.is_color(expected_color),
      timeout=timeout,
      error_message=f'WS2812 did not become {expected_color}.',
    )
  except TimeoutError as exc:
    error = exc

  # Always keep camera evidence for the final observed state.
  frame = hil.camera.capture_artifacts(expected_color)

  if error is None:
    return

  # Re-run detection on the saved frame to include the measured HSV/ROI
  # in the assertion message when polling timed out.
  try:
    actual_color = hil.camera.detect_color(frame)
    details = f'detected={actual_color}, ROI source={hil.camera.roi_source}'
  except RuntimeError as exc:
    details = str(exc)

  raise AssertionError(
    f'WS2812 did not become {expected_color}. {details}'
  ) from None


def test_connect_using_ssid(disconnected_device):
  result = disconnected_device.wifi.connect(SSID, PASSWORD)

  assert result.connected
  assert any(f'successfully connected to SSID:{SSID}' in line for line in result.response)


def test_connect_using_network_number(disconnected_device):
  result = disconnected_device.wifi.connect(
    SSID,
    PASSWORD,
    by_number=True,
  )

  assert result.connected


def test_connect_using_saved_credentials(disconnected_device_with_saved_credentials):
  result = disconnected_device_with_saved_credentials.wifi.connect()

  assert result.connected
  assert any(f'successfully connected to SSID:{SSID}' in line for line in result.response)


def test_disconnect_active_connection(connected_device):
  disconnected = connected_device.wifi.disconnect()

  assert disconnected


def test_status_reports_connected_details(connected_device):
  status = connected_device.wifi.status()

  assert status.connected
  assert status.ssid == SSID
  assert status.ip is not None
  assert re.fullmatch(r'\d+\.\d+\.\d+\.\d+', status.ip)
  assert status.rssi is not None


def test_status_reports_disconnected(disconnected_device):
  status = disconnected_device.wifi.status()

  assert status.connected is False


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


def test_k3_disconnects_wifi(connected_device, hil):
  hil.buttons.k3()

  wait_for_condition(
    lambda: not has_active_wifi_connection(connected_device),
    timeout=5,
    error_message='DUT did not disconnect from Wi-Fi after K3 press.',
  )

  assert not has_active_wifi_connection(connected_device)


def test_k3_reconnects_wifi(disconnected_device_with_saved_credentials, hil):
  hil.buttons.k3()

  wait_for_condition(
    lambda: has_active_wifi_connection(disconnected_device_with_saved_credentials),
    timeout=10,
    error_message='DUT did not reconnect to Wi-Fi after K3 press.',
  )

  assert has_active_wifi_connection(disconnected_device_with_saved_credentials)


def test_wifi_connected_led_is_green(connected_device, hil):
  wait_for_led_color(hil, 'green')


def test_wifi_disconnected_led_is_red(disconnected_device, hil):
  wait_for_led_color(hil, 'red')
