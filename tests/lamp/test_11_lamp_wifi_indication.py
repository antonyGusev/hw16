import pytest

from lib import has_active_wifi_connection
from test_data import SUPPORTED_COLORS


def response_contains(response, expected):
  return any(expected in line for line in response)


@pytest.mark.tc('TC-LAMP-036')
@pytest.mark.regression
@pytest.mark.positive
def test_wifi_connected_indication_is_restored_after_lamp_off(connected_device, hil):
  connected_device.led.auto()
  connected_device.lamp.set_color('blue')
  connected_device.lamp.set_brightness(50)
  connected_device.lamp.set_mode('solid')
  connected_device.lamp.on()

  response = connected_device.lamp.off()
  status = connected_device.lamp.status()

  assert response_contains(response, '[LAMP] off')
  assert not status.is_on

  hil.camera.photo.verify(
    'rgb',
    name='wifi_connected_indication_after_lamp_off',
    expected_rgb=SUPPORTED_COLORS['green'],
  )


@pytest.mark.tc('TC-LAMP-036')
@pytest.mark.regression
@pytest.mark.positive
def test_wifi_disconnected_indication_is_restored_after_lamp_off(disconnected_device, hil):
  disconnected_device.led.auto()
  disconnected_device.lamp.set_color('blue')
  disconnected_device.lamp.set_brightness(50)
  disconnected_device.lamp.set_mode('solid')
  disconnected_device.lamp.on()

  assert not has_active_wifi_connection(disconnected_device)

  response = disconnected_device.lamp.off()
  status = disconnected_device.lamp.status()

  assert response_contains(response, '[LAMP] off')
  assert not status.is_on

  hil.camera.photo.verify(
    'rgb',
    name='wifi_disconnected_indication_after_lamp_off',
    expected_rgb=SUPPORTED_COLORS['red'],
  )
