from lib import UARTConnector

from .controllers import (
  AlarmController,
  AuthController,
  ConfigController,
  DistanceSensorController,
  LampController,
  LedController,
  OtaController,
  WifiController,
)


class DeviceDriver:
  def __init__(self, connector: UARTConnector):
    self._connector = connector

    self.auth = AuthController(connector)
    self.alarm = AlarmController(connector)
    self.config = ConfigController(connector)
    self.distance = DistanceSensorController(connector)
    self.lamp = LampController(connector)
    self.led = LedController(connector)
    self.ota = OtaController(connector)
    self.wifi = WifiController(connector)

  def help(self) -> list[str]:
    return self._connector.execute_command('help')

  def status(self) -> list[str]:
    return self._connector.execute_command('status')
  
  def version(self, wait=True) -> list[str]:
    if wait:
      return self._connector.execute_command('version', until='state:')
    else:
      return self._connector.write_command('version')

  def reboot(self) -> list[str]:
    # Reboot does not return a regular command response,
    # so wait until firmware reports that the device is ready again.
    self._connector.write_command('reboot')

    return self._connector.wait_for_response("main_task: Returned from app_main()", timeout=20)

  def wait_for_log(self, pattern: str, timeout: float = 5) -> list[str]:
    return self._connector.wait_for_response(pattern, timeout)
