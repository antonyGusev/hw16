import pytest

from test_data import SUPPORTED_COLORS


def response_contains(response, expected):
  return any(expected in line for line in response)


@pytest.mark.tc('TC-LAMP-004')
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.parametrize(
  ('color', 'expected_rgb'),
  SUPPORTED_COLORS.items(),
  ids=[f'{color}_{rgb[0]}_{rgb[1]}_{rgb[2]}' for color, rgb in SUPPORTED_COLORS.items()],
)
def test_set_named_color(lamp_on_device, hil, color, expected_rgb):
  response = lamp_on_device.lamp.set_color(color)

  assert response_contains(
    response,
    f'[LAMP] color set: {color} ({expected_rgb[0]},{expected_rgb[1]},{expected_rgb[2]})',
  )

  status = lamp_on_device.lamp.status()

  assert status.color == expected_rgb

  hil.camera.photo.verify(
    'rgb',
    name=color,
    expected_rgb=expected_rgb,
  )


@pytest.mark.tc('TC-LAMP-005')
@pytest.mark.regression
@pytest.mark.negative
def test_reject_unknown_named_color(lamp_on_device):
  initial_status = lamp_on_device.lamp.status()

  response = lamp_on_device.lamp.execute('color orange')
  status = lamp_on_device.lamp.status()

  assert response_contains(response, "error: unknown color 'orange'")
  assert status.color == initial_status.color
