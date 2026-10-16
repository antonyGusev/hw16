import re
import time
from collections.abc import Callable

import pytest
from packaging.version import Version
from serial.tools import list_ports

from config import PASSWORD, SSID


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
    error_message or f'Callback result is not equal to {condition} after {timeout}s'
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


def ensure_wifi_connected(device):
  if not has_active_wifi_connection(device):
    result = device.wifi.connect(SSID, PASSWORD)
    assert result.connected, f'Wi-Fi connection failed: {result.response}'


def read_firmware(device) -> tuple[Version, str, str]:
  response = '\n'.join(device.version())
  version = re.search(r'FW:\s*v(\d+\.\d+\.\d+)', response)
  partition = re.search(r'partition:\s*(ota_[01]).*state:\s*(\w+)', response)

  assert version is not None, f'Firmware version missing: {response}'
  assert partition is not None, f'Firmware partition/state missing: {response}'

  return Version(version.group(1)), partition.group(1), partition.group(2)
