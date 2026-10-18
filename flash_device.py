import re

import serial

from config import FIRMWARE_PATH, HIL_PORT
from framework import DeviceDriver, HILDriver
from lib import FirmwareFlasher, UARTConnector, find_device_port, wait_for_condition


def wait_for_device(port: str, timeout: float = 15) -> None:
  connector = UARTConnector(port)
  device = DeviceDriver(connector)

  def is_ready() -> bool:
    try:
      if connector.ser is None or not connector.ser.is_open:
        connector.open()

      response = device.help()

      return any(re.match(r'^\s*version(?:\s|$)', line) for line in response)
    except (serial.SerialException, OSError):
      connector.close()
      return False

  try:
    wait_for_condition(
      is_ready,
      timeout=timeout,
      interval=0.5,
      error_message=f'DUT is not responding to help on {port}.',
    )
  finally:
    connector.close()


def main():
  hil_connector = UARTConnector(HIL_PORT)
  hil_connector.open()

  try:
    hil = HILDriver(hil_connector)
    hil.power_on()

    port = find_device_port()

    flasher = FirmwareFlasher()
    flasher.erase(port)
    flasher.flash(port, str(FIRMWARE_PATH))

    try:
      wait_for_device(port)
      print('DUT is ready after flashing.')

    except TimeoutError:
      print('DUT is not responding. Performing HIL power cycle...')

      hil.power_cycle()

      wait_for_device(port, timeout=30)
      print('DUT recovered after power cycle.')

  finally:
    hil_connector.close()


if __name__ == '__main__':
  main()
