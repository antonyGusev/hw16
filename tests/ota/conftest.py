import re

import pytest
import serial
from packaging.version import Version

from config import PASSWORD, SSID
from lib import (
  DeviceTimeoutError,
  find_device_port,
  has_active_wifi_connection,
  wait_for_condition,
)


@pytest.fixture(scope='session')
def ota_versions(ota_device):
  if not has_active_wifi_connection(ota_device):
    result = ota_device.wifi.connect(SSID, PASSWORD)
    assert result.connected, f'Wi-Fi connection failed: {result.response}'

  response = ota_device.ota.check()
  output = '\n'.join(response)

  versions = {}

  for channel in ('current', 'stable', 'beta'):
    label = 'current version' if channel == 'current' else f'{channel} channel'
    match = re.search(rf'\[OTA\] {label}:\s*v?(\d+\.\d+\.\d+)', output)

    assert match is not None, f'{label} missing in OTA check: {response}'

    versions[channel] = Version(match.group(1))

  return versions


@pytest.fixture(scope='session')
def ota_device(hil, ota_device):
  connector = ota_device._connector

  def is_ready() -> bool:
    try:
      response = ota_device.version()
      return any('state:' in line for line in response)
    except (DeviceTimeoutError, serial.SerialException):
      return False

  try:
    wait_for_condition(
      is_ready,
      timeout=10,
      interval=0.5,
      error_message='DUT did not respond after HIL power_on.',
    )

  except TimeoutError:
    print('DUT is not responding. Performing HIL power cycle...')

    connector.close()
    hil.power_cycle()

    wait_for_condition(
      lambda: find_device_port(fail_if_missing=False) is not None,
      timeout=30,
      interval=0.5,
      error_message='DUT COM port did not reappear after HIL power cycle.',
    )

    def reconnect_uart() -> bool:
      try:
        connector.open()
        return True
      except serial.SerialException:
        return False

    wait_for_condition(
      reconnect_uart,
      timeout=30,
      interval=0.5,
      error_message='DUT UART did not reopen after HIL power cycle.',
    )

    wait_for_condition(
      is_ready,
      timeout=20,
      interval=0.5,
      error_message='DUT did not respond after HIL power cycle.',
    )

  return ota_device
