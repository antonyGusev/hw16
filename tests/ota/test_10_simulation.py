import pytest

from lib import read_firmware


@pytest.mark.tc('TC-OTA-024')
@pytest.mark.regression
@pytest.mark.positive
def test_ota_simulation_without_flashing(ota_connected_device):
  device = ota_connected_device

  original_version, original_partition, original_state = read_firmware(device)

  assert original_state.lower() == 'valid'

  response = device.ota.test_server()
  output = '\n'.join(response)

  assert '[OTA] failed:' not in output, f'OTA simulation failed: {response}'

  assert "ready. Type 'help' for commands" in output, (
    f'DUT did not complete reboot after simulation: {response}'
  )

  assert '[OTA] downloading:' not in output, (
    f'Unexpected firmware download during simulation: {response}'
  )

  assert '[OTA] target partition:' not in output, (
    f'Unexpected OTA partition preparation during simulation: {response}'
  )

  current_version, current_partition, current_state = read_firmware(device)

  assert current_version == original_version
  assert current_partition == original_partition
  assert current_state.lower() == 'valid'
