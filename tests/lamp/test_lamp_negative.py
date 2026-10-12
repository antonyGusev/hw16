import pytest


def response_contains(response, expected):
  return any(expected in line for line in response)


@pytest.mark.min_fw('1.5.0')
@pytest.mark.first
@pytest.mark.negative
def test_reject_loading_empty_scene(lamp_on_device):
  scene = 3

  # Set a known lamp state so we can verify that a failed scene load
  # does not modify any current lamp settings.
  lamp_on_device.lamp.set_rgb(12, 34, 56)
  lamp_on_device.lamp.set_brightness(37)
  lamp_on_device.lamp.set_mode('solid')
  lamp_on_device.lamp.set_timer(0)

  initial_status = lamp_on_device.lamp.status()

  response = lamp_on_device.lamp.execute(f'scene load {scene}')
  status = lamp_on_device.lamp.status()

  assert response_contains(response, f'error: scene {scene} is empty')
  assert status == initial_status


@pytest.mark.negative
def test_reject_unknown_named_color(lamp_on_device):
  initial_status = lamp_on_device.lamp.status()

  response = lamp_on_device.lamp.execute('color orange')
  status = lamp_on_device.lamp.status()

  assert response_contains(response, "error: unknown color 'orange'")
  assert status.color == initial_status.color


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


@pytest.mark.negative
@pytest.mark.parametrize('brightness', [-5, 150])
def test_reject_brightness_outside_range(lamp_on_device, brightness):
  initial_status = lamp_on_device.lamp.status()

  response = lamp_on_device.lamp.execute(f'brightness {brightness}')
  status = lamp_on_device.lamp.status()

  assert response_contains(response, 'error: brightness must be 0-100')
  assert status.brightness == initial_status.brightness


@pytest.mark.negative
def test_reject_unknown_mode(lamp_on_device):
  initial_status = lamp_on_device.lamp.status()

  response = lamp_on_device.lamp.execute('mode disco')
  status = lamp_on_device.lamp.status()

  assert response_contains(response, "error: unknown mode 'disco'")
  assert status.mode == initial_status.mode


@pytest.mark.negative
@pytest.mark.parametrize('seconds', [-1, 3601])
def test_reject_invalid_timer(lamp_on_device, seconds):
  lamp_on_device.lamp.set_timer(0)

  response = lamp_on_device.lamp.execute(f'timer {seconds}')
  status = lamp_on_device.lamp.status()

  assert response_contains(response, 'error: timer must be 1-3600 s (0 = cancel)')
  assert status.timer_s == 0


@pytest.mark.negative
def test_reject_timer_when_lamp_is_off(device):
  device.lamp.off()

  response = device.lamp.execute('timer 5')
  status = device.lamp.status()

  assert response_contains(response, 'error: lamp is off')
  assert not status.is_on
  assert status.timer_s == 0


@pytest.mark.min_fw('1.5.0')
@pytest.mark.negative
@pytest.mark.parametrize(
  'command',
  [
    'scene save 0',
    'scene save 4',
    'scene load 0',
    'scene load 4',
  ],
)
def test_reject_invalid_scene_number(lamp_on_device, command):
  scene = 1
  expected_rgb = (12, 34, 56)
  expected_brightness = 37
  expected_mode = 'solid'

  lamp_on_device.lamp.set_rgb(*expected_rgb)
  lamp_on_device.lamp.set_brightness(expected_brightness)
  lamp_on_device.lamp.set_mode(expected_mode)
  lamp_on_device.lamp.save_scene(scene)

  response = lamp_on_device.lamp.execute(command)

  assert response_contains(response, 'error: scene must be 1-3')

  lamp_on_device.lamp.set_rgb(1, 2, 3)
  lamp_on_device.lamp.set_brightness(10)
  lamp_on_device.lamp.set_mode('breathe')

  load_response = lamp_on_device.lamp.load_scene(scene)
  status = lamp_on_device.lamp.status()

  assert response_contains(load_response, f'[LAMP] scene {scene} loaded')
  assert status.color == expected_rgb
  assert status.brightness == expected_brightness
  assert status.mode == expected_mode


@pytest.mark.negative
@pytest.mark.parametrize(
  'command',
  [
    'scene save 1',
    'scene load 1',
  ],
)
def test_reject_scene_commands_before_fw_1_5_0(lamp_on_device, firmware_version, command):
  if str(firmware_version) not in ('1.3.0', '1.4.0'):
    pytest.skip('Applicable only to firmware 1.3.0 and 1.4.0')

  response = lamp_on_device.lamp.execute(command)

  assert response_contains(response, 'error: scenes not implemented yet')


@pytest.mark.negative
def test_reject_unknown_lamp_command(device):
  response = device.lamp.execute('blabla')

  assert response_contains(response, "error: unknown lamp command. See 'help'")
