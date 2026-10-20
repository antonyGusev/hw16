from concurrent.futures import ThreadPoolExecutor

import pytest

from lib import has_active_wifi_connection, wait_for_condition


@pytest.mark.fw_only('1.3.0')
@pytest.mark.first
@pytest.mark.positive
def test_k3_without_saved_credentials(device, hil):
  with ThreadPoolExecutor(max_workers=1) as executor:
    log_future = executor.submit(
      device.wait_for_log,
      "no saved credentials, use 'connect' first",
      5,
    )

    hil.buttons.k3()
    response = log_future.result()

  assert any("no saved credentials, use 'connect' first" in line for line in response)
  assert not has_active_wifi_connection(device)


@pytest.mark.smoke
@pytest.mark.positive
def test_k3_disconnects_wifi(connected_device, hil):
  hil.buttons.k3()

  wait_for_condition(
    lambda: not has_active_wifi_connection(connected_device),
    timeout=5,
    error_message='DUT did not disconnect from Wi-Fi after K3 press.',
  )

  assert not has_active_wifi_connection(connected_device)


@pytest.mark.regression
@pytest.mark.positive
def test_k3_reconnects_wifi_after_rebooting(rebooted_device, hil):
  hil.buttons.k3()

  wait_for_condition(
    lambda: has_active_wifi_connection(rebooted_device),
    timeout=10,
    error_message='DUT did not reconnect to Wi-Fi after K3 press.',
  )

  assert has_active_wifi_connection(rebooted_device)


@pytest.mark.regression
@pytest.mark.positive
def test_k3_reconnects_wifi_after_disconnection(disconnected_device, hil):
  hil.buttons.k3()

  wait_for_condition(
    lambda: has_active_wifi_connection(disconnected_device),
    timeout=10,
    error_message='DUT did not reconnect to Wi-Fi after K3 press.',
  )

  assert has_active_wifi_connection(disconnected_device)
