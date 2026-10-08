from pathlib import Path
from typing import ClassVar

import cv2
import numpy as np
import requests

from lib import wait_for_condition


class CameraController:
  # Calibrated HSV values for each supported lamp color.
  # These values are specific to the current camera position,
  # exposure settings, lamp brightness, and physical test stand.
  COLOR_REFERENCES: ClassVar[dict[str, tuple[int, int, int]]] = {
    'red': (7, 244, 160),
    'green': (62, 252, 146),
    'blue': (105, 255, 145),
    'yellow': (36, 195, 153),
    'purple': (157, 147, 143),
    'cyan': (85, 249, 149),
    'white': (94, 104, 229),
  }

  # Maximum allowed difference between the measured HSV value
  # and the calibrated reference value.
  COLOR_TOLERANCE: ClassVar[dict[str, int]] = {
    'h': 5,
    's': 20,
    'v': 20,
  }

  # Fixed ROI containing the WS2812 LED.
  # Format: (x, y, width, height).
  ROI = (280, 355, 75, 75)

  def __init__(self, capture_url: str, timeout: float = 5):
    # Full camera capture endpoint, for example:
    # http://192.168.68.104/capture
    self.capture_url = capture_url
    self.timeout = timeout

  def capture(self) -> np.ndarray:
    """Capture a single frame from the HIL camera."""
    response = requests.get(self.capture_url, timeout=self.timeout)

    response.raise_for_status()

    image = np.frombuffer(response.content, dtype=np.uint8)

    frame = cv2.imdecode(image, cv2.IMREAD_COLOR)

    if frame is None:
      raise RuntimeError('Failed to decode camera frame.')

    return frame

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
    roi = self.get_roi(frame)

    return self.measure_color(roi)

  def detect_color(self, frame: np.ndarray) -> str:
    """Return the calibrated color name matching the camera frame."""
    actual_h, actual_s, actual_v = self.measure_roi_color(frame)

    matches = []

    for color, reference in self.COLOR_REFERENCES.items():
      expected_h, expected_s, expected_v = reference

      hue_difference = self._hue_distance(actual_h, expected_h)

      saturation_difference = abs(actual_s - expected_s)

      value_difference = abs(actual_v - expected_v)

      if (
        hue_difference <= self.COLOR_TOLERANCE['h']
        and saturation_difference <= self.COLOR_TOLERANCE['s']
        and value_difference <= self.COLOR_TOLERANCE['v']
      ):
        # Use the total HSV distance when more than one
        # reference happens to fall inside the tolerance.
        score = hue_difference + saturation_difference + value_difference

        matches.append((score, color))

    if not matches:
      raise RuntimeError(
        'Unable to match measured color '
        f'HSV({actual_h}, {actual_s}, {actual_v}) '
        'to any calibrated lamp color.'
      )

    _, color = min(matches, key=lambda match: match[0])

    return color

  def is_color(self, expected: str) -> bool:
    """Check whether the physical lamp matches the expected color."""
    if expected not in self.COLOR_REFERENCES:
      raise ValueError(f'Unsupported camera color: {expected}')

    try:
      actual = self.detect_color(self.capture())
    except RuntimeError:
      return False

    return actual == expected
  
  def wait_for_color(
    self,
    expected: str,
    timeout: float = 2,
    interval: float = 0.2,
  ) -> None:
    """Wait until the physical lamp reaches the expected color."""
    if expected not in self.COLOR_REFERENCES:
      raise ValueError(
        f'Unsupported camera color: {expected}'
      )

    expected_hsv = self.COLOR_REFERENCES[expected]
    actual_hsv = None

    def color_matches() -> bool:
      nonlocal actual_hsv

      frame = self.capture()
      actual_hsv = self.measure_roi_color(frame)

      actual_h, actual_s, actual_v = actual_hsv
      expected_h, expected_s, expected_v = expected_hsv

      return (
        self._hue_distance(actual_h, expected_h)
        <= self.COLOR_TOLERANCE['h']
        and abs(actual_s - expected_s)
        <= self.COLOR_TOLERANCE['s']
        and abs(actual_v - expected_v)
        <= self.COLOR_TOLERANCE['v']
      )

    wait_for_condition(
      color_matches,
      timeout=timeout,
      interval=interval,
      error_message=lambda: (
        f'Lamp did not become {expected}. '
        f'Expected HSV: {expected_hsv}, '
        f'actual HSV: {actual_hsv}.'
      ),
    )

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
    x, y, width, height = self.ROI

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
        f'ROI={self.ROI}, '
        f'frame={frame_width}x{frame_height}'
      )

    return x, y, width, height

  @staticmethod
  def _hue_distance(first: int, second: int) -> int:
    """Calculate circular OpenCV hue distance."""
    difference = abs(first - second)

    return min(difference, 180 - difference)
