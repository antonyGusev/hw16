import re

import pytest

from config import SSID


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
