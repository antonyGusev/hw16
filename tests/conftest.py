import pytest

from config import HIL_CAMERA_URL, HIL_PORT, PASSWORD, SSID
from framework import DeviceDriver, HILDriver
from lib import UARTConnector, find_device_port


@pytest.fixture(scope='session')
def hil():
  connector = UARTConnector(HIL_PORT)
  connector.open()

  hil = HILDriver(connector, HIL_CAMERA_URL)

  try:
    yield hil
  finally:
    connector.close()


@pytest.fixture(scope='session')
def device():
  port = find_device_port()

  connector = UARTConnector(port)
  connector.open()

  device = DeviceDriver(connector)

  try:
    yield device
  finally:
    try:
      device.reboot()
    finally:
      connector.close()


@pytest.fixture
def connected_device(device):
  if device.wifi.status().ip != '0.0.0.0' and device.wifi.status().ssid not in (None, ''):
    return device
  
  result = device.wifi.connect(SSID, PASSWORD)

  assert result.connected, f'Failed to prepare connected DUT: {result.response}'

  return device


@pytest.fixture
def disconnected_device(device):
  disconnected = device.wifi.disconnect()

  assert disconnected, 'Failed to prepare disconnected DUT.'

  return device


@pytest.fixture
def rebooted_device(device):
  device.reboot()

  return device


def pytest_collection_modifyitems(items):
  def test_order(item):
    if item.get_closest_marker('positive'):
      return 0

    if item.get_closest_marker('negative'):
      return 1

    return 2

  items.sort(key=test_order)
