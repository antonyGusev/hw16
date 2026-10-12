import re

import pytest
from packaging.version import Version

from config import (
  HIL_PORT,
  LAMP_DEFAULT_BRIGHTNESS,
  LAMP_DEFAULT_COLOR,
  LAMP_DEFAULT_MODE,
  LAMP_DEFAULT_RGB,
  PASSWORD,
  SSID,
)
from framework import DeviceDriver, HILDriver
from lib import UARTConnector, find_device_port, has_active_wifi_connection


def restore_default_lamp_state(device):
  status = device.lamp.status()

  if status.timer_s > 0 and status.is_on:
    device.lamp.set_timer(0)

  if status.is_on:
    device.lamp.off()

  if status.color != LAMP_DEFAULT_RGB:
    device.lamp.set_color(LAMP_DEFAULT_COLOR)

  if status.brightness != LAMP_DEFAULT_BRIGHTNESS:
    device.lamp.set_brightness(LAMP_DEFAULT_BRIGHTNESS)

  if status.mode != LAMP_DEFAULT_MODE:
    device.lamp.set_mode(LAMP_DEFAULT_MODE)

  status = device.lamp.status()

  assert not status.is_on
  assert status.color == LAMP_DEFAULT_RGB
  assert status.brightness == LAMP_DEFAULT_BRIGHTNESS
  assert status.mode == LAMP_DEFAULT_MODE
  assert status.timer_s == 0


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

  restore_default_lamp_state(device)

  try:
    yield device
  finally:
    try:
      restore_default_lamp_state(device)
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
