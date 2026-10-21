import pytest


def response_contains(response, expected):
  return any(expected in line for line in response)


@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.parametrize(
  'mode',
  [
    pytest.param('solid', marks=pytest.mark.tc('TC-LAMP-013')),
    pytest.param('blink', marks=pytest.mark.tc('TC-LAMP-014')),
    pytest.param('breathe', marks=pytest.mark.tc('TC-LAMP-015')),
    pytest.param('rainbow', marks=[pytest.mark.fw_min('1.5.0'), pytest.mark.tc('TC-LAMP-016')]),
  ],
)
def test_set_supported_mode(lamp_on_device, hil, mode):
  # Use a deterministic physical baseline so mode validation does not depend
  # on brightness or color left by a previous test.
  lamp_on_device.lamp.set_color('yellow')
  lamp_on_device.lamp.set_brightness(50)

  response = lamp_on_device.lamp.set_mode(mode)
  status = lamp_on_device.lamp.status()

  assert response_contains(response, f'[LAMP] mode set: {mode}')
  assert status.mode == mode

  hil.camera.video.verify(mode)


@pytest.mark.tc('TC-LAMP-018')
@pytest.mark.regression
@pytest.mark.negative
def test_reject_unknown_mode(lamp_on_device):
  initial_status = lamp_on_device.lamp.status()

  response = lamp_on_device.lamp.execute('mode disco')
  status = lamp_on_device.lamp.status()

  assert response_contains(response, "error: unknown mode 'disco'")
  assert status.mode == initial_status.mode
