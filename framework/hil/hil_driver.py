from lib import UARTConnector

from .controllers import ButtonsController, CameraController


class HILDriver:
  def __init__(self, connector: UARTConnector, camera_url: str):
    self._connector = connector

    self.buttons = ButtonsController(connector)
    self.camera = CameraController(camera_url)

  def help(self) -> list[str]:
      return self._connector.execute_command('help')

  def camera_status(self) -> list[str]:
      return self._connector.execute_command('camera_status')
    
  def camera_url(self) -> list[str]:
      return self._connector.execute_command('camera_url')
    
  @staticmethod
  def initialize_camera_url(connector: UARTConnector) -> str:
    response = connector.execute_command('camera_url')

    if not response:
      raise RuntimeError('Camera URL response is empty.')

    line = response[0].strip()
    prefix = '[HIL] Camera capture: '

    if line.startswith(prefix):
      return line.removeprefix(prefix).strip()

    raise RuntimeError(line)
    