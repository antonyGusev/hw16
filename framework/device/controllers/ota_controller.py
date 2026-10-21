from lib import UARTConnector


class OtaController:
  def __init__(self, connector: UARTConnector):
    self._connector = connector

  def check(self, until=None, timeout=60) -> list[str]:
    return self._connector.execute_command(
      'ota check',
      until=until
      if until is not None
      else (
        "Type 'ota update'",
        'up to date (stable)',
        '[OTA] failed:',
      ),
      timeout=timeout,
    )

  def install(self, version: str, force: bool = False, until=None, timeout=300) -> list[str]:
    command = f'ota install {version}'

    if force:
      command += ' force'

    return self._connector.execute_command(
      command,
      until=until
      if until is not None
      else (
        '[OTA] success:',
        '[OTA] failed:',
        '[OTA] error:',
        '[OTA] downgrade blocked:',
      ),
      timeout=timeout,
    )

  def update(self, beta: bool = False, until=None, timeout=300) -> list[str]:
    command = 'ota update beta' if beta else 'ota update'

    return self._connector.execute_command(
      command,
      until=until
      if until is not None
      else (
        '[OTA] success:',
        '[OTA] already up to date',
        '[OTA] failed:',
        '[OTA] error:',
      ),
      timeout=timeout,
    )

  def url(self, url: str, until=None, timeout=300) -> list[str]:
    return self._connector.execute_command(
      f'ota {url}',
      until=until
      if until is not None
      else (
        '[OTA] success:',
        '[OTA] failed:',
        '[OTA] error:',
        '[OTA] downgrade blocked:',
        '[OTA]downgrade blocked:',
      ),
      timeout=timeout,
    )

  def broken(self, until=None, timeout=300, wait: bool = True) -> list[str] | None:
    if not wait:
      self._connector.write_command('ota broken')
      return None

    return self._connector.execute_command(
      'ota broken',
      until=until
      if until is not None
      else (
        '[OTA] success:',
        '[OTA] failed:',
        '[OTA] error:',
      ),
      timeout=timeout,
    )

  def test_server(self, until=None, timeout=120) -> list[str]:
    return self._connector.execute_command(
      'ota-test-server',
      until=until
      if until is not None
      else (
        "ready. Type 'help' for commands",
        '[OTA] failed:',
      ),
      timeout=timeout,
    )
