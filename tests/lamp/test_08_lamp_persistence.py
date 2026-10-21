import pytest


@pytest.mark.tc('TC-LAMP-028')
@pytest.mark.regression
@pytest.mark.positive
def test_lamp_settings_survive_reboot(lamp_on_device, hil):
  expected_rgb = (12, 34, 56)

  lamp_on_device.lamp.set_rgb(*expected_rgb)
  lamp_on_device.lamp.set_brightness(37)
  lamp_on_device.lamp.set_mode('breathe')

  lamp_on_device.reboot()

  status = lamp_on_device.lamp.status()

  assert not status.is_on
  assert status.color == expected_rgb
  assert status.brightness == 37
  assert status.mode == 'breathe'
  assert status.timer_s == 0

  lamp_on_device.lamp.on()

  hil.camera.photo.verify(
    'rgb',
    name='persisted_color_after_reboot',
    expected_rgb=expected_rgb,
  )

  hil.camera.video.verify(
    'breathe',
    name='persisted_breathe_after_reboot',
  )
