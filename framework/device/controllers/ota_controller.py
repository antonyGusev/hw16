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
    
  def install(self, version: str, force: bool = False, until=None) -> list[str]:
    command = f'ota install {version}'

    if force:
      command += ' force'

    return self._connector.execute_command(
      command,
      until=until or (
        '[OTA] success:',
        '[OTA] failed:',
        '[OTA] downgrade blocked:',
      ),
      timeout=300,
    )

  def update(self, beta: bool = False) -> list[str]:
    command = 'ota update beta' if beta else 'ota update'

    return self._connector.execute_command(
      command,
      until=(
        '[OTA] success:',
        '[OTA] already up to date',
        '[OTA] failed:',
      ),
      timeout=300,
    )
    
  def url(self, url: str) -> list[str]:
    return self._connector.execute_command(
      f'ota {url}',
      until=('[OTA] success:', '[OTA] failed:'),
      timeout=300,
    )
    
  def test_server(self) -> list[str]:
    return self._connector.execute_command(
      'ota-test-server',
      until=("ready. Type 'help' for commands", '[OTA] failed:'),
      timeout=120,
    )
