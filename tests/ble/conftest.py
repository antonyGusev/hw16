import pytest

from framework import StationDevice
from lib import DeviceDriver, find_device_port


@pytest.fixture(scope='session')
def device():
  port = find_device_port()

  driver = DeviceDriver(port)
  driver.open()

  device = StationDevice(driver)

  try:
    yield device
  finally:
    driver.close()
