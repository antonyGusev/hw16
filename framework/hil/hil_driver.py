from lib import UARTConnector

from .controllers import ButtonsController, CameraController


class HILDriver:
  def __init__(self, connector: UARTConnector, camera_url: str):
    self._connector = connector

    self.buttons = ButtonsController(connector)
    self.camera = CameraController(camera_url)
