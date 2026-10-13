from lib import UARTConnector


class OtaController:
  def __init__(self, connector: UARTConnector):
    self._connector = connector

  def check(self) -> list[str]:
    return self._connector.execute_command(
      'ota check',
      until=("Type 'ota update'", 'up to date (stable)', '[OTA] failed:'),
      timeout=60,
    )
