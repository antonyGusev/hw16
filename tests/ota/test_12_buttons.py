import re

import pytest

from lib import read_firmware, wait_for_condition


def read_output_state(hil, button):
  response = hil.relay_status() if button == 'k2' else hil.led_status()
  label = 'RELAY' if button == 'k2' else 'LED'

  match = re.search(rf'\[HIL\] {label}:\s*(ON|OFF)', '\n'.join(response))

  assert match is not None, f'Failed to read {label} state: {response}'

  return match.group(1)


@pytest.mark.tc('TC-OTA-026')
@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.parametrize('button', ['k2', 'k4'])
def test_ota_physical_button_during_download(ota_connected_device, hil, button):
  device = ota_connected_device

  original_version, original_partition, original_state = read_firmware(device)
  assert original_state.lower() == 'valid'

  initial_state = read_output_state(hil, button)
  press_button = getattr(hil.buttons, button)

  ota_response = device.ota.install(
    str(original_version),
    force=True,
    until='[OTA] progress: 10%',
  )

  physical_error = None
  final_state = initial_state
  button_response = []

  try:
    assert any('[OTA] progress: 10%' in line for line in ota_response), (
      f'OTA did not reach 10%: {ota_response}'
    )

    button_response = press_button()

    try:
      wait_for_condition(
        lambda: read_output_state(hil, button) != initial_state,
        timeout=2,
        interval=0.1,
        error_message=f'{button.upper()} did not change physical output during OTA.',
      )
    except TimeoutError as error:
      physical_error = error

    final_state = read_output_state(hil, button)

  finally:
    ota_response += device.wait_for_log(
      "ready. Type 'help' for commands",
      timeout=300,
    )

  button_logs = [
    line
    for line in ota_response
    if re.search(r'button\s+\d+\s+pressed|\[K[1-4]\]', line, re.IGNORECASE)
  ]

  print(f'{button.upper()} HIL response: {button_response}')
  print(f'{button.upper()} DUT logs: {button_logs}')
  print(f'{button.upper()} physical state: {initial_state} -> {final_state}')

  assert physical_error is None, (
    f'{button.upper()} did not change physical output during OTA. '
    f'Before: {initial_state}, after: {final_state}. '
    f'DUT button logs: {button_logs}. '
    f'HIL response: {button_response}'
  )

  assert '[OTA] success:' in '\n'.join(ota_response), (
    f'OTA did not complete successfully: {ota_response}'
  )

  current_version, current_partition, current_state = read_firmware(device)

  assert current_version == original_version
  assert current_partition != original_partition
  assert current_state.lower() == 'valid'
