from abc import ABC
from pathlib import Path

import cv2
import numpy as np

# Maximum allowed hue difference for chromatic color validation.
RGB_HUE_TOLERANCE = 20

# White has no meaningful hue, so it is validated by saturation and brightness.
WHITE_SATURATION_MAX = 120
WHITE_VALUE_MIN = 180

# Black is validated by low brightness because hue and saturation are meaningless.
BLACK_VALUE_MAX = 50

# Fixed camera ROI containing the physical lamp.
CAMERA_ROI = (280, 355, 75, 75)


class BaseCameraModule(ABC):
  """Base camera functionality shared by photo and video modules."""

  def __init__(self, endpoints, timeout: float = 5):
    # Keep the same mutable endpoints object used by CameraController.
    # If HIL refreshes camera URLs, derived modules automatically use them.
    self._endpoints = endpoints
    self.timeout = timeout

  def get_roi(self, frame: np.ndarray) -> np.ndarray:
    """Extract the configured lamp ROI from the camera frame."""
    x, y, width, height = self._validated_roi(frame)

    return frame[
      y : y + height,
      x : x + width,
    ]

  def measure_color(self, roi: np.ndarray) -> tuple[int, int, int]:
    """Measure the median HSV color of valid lamp pixels inside the ROI."""
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    saturation = hsv[:, :, 1]
    value = hsv[:, :, 2]

    # Ignore weakly saturated background pixels, dark pixels,
    # and heavily clipped bright pixels from the LED center.
    mask = (saturation >= 100) & (value >= 80) & (value <= 245)
    pixels = hsv[mask]

    if len(pixels) == 0:
      raise RuntimeError('No valid color pixels were found inside camera ROI.')

    # Median is less sensitive to reflections and individual noisy pixels.
    return (
      int(np.median(pixels[:, 0])),
      int(np.median(pixels[:, 1])),
      int(np.median(pixels[:, 2])),
    )
    
  def measure_white(self, image: np.ndarray) -> tuple[int, int, int]:
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    value = hsv[:, :, 2]
    mask = value >= WHITE_VALUE_MIN

    pixels = hsv[mask]

    if pixels.size == 0:
      return 0, 0, 0

    return tuple(int(value) for value in np.median(pixels, axis=0))

  def measure_roi_color(self, frame: np.ndarray) -> tuple[int, int, int]:
    """Measure the lamp HSV color directly from a full camera frame."""
    return self.measure_color(self.get_roi(frame))
  
  def measure_roi_white(self, frame: np.ndarray) -> tuple[int, int, int]:
    return self.measure_white(self.get_roi(frame))

  def measure_roi_intensity(self, frame: np.ndarray) -> float:
    """Measure the median brightness of the lamp ROI."""
    roi = self.get_roi(frame)
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # The V channel represents brightness in HSV.
    return float(np.median(hsv[:, :, 2]))

  def rgb_to_hsv(self, rgb: tuple[int, int, int]) -> tuple[int, int, int]:
    """Convert an RGB value to OpenCV HSV representation."""
    red, green, blue = rgb

    # OpenCV expects BGR input rather than RGB.
    bgr = np.uint8([[[blue, green, red]]])
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)[0, 0]

    return int(hsv[0]), int(hsv[1]), int(hsv[2])

  def save_debug_image(self, frame: np.ndarray, path: str) -> None:
    """Save a full camera frame with the configured ROI highlighted."""
    output = frame.copy()

    x, y, width, height = self._validated_roi(frame)

    # Draw the ROI used for physical lamp analysis.
    cv2.rectangle(output, (x, y), (x + width, y + height), (255, 255, 255), 2)

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

    # Create artifact directories automatically when needed.
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not cv2.imwrite(str(output_path), output):
      raise RuntimeError(f'Failed to save debug image: {output_path}')

  def save_roi(self, frame: np.ndarray, path: str) -> None:
    """Save only the analyzed lamp ROI as an artifact."""
    roi = self.get_roi(frame)

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not cv2.imwrite(str(output_path), roi):
      raise RuntimeError(f'Failed to save ROI image: {output_path}')
    
  # region Service methods

  def _matches_rgb(self, actual_hsv: tuple[int, int, int], expected_rgb: tuple[int, int, int]) -> bool:
    """Check whether the measured lamp color matches the expected RGB value."""
    expected_hsv = self.rgb_to_hsv(expected_rgb)

    actual_h, actual_s, actual_v = actual_hsv
    expected_h, expected_s, expected_v = expected_hsv

    # Hue and saturation are undefined for black, so validate it
    # only by sufficiently low physical brightness.
    if expected_v == 0:
      return actual_v <= BLACK_VALUE_MAX

    # Hue is undefined for white, so validate it by low saturation
    # and sufficient brightness instead.
    if expected_s == 0:
      return actual_s <= WHITE_SATURATION_MAX and actual_v >= WHITE_VALUE_MIN

    # Camera exposure can strongly affect saturation and brightness,
    # therefore chromatic colors are validated primarily by hue.
    return self._hue_distance(actual_h, expected_h) <= RGB_HUE_TOLERANCE

  def _validated_roi(self, frame: np.ndarray) -> tuple[int, int, int, int]:
    """Validate that the configured ROI fits completely inside the frame."""
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
        f'ROI={CAMERA_ROI}, frame={frame_width}x{frame_height}'
      )

    return x, y, width, height

  @staticmethod
  def _hue_distance(first: int, second: int) -> int:
    """Calculate circular distance between two OpenCV hue values."""
    difference = abs(first - second)

    # OpenCV hue wraps around at 180, so 179 and 1 are close to each other.
    return min(difference, 180 - difference)
  
  # endregion
