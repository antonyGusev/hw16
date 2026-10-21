import pytest


def response_contains(response, expected):
  return any(expected in line for line in response)


@pytest.mark.tc('TC-LAMP-009')
@pytest.mark.smoke
@pytest.mark.positive
def test_set_brightness(lamp_on_device, hil):
  lamp_on_device.lamp.set_color('yellow')
  lamp_on_device.lamp.set_mode('solid')

  measured = {}

  for brightness in (0, 10, 50, 100):
    response = lamp_on_device.lamp.set_brightness(brightness)
    status = lamp_on_device.lamp.status()

    assert response_contains(response, f'[LAMP] brightness set: {brightness}%'), (
      f'Failed to set brightness to {brightness}%. Response: {response}'
    )
    assert status.brightness == brightness, (
      f'Expected brightness {brightness}%, got {status.brightness}%'
    )

    measured[brightness] = hil.camera.photo.measure('brightness')

    print(
      f'Brightness {brightness}%: measured={measured[brightness]:.2f}, status={status.brightness}%'
    )

  hil.camera.photo.verify(
    'brightness',
    name='brightness_levels',
    brightness_levels=measured,
  )


@pytest.mark.tc('TC-LAMP-012')
@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.parametrize(
  ('mode', 'duration'),
  [
    ('blink', 3.0),
    ('breathe', 7.0),
    # Rainbow completes one full color cycle in approximately 5 seconds.
    pytest.param('rainbow', 6.0, marks=pytest.mark.fw_min('1.5.0')),
  ],
)
def test_brightness_applies_in_all_modes(lamp_on_device, hil, mode, duration):
  brightness = 30

  lamp_on_device.lamp.set_color('white')
  lamp_on_device.lamp.set_brightness(brightness)

  lamp_on_device.lamp.set_mode('solid')
  solid_intensity = hil.camera.photo.measure('brightness')

  lamp_on_device.lamp.set_mode(mode)
  mode_intensity = hil.camera.video.measure('max_brightness', duration)

  assert mode_intensity == pytest.approx(solid_intensity, rel=0.1)


@pytest.mark.tc('TC-LAMP-011')
@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.parametrize('brightness', [-5, 150])
def test_reject_brightness_outside_range(lamp_on_device, brightness):
  initial_status = lamp_on_device.lamp.status()

  try:
    response = lamp_on_device.lamp.execute(f'brightness {brightness}')
    status = lamp_on_device.lamp.status()

    assert response_contains(response, 'error: brightness must be 0-100')
    assert status.brightness == initial_status.brightness
  finally:
    # Restore the valid brightness even when buggy firmware accepts
    # the invalid value, so the failure cannot affect later feature tests.
    current_status = lamp_on_device.lamp.status()

    if current_status.brightness != initial_status.brightness:
      lamp_on_device.lamp.set_brightness(initial_status.brightness)
