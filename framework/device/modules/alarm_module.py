from typing import TypedDict

from lib import DeviceDriver

FIELDS_MAP = {
  'State': 'state',
  'Threshold': 'threshold',
  'Last value': 'last_value',
  'Sensor': 'sensor',
  'LED state': 'led_state',
}


class AlarmStatus(TypedDict, total=False):
  state: str
  threshold: int
  last_value: int
  sensor: str
  led_state: str


class AlarmModule:
  def __init__(self, driver: DeviceDriver):
    self._driver = driver

  def status(self) -> AlarmStatus:
    response = self._driver.execute_command('alarm status')

    status: AlarmStatus = {}

    for line in response:
      if '[Alarm]' not in line:
        continue

      # Remove the log prefix and parse only the alarm-specific payload.
      content = line.split('[Alarm]', 1)[1].strip()
      name, _, value = content.partition(':')

      # Ignore headers and other alarm lines that are not part of the expected status fields.
      if name not in FIELDS_MAP:
        continue

      key = FIELDS_MAP[name]
      value = value.strip()

      # Keep string values exactly as returned by firmware.
      if key in ('threshold', 'last_value'):
        status[key] = int(value)
      else:
        status[key] = value

    return status

  def arm(self) -> list[str]:
    return self._driver.execute_command('alarm arm')

  def disarm(self) -> list[str]:
    return self._driver.execute_command('alarm disarm')
