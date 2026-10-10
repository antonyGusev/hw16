from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np
import requests

from lib import wait_for_condition

RGB_HUE_TOLERANCE = 20
WHITE_SATURATION_MAX = 120
WHITE_VALUE_MIN = 180
CAMERA_ROI = (280, 355, 75, 75)


@dataclass
class CameraEndpoints:
  capture_url: str
  stream_url: str


class CameraController:
  def __init__(self, endpoints: CameraEndpoints, timeout: float = 5):
    # Keep a reference to the same mutable endpoints object used by HILDriver.
    # If HILDriver refreshes the URLs after reconnect, CameraController
    # automatically starts using the new endpoints.
    self._endpoints = endpoints
    self.timeout = timeout

  def capture(self) -> np.ndarray:
    """Capture a single frame from the HIL camera."""
    response = requests.get(self._endpoints.capture_url, timeout=self.timeout)

    response.raise_for_status()

    image = np.frombuffer(response.content, dtype=np.uint8)
    frame = cv2.imdecode(image, cv2.IMREAD_COLOR)

    if frame is None:
      raise RuntimeError('Failed to decode camera frame.')

    return frame

  def open_stream(self) -> cv2.VideoCapture:
    """Open the current MJPEG stream from the HIL camera."""
    stream = cv2.VideoCapture(self._endpoints.stream_url)

    if not stream.isOpened():
      stream.release()
      raise RuntimeError(f'Failed to open camera stream: {self._endpoints.stream_url}')

    return stream

  def capture_artifacts(self, name: str) -> np.ndarray:
    """Capture a frame and save debug and ROI images."""
    frame = self.capture()

    self.save_debug_image(frame, f'artifacts/camera/{name}_debug.jpg')
    self.save_roi(frame, f'artifacts/camera/{name}_roi.jpg')

    return frame

  def get_roi(self, frame: np.ndarray) -> np.ndarray:
    """Return the fixed lamp ROI from the frame."""
    x, y, width, height = self._validated_roi(frame)

    return frame[
      y : y + height,
      x : x + width,
    ]

  def measure_color(self, roi: np.ndarray) -> tuple[int, int, int]:
    """Measure the median HSV color inside the lamp ROI."""
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    saturation = hsv[:, :, 1]
    value = hsv[:, :, 2]

    # Ignore dark background pixels, weak reflections,
    # and heavily clipped pixels in the LED center.
    mask = (saturation >= 100) & (value >= 80) & (value <= 245)

    pixels = hsv[mask]

    if len(pixels) == 0:
      raise RuntimeError('No valid color pixels were found inside camera ROI.')

    median_hue = int(np.median(pixels[:, 0]))
    median_saturation = int(np.median(pixels[:, 1]))
    median_value = int(np.median(pixels[:, 2]))

    return median_hue, median_saturation, median_value

  def measure_roi_color(self, frame: np.ndarray) -> tuple[int, int, int]:
    """Measure HSV color of the lamp in a full camera frame."""
    return self.measure_color(self.get_roi(frame))

  def rgb_to_hsv(self, rgb: tuple[int, int, int]) -> tuple[int, int, int]:
    """Convert an RGB value to OpenCV HSV."""
    red, green, blue = rgb

    bgr = np.uint8([[[blue, green, red]]])
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)[0, 0]

    return int(hsv[0]), int(hsv[1]), int(hsv[2])

  def wait_for_rgb_color(
    self, color: str, expected_rgb: tuple[int, int, int], timeout: float = 2, interval: float = 0.2
  ) -> None:
    """Wait until the physical lamp matches the expected RGB color."""
    expected_hsv = self.rgb_to_hsv(expected_rgb)
    name = f'{color}_{expected_rgb[0]}_{expected_rgb[1]}_{expected_rgb[2]}'

    actual_hsv = None
    last_frame = None

    def color_matches() -> bool:
      nonlocal actual_hsv, last_frame

      last_frame = self.capture()
      actual_hsv = self.measure_roi_color(last_frame)

      actual_h, actual_s, actual_v = actual_hsv
      expected_h, expected_s, _ = expected_hsv

      if expected_s == 0:
        return actual_s <= WHITE_SATURATION_MAX and actual_v >= WHITE_VALUE_MIN

      return self._hue_distance(actual_h, expected_h) <= RGB_HUE_TOLERANCE

    try:
      wait_for_condition(
        color_matches,
        timeout=timeout,
        interval=interval,
        error_message=lambda: (
          f'Lamp did not reach RGB {expected_rgb}. '
          f'Expected HSV: {expected_hsv}, '
          f'actual HSV: {actual_hsv}.'
        ),
      )
    except TimeoutError:
      if last_frame is not None:
        self.save_debug_image(last_frame, f'artifacts/camera/failed/{name}_debug.jpg')
        self.save_roi(last_frame, f'artifacts/camera/failed/{name}_roi.jpg')

      raise

    self.save_roi(last_frame, f'artifacts/camera/passed/{name}_roi.jpg')

  def save_debug_image(self, frame: np.ndarray, path: str) -> None:
    """Save the full camera frame with the fixed ROI marked."""
    output = frame.copy()

    x, y, width, height = self._validated_roi(frame)

    cv2.rectangle(
      output,
      (x, y),
      (x + width, y + height),
      (255, 255, 255),
      2,
    )

    cv2.putText(
      output,
      'ROI: fixed',
      (x, max(20, y - 10)),
      cv2.FONT_HERSHEY_SIMPLEX,
      0.6,
      (255, 255, 255),
      2,
      cv2.LINE_AA,
    )

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not cv2.imwrite(str(output_path), output):
      raise RuntimeError(f'Failed to save debug image: {output_path}')

  def save_roi(self, frame: np.ndarray, path: str) -> None:
    """Save only the lamp ROI as a separate artifact."""
    roi = self.get_roi(frame)

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not cv2.imwrite(str(output_path), roi):
      raise RuntimeError(f'Failed to save ROI image: {output_path}')

  def _validated_roi(self, frame: np.ndarray) -> tuple[int, int, int, int]:
    """Validate that the configured ROI fits inside the frame."""
    x, y, width, height = CAMERA_ROI

    frame_height, frame_width = frame.shape[:2]

    if (
      x < 0
      or y < 0
      or width <= 0
      or height <= 0
      or x + width > frame_width
      or y + height > frame_height
    ):
      raise RuntimeError(
        'Configured camera ROI is outside the captured frame: '
        f'ROI={CAMERA_ROI}, '
        f'frame={frame_width}x{frame_height}'
      )

    return x, y, width, height

  @staticmethod
  def _hue_distance(first: int, second: int) -> int:
    """Calculate circular OpenCV hue distance."""
    difference = abs(first - second)

    return min(difference, 180 - difference)
