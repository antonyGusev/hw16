import time
from collections.abc import Callable

import pytest
from serial.tools import list_ports


def wait_for_condition(
  callback: Callable[[], bool],
  condition: bool = True,
  timeout: float = 2,
  interval: float = 0.2,
  error_message: str | Callable[[], str] | None = None,
) -> None:
  deadline = time.monotonic() + timeout

  while time.monotonic() < deadline:
    if callback() == condition:
      return

    time.sleep(interval)

  if callable(error_message):
    error_message = error_message()

  raise TimeoutError(
    error_message
    or f'Callback result is not equal to {condition} after {timeout}s'
  )


# Supported USB-to-serial adapters used to identify the connected DUT.
KNOWN_USB_DEVICES = {
  (0x1A86, 0x55D3),  # WCH CH343
  (0x1A86, 0x7523),  # WCH CH340/CH341
  (0x10C4, 0xEA60),  # Silicon Labs CP210x
  (0x0403, 0x6001),  # FTDI FT232
}


def find_device_port(fail_if_missing=True):
  ports = list(list_ports.comports())

  if not ports:
    if fail_if_missing:
      pytest.fail('No COM ports found.')

    return None

  candidates = [port for port in ports if (port.vid, port.pid) in KNOWN_USB_DEVICES]

  if not candidates:
    if fail_if_missing:
      pytest.fail('No supported USB serial devices found.')

    return None

  return candidates[0].device


def has_active_wifi_connection(device) -> bool:
  status = device.wifi.status()

  return status.ip not in (None, '', '0.0.0.0') and status.ssid not in (None, '')
