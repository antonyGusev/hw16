import pytest


def response_contains(response, expected):
  return any(expected in line for line in response)


@pytest.mark.tc('TC-LAMP-034')
@pytest.mark.regression
@pytest.mark.negative
def test_reject_unknown_lamp_command(device):
  response = device.lamp.execute('blabla')

  assert response_contains(response, "error: unknown lamp command. See 'help'")
