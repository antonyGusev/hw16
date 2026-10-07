from pathlib import Path
from typing import ClassVar

import cv2
import numpy as np
import requests


class CameraController:
  # HSV reference values measured from the real WS2812 through the HIL camera.
  # OpenCV stores Hue in the 0..179 range, not 0..360.
  COLOR_REFERENCES: ClassVar[dict[str, tuple[int, int, int]]] = {
    'red': (6, 226, 255),
    'green': (65, 228, 255),
  }

  # Allowed deviation from the calibrated HSV reference values.
  COLOR_TOLERANCE: ClassVar[dict[str, int]] = {
    'h': 5,
    's': 20,
    'v': 20,
  }

  # Dynamic ROI detection keeps only the brightest pixels, then searches for
  # a compact bright component that is likely to be the WS2812.
  BRIGHTNESS_PERCENTILE = 95
  MIN_BLOB_AREA = 50
  MAX_BLOB_AREA_RATIO = 0.1
  ROI_PADDING = 10
  # Known WS2812 location used when dynamic detection cannot find a valid blob.
  # Format: x, y, width, height.
  FALLBACK_ROI = (268, 281, 142, 137)

  def __init__(self, base_url: str, timeout: float = 5):
    self.base_url = base_url.rstrip('/')
    self.timeout = timeout
    self._roi_source = 'unknown'

  def capture(self) -> np.ndarray:
    # /capture returns a JPEG from the HIL camera web server.
    response = requests.get(f'{self.base_url}/capture', timeout=self.timeout)
    response.raise_for_status()

    image_data = np.frombuffer(response.content, dtype=np.uint8)
    frame = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

    if frame is None:
      raise RuntimeError('Failed to decode camera JPEG.')

    return frame
  
  def capture_artifacts(self, name: str) -> np.ndarray:
    # Save both the annotated full frame and the cropped ROI for every LED check.
    # Keeping this separate from capture() avoids disk writes during polling.
    frame = self.capture()

    self.save_debug_image(frame, f'artifacts/camera/{name}_debug.jpg')

    self.save_roi(frame, f'artifacts/camera/{name}_roi.jpg')

    return frame

  def detect_roi(self, frame: np.ndarray) -> tuple[int, int, int, int]:
    # Brightness is taken from HSV Value so ROI detection does not depend on LED color.
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    brightness = hsv[:, :, 2]

    # Use a percentile instead of a fixed threshold so detection adapts to
    # exposure and ambient-light changes between captures.
    threshold = np.percentile(brightness, self.BRIGHTNESS_PERCENTILE)
    mask = np.where(brightness >= threshold, 255, 0).astype(np.uint8)

    # Remove isolated bright pixels and close small gaps inside bright regions.
    kernel = np.ones((3, 3), dtype=np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    component_count, labels, stats, _ = cv2.connectedComponentsWithStats(mask)

    frame_area = frame.shape[0] * frame.shape[1]
    max_blob_area = frame_area * self.MAX_BLOB_AREA_RATIO
    candidates = []

    for label in range(1, component_count):
      x = stats[label, cv2.CC_STAT_LEFT]
      y = stats[label, cv2.CC_STAT_TOP]
      width = stats[label, cv2.CC_STAT_WIDTH]
      height = stats[label, cv2.CC_STAT_HEIGHT]
      area = stats[label, cv2.CC_STAT_AREA]

      # Reject noise and large bright surfaces that cannot be the LED.
      if area < self.MIN_BLOB_AREA or area > max_blob_area:
        continue

      component_mask = labels == label
      # Prefer components that are both bright and large enough to be stable.
      mean_brightness = float(np.mean(brightness[component_mask]))
      score = area * mean_brightness

      candidates.append((score, x, y, width, height))

    if not candidates:
      raise RuntimeError('Unable to detect WS2812 bright region.')

    _, x, y, width, height = max(candidates, key=lambda candidate: candidate[0])

    # Add context around the detected component while keeping ROI inside the frame.
    x1 = max(0, x - self.ROI_PADDING)
    y1 = max(0, y - self.ROI_PADDING)
    x2 = min(frame.shape[1], x + width + self.ROI_PADDING)
    y2 = min(frame.shape[0], y + height + self.ROI_PADDING)

    return x1, y1, x2 - x1, y2 - y1

  def resolve_roi(self, frame: np.ndarray) -> tuple[int, int, int, int]:
    # Dynamic detection is preferred; the calibrated ROI keeps diagnostics
    # available when the LED is off or the bright-region detector cannot lock on.
    try:
      roi = self.detect_roi(frame)
      self._roi_source = 'dynamic'

      return roi
    except RuntimeError:
      self._roi_source = 'fallback'

      return self._validated_fallback_roi(frame)

  @property
  def roi_source(self) -> str:
    return self._roi_source

  def get_roi(self, frame: np.ndarray) -> np.ndarray:
    x, y, width, height = self.resolve_roi(frame)
    roi = frame[y:y + height, x:x + width]

    if roi.size == 0:
      raise RuntimeError(
        f'Camera ROI is empty. ROI source: {self.roi_source}, '
        f'ROI: x={x}, y={y}, width={width}, height={height}'
      )

    return roi

  def measure_color(self, roi: np.ndarray) -> tuple[int, int, int]:
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    saturation = hsv[:, :, 1]
    value = hsv[:, :, 2]
    # Ignore dark/background pixels and low-saturation reflections.
    mask = (saturation >= 100) & (value >= 80)
    pixels = hsv[mask]

    if len(pixels) == 0:
      raise RuntimeError('No colored LED pixels found inside camera ROI.')

    # Median HSV is less sensitive to glare and individual overexposed pixels.
    median_hue = int(np.median(pixels[:, 0]))
    median_saturation = int(np.median(pixels[:, 1]))
    median_value = int(np.median(pixels[:, 2]))

    return median_hue, median_saturation, median_value

  def measure_roi_color(self, frame: np.ndarray) -> tuple[int, int, int]:
    return self.measure_color(self.get_roi(frame))

  def save_debug_image(self, frame: np.ndarray, path: str | Path) -> None:
    # Annotate the exact ROI used by color detection so failures can be inspected.
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    debug_frame = frame.copy()
    x, y, width, height = self.resolve_roi(frame)

    cv2.rectangle(
      debug_frame,
      (x, y),
      (x + width, y + height),
      (255, 255, 255),
      2,
    )

    cv2.putText(
      debug_frame,
      f'ROI: {self.roi_source}',
      (x, max(20, y - 10)),
      cv2.FONT_HERSHEY_SIMPLEX,
      0.6,
      (255, 255, 255),
      2,
    )

    cv2.imwrite(str(path), debug_frame)

  def save_roi(self, frame: np.ndarray, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    cv2.imwrite(str(path), self.get_roi(frame))

  def detect_color(self, frame: np.ndarray) -> str:
    actual_h, actual_s, actual_v = self.measure_roi_color(frame)

    for color, reference in self.COLOR_REFERENCES.items():
      expected_h, expected_s, expected_v = reference

      # Hue is circular in OpenCV HSV, so 179 and 0 are neighboring values.
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
      f'Unknown WS2812 color: H={actual_h}, S={actual_s}, V={actual_v}. '
      f'ROI source: {self.roi_source}'
    )

  def is_color(self, expected_color: str) -> bool:
    # Polling helper: an unreadable/unknown color means the expected color
    # has not been reached yet, not that the polling loop itself should fail.
    try:
      return self.detect_color(self.capture()) == expected_color
    except RuntimeError:
      return False

  def _validated_fallback_roi(self, frame: np.ndarray) -> tuple[int, int, int, int]:
    x, y, width, height = self.FALLBACK_ROI

    if x >= frame.shape[1] or y >= frame.shape[0]:
      raise RuntimeError(
        f'Fallback ROI is outside camera frame: x={x}, y={y}, '
        f'width={width}, height={height}'
      )

    # Clip the configured ROI when camera resolution changes slightly.
    width = min(width, frame.shape[1] - x)
    height = min(height, frame.shape[0] - y)

    if width <= 0 or height <= 0:
      raise RuntimeError('Fallback camera ROI is empty.')

    return x, y, width, height

  @staticmethod
  def _hue_distance(actual: int, expected: int) -> int:
    # OpenCV Hue wraps after 179, therefore use the shortest circular distance.
    difference = abs(actual - expected)

    return min(difference, 180 - difference)
