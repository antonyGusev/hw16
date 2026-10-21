import json

import pytest


@pytest.mark.tc('TC-LAMP-025')
@pytest.mark.smoke
@pytest.mark.positive
def test_lamp_status_returns_valid_json(lamp_on_device):
  response = lamp_on_device.lamp.status_raw()

  json_lines = [line.strip() for line in response if line.strip().startswith('{')]

  assert len(json_lines) == 1

  payload = json.loads(json_lines[0])

  assert set(payload) == {
    'lamp',
    'color',
    'brightness',
    'mode',
    'timer_s',
  }

  assert type(payload['lamp']) is str
  assert payload['lamp'] in ('on', 'off')

  assert type(payload['color']) is list
  assert len(payload['color']) == 3
  assert all(type(value) is int for value in payload['color'])

  assert type(payload['brightness']) is int
  assert type(payload['mode']) is str
  assert type(payload['timer_s']) is int


@pytest.mark.tc('TC-LAMP-026')
@pytest.mark.regression
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
