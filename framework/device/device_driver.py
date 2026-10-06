from lib import UARTConnector

from .controllers import (
  AlarmController,
  AuthController,
  ConfigController,
  DistanceSensorController,
  WifiController,
)


class DeviceDriver:
  def __init__(self, connector: UARTConnector):
    self._connector = connector

    self.auth = AuthController(connector)
    self.alarm = AlarmController(connector)
    self.config = ConfigController(connector)
    self.distance = DistanceSensorController(connector)
    self.wifi = WifiController(connector)

  def help(self) -> list[str]:
    return self._connector.execute_command('help')

  def status(self) -> list[str]:
    return self._connector.execute_command('status')

  def reboot(self) -> list[str]:
    # Reboot does not return a regular command response,
    # so wait until firmware reports that the device is ready again.
    self._connector.write_command('reboot')

    return self._connector.wait_for_response("ready. Type 'help' for commands", timeout=10)

  def wait_for_log(self, pattern: str, timeout: float = 5) -> list[str]:
    return self._connector.wait_for_response(pattern, timeout)
