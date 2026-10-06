from typing import ClassVar, Literal, TypeAlias

from lib import UARTConnector

# Restrict supported distance modes at type-checking level.
DistanceMode: TypeAlias = Literal['single', '10s', '1m']


class DistanceSensorController:
  _COMMANDS: ClassVar[dict[DistanceMode, tuple[str, str, int]]] = {
    'single': ('distance', '[Distance] #1', 2),
    '10s': ('distance 10s', '[Distance] Done.', 12),
    '1m': ('distance 1m', '[Distance] Done.', 65),
  }

  def __init__(self, connector: UARTConnector):
    self._connector = connector

  def get(self, mode: DistanceMode = 'single') -> list[float]:
    command, pattern, timeout = self._COMMANDS[mode]

    if mode == 'single':
      response = self._connector.execute_command(command, timeout=timeout, until=pattern)

    else:
      self._connector.write_command(command)

      # Fail early if the distance subsystem does not produce
      # the first reading within 5 seconds.
      response = self._connector.wait_for_response('[Distance] #', timeout=5)

      # After the first reading, continue collecting data until firmware
      # reports that the requested measurement period is complete.
      response += self._connector.wait_for_response(pattern, timeout=timeout)

    return self._parse_readings(response)

  # region Service Methods

  def _parse_readings(self, response: list[str]) -> list[float]:
    readings = []

    for line in response:
      if '[Distance] #' not in line:
        continue

      value = line.split('[Distance]', 1)[1]
      value = value.split('cm', 1)[0].split()[-1]

      readings.append(float(value))

    return readings

  # endregion
