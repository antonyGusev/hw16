import pytest

from test_data import SUPPORTED_COLORS


def response_contains(response, expected):
  return any(expected in line for line in response)


@pytest.mark.tc('TC-LAMP-001')
@pytest.mark.smoke
@pytest.mark.positive
def test_lamp_on(device, hil):
  try:
    response = device.lamp.on()
    status = device.lamp.status()

    assert response_contains(response, '[LAMP] on')
    assert status.is_on
    assert status.color == SUPPORTED_COLORS['white']

    hil.camera.photo.verify(
      'rgb',
      name='lamp_on_white',
      expected_rgb=status.color,
    )

  finally:
    device.lamp.off()


@pytest.mark.tc('TC-LAMP-002')
@pytest.mark.smoke
@pytest.mark.positive
def test_lamp_off(device, hil):
  device.lamp.on()

  try:
    response = device.lamp.off()
    status = device.lamp.status()

    assert response_contains(response, '[LAMP] off')
    assert not status.is_on

    hil.camera.photo.verify(
      'rgb',
      name='lamp_off_red',
      expected_rgb=SUPPORTED_COLORS['red'],
    )

  finally:
    if device.lamp.status().is_on:
      device.lamp.off()


@pytest.mark.tc('TC-LAMP-003')
@pytest.mark.regression
@pytest.mark.positive
def test_lamp_is_off_after_reboot(lamp_on_device, hil):
  lamp_on_device.reboot()

  status = lamp_on_device.lamp.status()

  assert not status.is_on
  assert status.timer_s == 0

  hil.camera.photo.verify(
    'rgb',
    name='reboot_off_red',
    expected_rgb=SUPPORTED_COLORS['red'],
  )
