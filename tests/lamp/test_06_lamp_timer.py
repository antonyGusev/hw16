import pytest

from test_data import SUPPORTED_COLORS


def response_contains(response, expected):
  return any(expected in line for line in response)


@pytest.mark.tc('TC-LAMP-019')
@pytest.mark.regression
@pytest.mark.positive
def test_timer_expires_and_turns_lamp_off(lamp_on_device, hil):
  response = lamp_on_device.lamp.set_timer(1)

  assert response_contains(response, '[LAMP] auto-off in 1 s')

  log = lamp_on_device.wait_for_log('[LAMP] timer expired, lamp off', timeout=2)
  status = lamp_on_device.lamp.status()

  assert response_contains(log, '[LAMP] timer expired, lamp off')
  assert not status.is_on
  assert status.timer_s == 0

  hil.camera.photo.verify(
    'rgb',
    name='timer_expired_red',
    expected_rgb=SUPPORTED_COLORS['red'],
  )


@pytest.mark.tc('TC-LAMP-020')
@pytest.mark.regression
@pytest.mark.positive
def test_cancel_active_timer(lamp_on_device, hil):
  lamp_on_device.lamp.set_color('yellow')
  lamp_on_device.lamp.set_timer(2)

  response = lamp_on_device.lamp.set_timer(0)
  status = lamp_on_device.lamp.status()

  assert response_contains(response, '[LAMP] timer cancelled')
  assert status.is_on
  assert status.timer_s == 0

  hil.camera.video.verify(
    'stable_color',
    name='cancelled_timer',
  )

  assert lamp_on_device.lamp.status().is_on


@pytest.mark.tc('TC-LAMP-021')
@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.parametrize('seconds', [1, 3600])
def test_timer_accepts_boundary_values(lamp_on_device, seconds):
  response = lamp_on_device.lamp.set_timer(seconds)
  status = lamp_on_device.lamp.status()

  assert response_contains(response, f'[LAMP] auto-off in {seconds} s')
  assert status.is_on
  assert 0 <= status.timer_s <= seconds

  cancel_response = lamp_on_device.lamp.set_timer(0)

  assert response_contains(cancel_response, '[LAMP] timer cancelled')
  assert lamp_on_device.lamp.status().timer_s == 0


@pytest.mark.tc('TC-LAMP-024')
@pytest.mark.regression
@pytest.mark.positive
def test_timer_is_not_preserved_after_reboot(lamp_on_device, hil):
  lamp_on_device.lamp.set_timer(10)

  lamp_on_device.reboot()

  status = lamp_on_device.lamp.status()

  assert not status.is_on
  assert status.timer_s == 0

  hil.camera.photo.verify(
    'rgb',
    name='timer_after_reboot_red',
    expected_rgb=SUPPORTED_COLORS['red'],
  )


@pytest.mark.tc('TC-LAMP-022')
@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.parametrize('seconds', [-1, 3601])
def test_reject_invalid_timer(lamp_on_device, seconds):
  lamp_on_device.lamp.set_timer(0)

  response = lamp_on_device.lamp.execute(f'timer {seconds}')
  status = lamp_on_device.lamp.status()

  assert response_contains(response, 'error: timer must be 1-3600 s (0 = cancel)')
  assert status.timer_s == 0


@pytest.mark.tc('TC-LAMP-023')
@pytest.mark.regression
@pytest.mark.negative
def test_reject_timer_when_lamp_is_off(device):
  device.lamp.off()

  response = device.lamp.execute('timer 5')
  status = device.lamp.status()

  assert response_contains(response, 'error: lamp is off')
  assert not status.is_on
  assert status.timer_s == 0
