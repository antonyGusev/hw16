from lib import UARTConnector


class LedController:
  def __init__(self, connector: UARTConnector):
    self._connector = connector

  def on(self) -> list[str]:
    return self._connector.execute_command('led on')

  def off(self) -> list[str]:
    return self._connector.execute_command('led off')

  def auto(self) -> list[str]:
    return self._connector.execute_command('led auto')

  def rgb(self) -> list[str]:
    return self._connector.execute_command('led rgb')
