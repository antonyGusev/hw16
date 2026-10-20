import pytest


@pytest.mark.regression
@pytest.mark.positive
def test_saved_credentials_persist_after_reboot(rebooted_device):
  result = rebooted_device.wifi.connect()

  assert result.connected
