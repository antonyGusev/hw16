import pytest


@pytest.fixture
def lamp_on_device(device):
  device.lamp.on()

  yield device

  device.lamp.off()


@pytest.fixture(scope='package', autouse=True)
def ensure_lamp_off_after_suite(device):
  yield

  try:
    device.lamp.off()
  finally:
    status = device.lamp.status()

    if status.lamp != 'off':
      device.lamp.off()
      status = device.lamp.status()

    assert status.lamp == 'off'
