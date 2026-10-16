import re

import pytest

from lib import read_firmware


def read_output_state(hil, button):
  response = hil.relay_status() if button == 'k2' else hil.led_status()
  output = '\n'.join(response)

  label = 'RELAY' if button == 'k2' else 'LED'
  match = re.search(rf'\[HIL\] {label}:\s*(ON|OFF)', output)

  assert match is not None, f'Failed to read {label} state: {response}'

  return match.group(1)


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.parametrize('button', ['k2', 'k4'])
def test_ota_physical_button_during_download(connected_device, hil, button):
  device = connected_device

  original_version, original_partition, original_state = read_firmware(device)

  assert original_state.lower() == 'valid'

  initial_state = read_output_state(hil, button)
  press_button = getattr(hil.buttons, button)

  response = device.ota.install(
    str(original_version),
    force=True,
    until='[OTA] progress: 10%',
  )

  assert any('[OTA] progress: 10%' in line for line in response), (
    f'OTA did not reach 10%: {response}'
  )

  try:
    press_button()

    changed_state = read_output_state(hil, button)

    assert changed_state != initial_state, (
      f'{button.upper()} did not change physical output during OTA. '
      f'Before: {initial_state}, after: {changed_state}'
    )

  finally:
    if read_output_state(hil, button) != initial_state:
      press_button()

  response = device.wait_for_log('[OTA] success:', timeout=300)
  output = '\n'.join(response)

  assert '[OTA] success:' in output, (
    f'OTA did not complete after {button.upper()} press: {response}'
  )

  progress = [
    int(match.group(1))
    for line in response
    if (match := re.search(r'\[OTA\] progress:\s*(\d+)%', line))
  ]

  assert any(10 < percent < 100 for percent in progress), (
    f'No intermediate OTA progress after {button.upper()} press: {response}'
  )

  device.wait_for_log("ready. Type 'help' for commands", timeout=60)

  current_version, current_partition, current_state = read_firmware(device)

  assert current_version == original_version
  assert current_partition != original_partition
  assert current_state.lower() == 'valid'
