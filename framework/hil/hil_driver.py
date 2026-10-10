from lib import UARTConnector

from .controllers import ButtonsController, CameraController, CameraEndpoints


class HILDriver:
  def __init__(self, connector: UARTConnector):
    self._connector = connector

    self._camera_endpoints = CameraEndpoints(
      capture_url='',
      stream_url='',
    )

    self.buttons = ButtonsController(connector)
    self.camera = CameraController(self._camera_endpoints)

  def help(self) -> list[str]:
    return self._connector.execute_command('help')

  def camera_status(self) -> list[str]:
    return self._connector.execute_command('camera_status')

  def camera_capture(self) -> list[str]:
    return self._connector.execute_command('camera_capture')

  def camera_stream(self) -> list[str]:
    return self._connector.execute_command('camera_stream')

  def init_endpoints(self):
    endpoints = self._initialize_camera_endpoints()

    self._camera_endpoints.capture_url = endpoints.capture_url
    self._camera_endpoints.stream_url = endpoints.stream_url

    return self

  def _get_camera_url(self, command: str, prefix: str) -> str:
    response = self._connector.execute_command(command)

    if not response:
      raise RuntimeError(f'{command} response is empty.')

    line = response[0].strip()

    if not line.startswith(prefix):
      raise RuntimeError(f'Unexpected {command} response: {response}')

    return line.removeprefix(prefix).strip()


  def _initialize_camera_endpoints(self) -> CameraEndpoints:
    capture_url = self._get_camera_url('camera_capture', '[HIL] Camera capture: ')
    stream_url = self._get_camera_url('camera_stream', '[HIL] Camera stream: ')

    return CameraEndpoints(capture_url=capture_url, stream_url=stream_url)
  