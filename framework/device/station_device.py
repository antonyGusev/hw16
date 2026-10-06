from lib import DeviceDriver

from .modules import AlarmModule, AuthModule, ConfigModule, DistanceSensorModule, WifiModule


class StationDevice:
  def __init__(self, driver: DeviceDriver):
    self._driver = driver

    self.auth = AuthModule(driver)
    self.alarm = AlarmModule(driver)
    self.config = ConfigModule(driver)
    self.distance = DistanceSensorModule(driver)
    self.wifi = WifiModule(driver)

  def help(self) -> list[str]:
    return self._driver.execute_command('help')

  def status(self) -> list[str]:
    return self._driver.execute_command('status')

  def reboot(self) -> list[str]:
    # Reboot does not return a regular command response,
    # so wait until firmware reports that the device is ready again.
    self._driver.write_command('reboot')

    return self._driver.wait_for_response("ready. Type 'help' for commands", timeout=10)
  
  def wait_for_log(self, pattern: str, timeout: float = 5) -> list[str]:
    return self._driver.wait_for_response(pattern, timeout)
