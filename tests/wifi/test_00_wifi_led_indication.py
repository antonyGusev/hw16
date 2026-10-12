import pytest

from test_data import SUPPORTED_COLORS


def wait_for_led_color(hil, expected_color):
  expected_rgb = SUPPORTED_COLORS[expected_color]

  # RGB verification belongs to the photo camera module in the current HIL API.
  hil.camera.photo.verify(
    'rgb',
    name=f'wifi_{expected_color}_indication',
    expected_rgb=expected_rgb,
  )


@pytest.mark.positive
def test_wifi_connected_led_is_green(connected_device, hil):
  wait_for_led_color(hil, 'green')


@pytest.mark.positive
def test_wifi_disconnected_led_is_red(disconnected_device, hil):
  wait_for_led_color(hil, 'red')
