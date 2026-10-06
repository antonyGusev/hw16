from pathlib import Path
from typing import ClassVar

import cv2
import numpy as np
import requests
  

class CameraDriver:
  COLOR_REFERENCES: ClassVar[dict[str, tuple[int, int, int]]] = {
    'red': (178, 189, 246),
    'green': (80, 234, 255),
  }

  COLOR_TOLERANCE: ClassVar[dict[str, int]] = {
    'h': 5,
    's': 20,
    'v': 20,
  }
  
  def __init__(
    self,
    base_url: str,
    timeout: float = 5,
    roi_x: int = 0,
    roi_y: int = 0,
    roi_width: int = 100,
    roi_height: int = 100,
  ):
    self.base_url = base_url.rstrip('/')
    self.timeout = timeout

    self.roi_x = roi_x
    self.roi_y = roi_y
    self.roi_width = roi_width
    self.roi_height = roi_height

  def capture(self) -> np.ndarray:
    response = requests.get(
      f'{self.base_url}/capture',
      timeout=self.timeout,
    )
    response.raise_for_status()

    image_data = np.frombuffer(response.content, dtype=np.uint8)

    frame = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

    if frame is None:
      raise RuntimeError('Failed to decode camera JPEG.')

    return frame

  def select_roi(self, frame: np.ndarray) -> tuple[int, int, int, int]:
    roi = cv2.selectROI(
      'Select WS2812',
      frame,
      showCrosshair=True,
      fromCenter=False,
    )

    cv2.destroyAllWindows()

    x, y, width, height = map(int, roi)

    if width == 0 or height == 0:
      raise RuntimeError('ROI selection was cancelled.')

    return x, y, width, height

  def set_roi(
    self,
    x: int,
    y: int,
    width: int,
    height: int,
  ) -> None:
    self.roi_x = x
    self.roi_y = y
    self.roi_width = width
    self.roi_height = height

  def get_roi(self, frame: np.ndarray) -> np.ndarray:
    x1 = self.roi_x
    y1 = self.roi_y

    x2 = x1 + self.roi_width
    y2 = y1 + self.roi_height

    frame_height, frame_width = frame.shape[:2]

    if x1 < 0 or y1 < 0 or x2 > frame_width or y2 > frame_height:
      raise ValueError(
        'ROI is outside the camera frame. '
        f'ROI=({x1}, {y1}, {x2}, {y2}), '
        f'frame={frame_width}x{frame_height}'
      )

    roi = frame[y1:y2, x1:x2]

    if roi.size == 0:
      raise RuntimeError('Camera ROI is empty.')

    return roi

  def measure_color(self, roi: np.ndarray) -> tuple[int, int, int]:
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    saturation = hsv[:, :, 1]
    value = hsv[:, :, 2]

    # Ignore dark background and overexposed white pixels.
    mask = (saturation >= 100) & (value >= 80)

    pixels = hsv[mask]

    if len(pixels) == 0:
      raise RuntimeError('No colored LED pixels found inside camera ROI.')

    median_hue = int(np.median(pixels[:, 0]))
    median_saturation = int(np.median(pixels[:, 1]))
    median_value = int(np.median(pixels[:, 2]))

    return median_hue, median_saturation, median_value

  def measure_roi_color(self, frame: np.ndarray) -> tuple[int, int, int]:
    roi = self.get_roi(frame)

    return self.measure_color(roi)

  def save_debug_image(self, frame: np.ndarray, path: str | Path) -> None:
    path = Path(path)

    path.parent.mkdir(parents=True, exist_ok=True)

    debug_frame = frame.copy()

    x1 = self.roi_x
    y1 = self.roi_y

    x2 = x1 + self.roi_width
    y2 = y1 + self.roi_height

    cv2.rectangle(
      debug_frame,
      (x1, y1),
      (x2, y2),
      (255, 255, 255),
      2,
    )

    cv2.imwrite(str(path), debug_frame)

  def save_roi(self, frame: np.ndarray, path: str | Path) -> None:
    path = Path(path)

    path.parent.mkdir(parents=True, exist_ok=True)

    roi = self.get_roi(frame)

    cv2.imwrite(str(path), roi)
    
  def detect_color(self, frame: np.ndarray) -> str:
    actual_h, actual_s, actual_v = self.measure_roi_color(frame)

    for color, reference in self.COLOR_REFERENCES.items():
      expected_h, expected_s, expected_v = reference

      hue_diff = self._hue_distance(actual_h, expected_h)
      saturation_diff = abs(actual_s - expected_s)
      value_diff = abs(actual_v - expected_v)

      if (
        hue_diff <= self.COLOR_TOLERANCE['h']
        and saturation_diff <= self.COLOR_TOLERANCE['s']
        and value_diff <= self.COLOR_TOLERANCE['v']
      ):
        return color

    raise RuntimeError(
      f'Unknown WS2812 color: '
      f'H={actual_h}, S={actual_s}, V={actual_v}'
    )
    
  def is_color(self, expected_color: str) -> bool:
    try:
      return self.detect_color(self.capture()) == expected_color
    except RuntimeError:
      return False

  @staticmethod
  def _hue_distance(actual: int, expected: int) -> int:
    difference = abs(actual - expected)

    return min(difference, 180 - difference)
