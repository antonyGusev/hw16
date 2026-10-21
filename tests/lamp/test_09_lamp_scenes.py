import pytest


def response_contains(response, expected):
  return any(expected in line for line in response)


@pytest.mark.tc('TC-LAMP-031')
@pytest.mark.fw_min('1.5.0')
@pytest.mark.regression
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


@pytest.mark.tc('TC-LAMP-029')
@pytest.mark.fw_min('1.5.0')
@pytest.mark.smoke
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


@pytest.mark.tc('TC-LAMP-032')
@pytest.mark.fw_min('1.5.0')
@pytest.mark.regression
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


@pytest.mark.tc('TC-LAMP-030')
@pytest.mark.fw_min('1.5.0')
@pytest.mark.regression
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

@pytest.mark.tc('TC-LAMP-033')
@pytest.mark.regression
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
