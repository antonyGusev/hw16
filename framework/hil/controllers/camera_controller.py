from dataclasses import dataclass

from .modules import PhotoModule, VideoModule


@dataclass
class CameraEndpoints:
  capture_url: str
  stream_url: str


class CameraController:
  def __init__(self, endpoints: CameraEndpoints, timeout: float = 5):
    self.photo = PhotoModule(endpoints, timeout)
    self.video = VideoModule(endpoints, timeout)
