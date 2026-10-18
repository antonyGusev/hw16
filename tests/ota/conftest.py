import pytest
import serial

from config import HIL_PORT
from framework import HILDriver
from lib import (
  DeviceTimeoutError,
  UARTConnector,
  find_device_port,
  wait_for_condition,
)


@pytest.fixture(scope='session')
def hil():
  connector = UARTConnector(HIL_PORT)
  connector.open()

  try:
    driver = HILDriver(connector)

    def hil_is_ready():
      try:
        response = driver.help()
        return any('[HIL] Commands:' in line for line in response)
      except DeviceTimeoutError:
        return False

    wait_for_condition(
      hil_is_ready,
      timeout=30,
      interval=0.5,
      error_message='HIL did not become ready.',
    )

    print('HIL ready. Powering on DUT.')
    driver.power_on()

    wait_for_condition(
      lambda: find_device_port(fail_if_missing=False) is not None,
      timeout=30,
      interval=0.5,
      error_message='DUT COM port did not appear after HIL power_on.',
    )

    driver.init_endpoints()
    yield driver
  finally:
    connector.close()


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
