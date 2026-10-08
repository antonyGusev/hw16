import json
from dataclasses import dataclass

from lib import ResponseParseError, UARTConnector


@dataclass
class LampStatus:
  lamp: str
  color: tuple[int, int, int]
  brightness: int
  mode: str
  timer_s: int

  @property
  def is_on(self) -> bool:
    return self.lamp == 'on'


class LampController:
  def __init__(self, connector: UARTConnector):
    self._connector = connector

  def on(self) -> list[str]:
    return self._connector.execute_command('lamp on', until='[LAMP]')

  def off(self) -> list[str]:
    return self._connector.execute_command('lamp off', until='[LAMP]')
  
  def status_raw(self) -> list[str]:
    return self._connector.execute_command('lamp status', until='"lamp"')

  def status(self) -> LampStatus:
    return self._parse_status(self.status_raw())

  def set_color(self, name: str) -> list[str]:
    return self._connector.execute_command(f'lamp color {name}', until='[LAMP]')

  def set_rgb(self, red: int, green: int, blue: int) -> list[str]:
    return self._connector.execute_command(f'lamp color {red} {green} {blue}', until='[LAMP]')

  def set_brightness(self, brightness: int) -> list[str]:
    return self._connector.execute_command(f'lamp brightness {brightness}', until='[LAMP]')

  def set_mode(self, mode: str) -> list[str]:
    return self._connector.execute_command(f'lamp mode {mode}', until='[LAMP]')

  def set_timer(self, seconds: int) -> list[str]:
    return self._connector.execute_command(f'lamp timer {seconds}', until='[LAMP]')

  def save_scene(self, scene: int) -> list[str]:
    return self._connector.execute_command(f'lamp scene save {scene}', until='[LAMP]')

  def load_scene(self, scene: int) -> list[str]:
    return self._connector.execute_command(f'lamp scene load {scene}', until='[LAMP]')

  def execute(self, subcommand: str) -> list[str]:
    # Keep a generic escape hatch for protocol-level negative tests such as
    # `lamp blabla` without exposing the UART connector to the test layer.
    return self._connector.execute_command(f'lamp {subcommand}')

  # region Service Methods

  def _parse_status(self, response: list[str]) -> LampStatus:
    payload = None

    for line in response:
      line = line.strip()

      if not line.startswith('{'):
        continue

      try:
        candidate = json.loads(line)
      except json.JSONDecodeError as exc:
        raise ResponseParseError(
          f'Lamp status contains invalid JSON: {line}'
        ) from exc

      if isinstance(candidate, dict) and candidate.get('lamp') in ('on', 'off'):
        payload = candidate
        break

    if payload is None:
      raise ResponseParseError(f'Lamp status JSON was not found in response: {response}')

    required_fields = ('lamp', 'color', 'brightness', 'mode', 'timer_s')
    missing_fields = [field for field in required_fields if field not in payload]

    if missing_fields:
      raise ResponseParseError(
        f'Lamp status is missing fields {missing_fields}: {payload}'
      )

    color = payload['color']

    if (
      not isinstance(color, list)
      or len(color) != 3
      or not all(isinstance(value, int) for value in color)
    ):
      raise ResponseParseError(f'Invalid lamp color in status: {color}')

    brightness = payload['brightness']
    mode = payload['mode']
    timer_s = payload['timer_s']

    if not isinstance(brightness, int):
      raise ResponseParseError(f'Invalid lamp brightness in status: {brightness}')

    if not isinstance(mode, str):
      raise ResponseParseError(f'Invalid lamp mode in status: {mode}')

    if not isinstance(timer_s, int):
      raise ResponseParseError(f'Invalid lamp timer in status: {timer_s}')

    return LampStatus(
      lamp=payload['lamp'],
      color=tuple(color),
      brightness=brightness,
      mode=mode,
      timer_s=timer_s,
    )

  # endregion
