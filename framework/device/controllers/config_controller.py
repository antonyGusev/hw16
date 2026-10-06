from typing import Literal, TypeAlias

from lib import UARTConnector, ResponseParseError

# Restrict supported configuration keys at type-checking level.
ConfigKey: TypeAlias = Literal['sensor_interval', 'alarm_threshold', 'dist_threshold']


class ConfigController:
  def __init__(self, connector: UARTConnector):
    self._connector = connector

  def set(self, key: ConfigKey, value: int) -> list[str]:
    return self._connector.execute_command(f'config set {key} {value}')

  def get(self, key: ConfigKey) -> int:
    response = self._connector.execute_command(f'config get {key}')

    for line in response:
      if f'[Config] {key} =' not in line:
        continue

      # Extract only the numeric value and ignore optional units such as ms or cm.
      value = line.split('=', 1)[1].strip().split()[0]

      return int(value)

    raise ResponseParseError(f'Config value "{key}" was not found in response: {response}')

  def save(self) -> list[str]:
    return self._connector.execute_command('config save')

  def load(self) -> list[str]:
    return self._connector.execute_command('config load')
