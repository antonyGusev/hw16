import pytest

from test_data import RGB_COLORS


def response_contains(response, expected):
  return any(expected in line for line in response)


@pytest.mark.tc('TC-LAMP-006')
@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.parametrize(
  ('color', 'rgb'),
  RGB_COLORS.items(),
  ids=[f'{color}_{rgb[0]}_{rgb[1]}_{rgb[2]}' for color, rgb in RGB_COLORS.items()],
)
def test_set_rgb_color(lamp_on_device, hil, color, rgb):
  red, green, blue = rgb

  response = lamp_on_device.lamp.set_rgb(red, green, blue)

  assert response_contains(response, f'[LAMP] color set: ({red},{green},{blue})')

  status = lamp_on_device.lamp.status()

  assert status.color == rgb

  hil.camera.photo.verify(
    'rgb',
    name=color,
    expected_rgb=rgb,
  )


@pytest.mark.tc('TC-LAMP-007')
@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.parametrize(
  'rgb',
  [
    (0, 0, 0),
    (255, 255, 255),
  ],
  ids=['min_rgb', 'max_rgb'],
)
def test_set_rgb_boundary_values(lamp_on_device, hil, rgb):
  red, green, blue = rgb

  response = lamp_on_device.lamp.set_rgb(red, green, blue)
  status = lamp_on_device.lamp.status()

  assert response_contains(response, f'[LAMP] color set: ({red},{green},{blue})')
  assert status.color == rgb

  # Verify that the physical LED also reflects the accepted boundary value.
  hil.camera.photo.verify(
    'rgb',
    name='rgb_boundary',
    expected_rgb=rgb,
  )


@pytest.mark.tc('TC-LAMP-008')
@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.parametrize(
  ('red', 'green', 'blue'),
  [
    (-1, 0, 0),
    (256, 0, 0),
    (0, -1, 0),
    (0, 256, 0),
    (0, 0, -1),
    (0, 0, 256),
  ],
)
def test_reject_rgb_values_outside_range(lamp_on_device, red, green, blue):
  initial_status = lamp_on_device.lamp.status()

  response = lamp_on_device.lamp.execute(f'color {red} {green} {blue}')
  status = lamp_on_device.lamp.status()

  assert response_contains(response, 'error: rgb values must be 0-255')
  assert status.color == initial_status.color
