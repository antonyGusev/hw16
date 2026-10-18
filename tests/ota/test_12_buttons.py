import re

import pytest

from lib import read_firmware, wait_for_condition


def read_output_state(hil, button):
  response = hil.relay_status() if button == 'k2' else hil.led_status()
  label = 'RELAY' if button == 'k2' else 'LED'

  match = re.search(rf'\[HIL\] {label}:\s*(ON|OFF)', '\n'.join(response))

  assert match is not None, f'Failed to read {label} state: {response}'

  return match.group(1)


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.parametrize('button', ['k2', 'k4'])
def test_ota_physical_button_during_download(ota_connected_device, hil, button):
  device = ota_connected_device

  original_version, original_partition, original_state = read_firmware(device)
  assert original_state.lower() == 'valid'

  initial_state = read_output_state(hil, button)
  press_button = getattr(hil.buttons, button)

  response = device.ota.install(
    str(original_version),
    force=True,
    until='[OTA] progress: 10%',
  )

  try:
    assert any('[OTA] progress: 10%' in line for line in response), (
      f'OTA did not reach 10%: {response}'
    )

    press_button()

    wait_for_condition(
      lambda: read_output_state(hil, button) != initial_state,
      timeout=2,
      interval=0.1,
      error_message=(
        f'{button.upper()} did not change physical output during OTA. '
        f'Initial state: {initial_state}'
      ),
    )

  finally:
    response = device.wait_for_log(
      "ready. Type 'help' for commands",
      timeout=300,
    )

  assert '[OTA] success:' in '\n'.join(response), f'OTA did not complete successfully: {response}'

  current_version, current_partition, current_state = read_firmware(device)

  assert current_version == original_version
  assert current_partition != original_partition
  assert current_state.lower() == 'valid'
