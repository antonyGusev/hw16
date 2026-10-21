import pytest

from test_data import SUPPORTED_COLORS


@pytest.mark.tc('TC-LAMP-027')
@pytest.mark.first
@pytest.mark.positive
def test_default_lamp_state_on_clean_device(device):
  status = device.lamp.status()

  assert not status.is_on
  assert status.color == SUPPORTED_COLORS['white']
  assert status.brightness == 50
  assert status.mode == 'solid'
