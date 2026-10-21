import pytest

from test_data import SUPPORTED_COLORS


@pytest.mark.tc('TC-LAMP-035')
@pytest.mark.regression
@pytest.mark.positive
def test_lamp_overrides_wifi_and_led_commands(connected_device, hil):
  expected_rgb = SUPPORTED_COLORS['blue']

  connected_device.lamp.set_color('blue')
  connected_device.lamp.set_brightness(50)
  connected_device.lamp.set_mode('solid')
  connected_device.lamp.on()

  try:
    initial_status = connected_device.lamp.status()

    hil.camera.photo.verify(
      'rgb',
      name='lamp_priority_initial',
      expected_rgb=expected_rgb,
    )

    connected_device.wifi.disconnect()

    status_after_wifi_change = connected_device.lamp.status()

    assert status_after_wifi_change == initial_status

    hil.camera.photo.verify(
      'rgb',
      name='lamp_priority_after_wifi_change',
      expected_rgb=expected_rgb,
    )

    connected_device.led.off()

    status_after_led_command = connected_device.lamp.status()

    assert status_after_led_command == initial_status

    hil.camera.photo.verify(
      'rgb',
      name='lamp_priority_after_led_command',
      expected_rgb=expected_rgb,
    )

  finally:
    connected_device.led.auto()
    connected_device.lamp.off()
