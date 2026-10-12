import pytest


def response_contains(response, expected):
  return any(expected in line for line in response)


@pytest.mark.positive
@pytest.mark.parametrize(
  'mode',
  [
    'solid',
    'blink',
    'breathe',
    pytest.param('rainbow', marks=pytest.mark.min_fw('1.5.0')),
  ],
)
def test_set_supported_mode(lamp_on_device, hil, mode):
  # Use a deterministic physical baseline so mode validation does not depend
  # on brightness or color left by a previous test.
  lamp_on_device.lamp.set_color('white')
  lamp_on_device.lamp.set_brightness(50)

  response = lamp_on_device.lamp.set_mode(mode)
  status = lamp_on_device.lamp.status()

  assert response_contains(response, f'[LAMP] mode set: {mode}')
  assert status.mode == mode

  hil.camera.video.verify(mode)


@pytest.mark.negative
def test_reject_unknown_mode(lamp_on_device):
  initial_status = lamp_on_device.lamp.status()

  response = lamp_on_device.lamp.execute('mode disco')
  status = lamp_on_device.lamp.status()

  assert response_contains(response, "error: unknown mode 'disco'")
  assert status.mode == initial_status.mode
