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
  # Reset Wi-Fi state first so this fixture does not depend on a previous test.
  device.wifi.disconnect()

  result = device.wifi.connect(SSID, PASSWORD)

  assert result.connected, f'Failed to prepare connected DUT: {result.response}'

  return device


@pytest.fixture
def disconnected_device(device):
  disconnected = device.wifi.disconnect()

  assert disconnected, 'Failed to prepare disconnected DUT.'

  return device


@pytest.fixture
def disconnected_device_with_saved_credentials(device):
  # Recreate saved credentials explicitly, then leave the DUT disconnected.
  device.wifi.disconnect()

  result = device.wifi.connect(SSID, PASSWORD)

  assert result.connected, f'Failed to save Wi-Fi credentials: {result.response}'

  disconnected = device.wifi.disconnect()

  assert disconnected, 'Failed to prepare disconnected DUT.'

  return device
