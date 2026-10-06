from lib import UARTConnector


class ButtonsController:
  def __init__(self, connector: UARTConnector):
    self._connector = connector

  def k1(self) -> list[str]:
    return self._press('k1')

  def k2(self) -> list[str]:
    return self._press('k2')

  def k3(self) -> list[str]:
    return self._press('k3')

  def k4(self) -> list[str]:
    return self._press('k4')

  def _press(self, button: str) -> list[str]:
    return self._connector.execute_command(
      button,
      timeout=2,
      until=f'[HIL] {button.upper()} release',
    )
