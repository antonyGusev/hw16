import time

import pytest

SUPPORTED_COLORS = {
  'red': (255, 0, 0),
  'green': (0, 255, 0),
  'blue': (0, 0, 255),
  'white': (255, 255, 255),
  'yellow': (255, 180, 0),
  'purple': (160, 0, 255),
  'cyan': (0, 255, 255),
}


def response_contains(response, expected):
  return any(expected in line for line in response)


@pytest.mark.positive
def test_lamp_on(device):
  try:
    response = device.lamp.on()

    assert response_contains(response, '[LAMP] on')
    assert device.lamp.status().is_on

  finally:
    device.lamp.off()


@pytest.mark.positive
def test_lamp_off(device):
  device.lamp.on()

  try:
    response = device.lamp.off()

    assert response_contains(response, '[LAMP] off')
    assert not device.lamp.status().is_on

  finally:
    if device.lamp.status().is_on:
      device.lamp.off()


@pytest.mark.positive
def test_lamp_is_off_after_reboot(lamp_on_device):
  lamp_on_device.reboot()

  assert not lamp_on_device.lamp.status().is_on


@pytest.mark.positive
@pytest.mark.parametrize(
  ('color', 'expected_rgb'),
  SUPPORTED_COLORS.items(),
)
def test_set_named_color(lamp_on_device, hil, color, expected_rgb):
  response = lamp_on_device.lamp.set_color(color)

  assert response_contains(
    response,
    f'[LAMP] color set: {color} '
    f'({expected_rgb[0]},{expected_rgb[1]},{expected_rgb[2]})',
  )

  status = lamp_on_device.lamp.status()

  assert status.color == expected_rgb

  hil.camera.wait_for_color(color)


@pytest.mark.positive
@pytest.mark.parametrize(
  'rgb',
  [
    (0, 0, 0),
    (255, 255, 255),
    (255, 0, 128),
  ],
)
def test_set_rgb_color(lamp_on_device, rgb):
  red, green, blue = rgb

  response = lamp_on_device.lamp.set_rgb(red, green, blue)
  status = lamp_on_device.lamp.status()

  assert response_contains(response, f'[LAMP] color set: ({red},{green},{blue})')
  assert status.color == rgb


@pytest.mark.positive
@pytest.mark.parametrize('brightness', [0, 1, 50, 100])
def test_set_brightness(lamp_on_device, brightness):
  response = lamp_on_device.lamp.set_brightness(brightness)
  status = lamp_on_device.lamp.status()

  assert response_contains(response, f'[LAMP] brightness set: {brightness}%')
  assert status.brightness == brightness


@pytest.mark.positive
@pytest.mark.parametrize(
  'mode',
  [
    'solid',
    'blink',
    'breathe',
    pytest.param(
      'rainbow',
      marks=pytest.mark.min_fw('1.5.0'),
    ),
  ],
)
def test_set_supported_mode(lamp_on_device, mode):
  response = lamp_on_device.lamp.set_mode(mode)
  status = lamp_on_device.lamp.status()

  assert response_contains(response, f'[LAMP] mode set: {mode}')
  assert status.mode == mode


@pytest.mark.positive
def test_timer_expires_and_turns_lamp_off(lamp_on_device):
  response = lamp_on_device.lamp.set_timer(1)

  assert response_contains(response, '[LAMP] auto-off in 1 s')

  expiration_log = lamp_on_device.wait_for_log('[LAMP] timer expired, lamp off', timeout=2)
  status = lamp_on_device.lamp.status()

  assert response_contains(expiration_log, '[LAMP] timer expired, lamp off')
  assert not status.is_on
  assert status.timer_s == 0


@pytest.mark.positive
def test_cancel_active_timer(lamp_on_device):
  lamp_on_device.lamp.set_timer(2)

  response = lamp_on_device.lamp.set_timer(0)
  status = lamp_on_device.lamp.status()

  assert response_contains(response, '[LAMP] timer cancelled')
  assert status.is_on
  assert status.timer_s == 0

  # Prove that cancelling the timer removes the scheduled auto-off,
  # not only the timer value reported by `lamp status`.
  time.sleep(2.2)

  assert lamp_on_device.lamp.status().is_on


@pytest.mark.positive
def test_timer_accepts_upper_boundary(lamp_on_device):
  response = lamp_on_device.lamp.set_timer(3600)
  status = lamp_on_device.lamp.status()

  assert response_contains(response, '[LAMP] auto-off in 3600 s')
  assert status.is_on
  assert 3598 <= status.timer_s <= 3600

  cancel_response = lamp_on_device.lamp.set_timer(0)

  assert response_contains(cancel_response, '[LAMP] timer cancelled')
  assert lamp_on_device.lamp.status().timer_s == 0


@pytest.mark.positive
def test_timer_is_not_preserved_after_reboot(lamp_on_device):
  lamp_on_device.lamp.set_timer(10)

  lamp_on_device.reboot()

  status = lamp_on_device.lamp.status()

  assert not status.is_on
  assert status.timer_s == 0


@pytest.mark.positive
def test_lamp_status_matches_configured_state(lamp_on_device):
  lamp_on_device.lamp.set_rgb(255, 0, 128)
  lamp_on_device.lamp.set_brightness(30)
  lamp_on_device.lamp.set_mode('solid')
  lamp_on_device.lamp.set_timer(10)

  status = lamp_on_device.lamp.status()

  assert status.lamp == 'on'
  assert status.color == (255, 0, 128)
  assert status.brightness == 30
  assert status.mode == 'solid'
  assert 8 <= status.timer_s <= 10

  lamp_on_device.lamp.set_timer(0)


@pytest.mark.positive
def test_lamp_settings_survive_reboot(lamp_on_device):
  lamp_on_device.lamp.set_rgb(12, 34, 56)
  lamp_on_device.lamp.set_brightness(37)
  lamp_on_device.lamp.set_mode('breathe')

  lamp_on_device.reboot()

  status = lamp_on_device.lamp.status()

  assert not status.is_on
  assert status.color == (12, 34, 56)
  assert status.brightness == 37
  assert status.mode == 'breathe'
  assert status.timer_s == 0


@pytest.mark.min_fw('1.5.0')
@pytest.mark.positive
@pytest.mark.parametrize(
  ('scene', 'rgb', 'brightness', 'mode'),
  [
    (1, (255, 0, 0), 25, 'solid'),
    (2, (0, 255, 0), 50, 'blink'),
    (3, (0, 0, 255), 75, 'breathe'),
  ],
)
def test_save_and_load_scene(lamp_on_device, scene, rgb, brightness, mode):
  lamp_on_device.lamp.set_rgb(*rgb)
  lamp_on_device.lamp.set_brightness(brightness)
  lamp_on_device.lamp.set_mode(mode)

  save_response = lamp_on_device.lamp.save_scene(scene)

  lamp_on_device.lamp.set_rgb(1, 2, 3)
  lamp_on_device.lamp.set_brightness(10)
  lamp_on_device.lamp.set_mode('solid')

  load_response = lamp_on_device.lamp.load_scene(scene)
  status = lamp_on_device.lamp.status()

  assert response_contains(save_response, f'[LAMP] scene {scene} saved')
  assert response_contains(load_response, f'[LAMP] scene {scene} loaded')
  assert status.color == rgb
  assert status.brightness == brightness
  assert status.mode == mode


@pytest.mark.min_fw('1.5.0')
@pytest.mark.positive
def test_scene_survives_reboot(lamp_on_device):
  scene = 1
  expected_rgb = (160, 0, 255)
  expected_brightness = 42
  expected_mode = 'solid'

  lamp_on_device.lamp.set_rgb(*expected_rgb)
  lamp_on_device.lamp.set_brightness(expected_brightness)
  lamp_on_device.lamp.set_mode(expected_mode)
  lamp_on_device.lamp.save_scene(scene)

  lamp_on_device.reboot()

  load_response = lamp_on_device.lamp.load_scene(scene)
  status = lamp_on_device.lamp.status()

  assert response_contains(load_response, f'[LAMP] scene {scene} loaded')
  assert status.color == expected_rgb
  assert status.brightness == expected_brightness
  assert status.mode == expected_mode
