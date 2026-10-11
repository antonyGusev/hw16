import re

import pytest
from packaging.version import Version

from config import HIL_PORT, PASSWORD, SSID
from framework import DeviceDriver, HILDriver
from lib import UARTConnector, find_device_port, has_active_wifi_connection


def pytest_collection_modifyitems(items):
  def test_order(item):
    if item.get_closest_marker('first'):
      return -1

    if item.get_closest_marker('positive'):
      return 0

    if item.get_closest_marker('negative'):
      return 1

    return 2

  items.sort(key=test_order)


@pytest.fixture(scope='session')
def hil():
  connector = UARTConnector(HIL_PORT)
  connector.open()

  hil = HILDriver(connector).init_endpoints()

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
  if has_active_wifi_connection(device):
    return device

  result = device.wifi.connect(SSID, PASSWORD)

  assert result.connected, f'Failed to prepare connected DUT: {result.response}'

  return device


@pytest.fixture
def disconnected_device(device):
  disconnected = device.wifi.disconnect()
  is_connected = has_active_wifi_connection(device)

  assert disconnected, 'Failed to prepare disconnected DUT.'
  assert not is_connected, 'DUT is still connected to Wi-Fi after disconnecting.'

  return device


@pytest.fixture
def rebooted_device(device):
  device.reboot()

  return device


@pytest.fixture(scope='session')
def firmware_version(device) -> Version:
  response = device.version()

  for line in response:
    match = re.search(r'FW:\s*v(\d+\.\d+\.\d+)', line)

    if match:
      return Version(match.group(1))

  raise RuntimeError(f'Firmware version was not found in response: {response}')


@pytest.fixture(autouse=True)
def check_min_firmware(request):
  marker = request.node.get_closest_marker('min_fw')

  if marker is None:
    return

  firmware_version = request.getfixturevalue('firmware_version')
  required_version = Version(marker.args[0])

  if firmware_version < required_version:
    pytest.skip(f'Requires firmware >= {required_version}, current firmware is {firmware_version}')
