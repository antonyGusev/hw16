import itertools
from typing import Literal

import cv2
import numpy as np
import requests

from lib import wait_for_condition

from .base_camera_module import BaseCameraModule

PhotoCheck = Literal['rgb', 'brightness']
PhotoMeasurement = Literal['brightness']

BRIGHTNESS_SAMPLES = 5


class PhotoModule(BaseCameraModule):
  """Camera module for static image verification and measurements."""

  def capture(self) -> np.ndarray:
    """Capture and decode a single frame from the camera."""
    response = requests.get(self._endpoints.capture_url, timeout=self.timeout)
    response.raise_for_status()

    image = np.frombuffer(response.content, dtype=np.uint8)
    frame = cv2.imdecode(image, cv2.IMREAD_COLOR)

    if frame is None:
      raise RuntimeError('Failed to decode camera frame.')

    return frame

  def verify(
    self,
    check: PhotoCheck,
    name: str,
    expected_rgb: tuple[int, int, int] | None = None,
    brightness_levels: dict[int, float] | None = None,
  ) -> None:
    """Run the requested static camera verification."""
    if check == 'rgb':
      if expected_rgb is None:
        raise ValueError('expected_rgb is required for RGB verification.')

      self._validate_rgb(name, expected_rgb)
      return

    if check == 'brightness':
      if brightness_levels is None:
        raise ValueError('brightness_levels are required for brightness verification.')

      self._validate_brightness(brightness_levels)
      return

    raise ValueError(f'Unsupported photo verification: {check}')

  def measure(self, measurement: PhotoMeasurement) -> float:
    """Measure the requested physical lamp property."""
    if measurement == 'brightness':
      return self._measure_brightness()

    raise ValueError(f'Unsupported photo measurement: {measurement}')
  
  # region Service methods

  def _validate_rgb(
    self, name: str, expected_rgb: tuple[int, int, int], timeout: float = 2, interval: float = 0.2
  ) -> None:
    """Wait until the physical lamp matches the expected RGB color."""
    expected_hsv = self.rgb_to_hsv(expected_rgb)
    artifact_name = f'{name}_{expected_rgb[0]}_{expected_rgb[1]}_{expected_rgb[2]}'

    actual_hsv = None
    last_frame = None

    def color_matches() -> bool:
      nonlocal actual_hsv, last_frame

      last_frame = self.capture()

      if expected_rgb == (255, 255, 255):
        # White requires a dedicated measurement because the regular color mask
        # intentionally ignores low-saturation pixels.
        actual_hsv = self.measure_roi_white(last_frame)
      elif expected_rgb == (0, 0, 0):
        # Black has no useful hue or saturation, so use physical ROI brightness
        # as the HSV value component for validation.
        actual_hsv = (0, 0, int(self.measure_roi_intensity(last_frame)))
      else:
        actual_hsv = self.measure_roi_color(last_frame)

      return self._matches_rgb(actual_hsv, expected_rgb)

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
        self.save_debug_image(last_frame, f'artifacts/camera/failed/{artifact_name}_debug.jpg')
        self.save_roi(last_frame, f'artifacts/camera/failed/{artifact_name}_roi.jpg')

      raise

    self.save_roi(last_frame, f'artifacts/camera/passed/{artifact_name}_roi.jpg')

  def _validate_brightness(self, brightness_levels: dict[int, float]) -> None:
    """Verify that physical lamp brightness increases with configured brightness."""
    if len(brightness_levels) < 2:
      raise ValueError('At least two brightness levels are required for validation.')

    ordered_levels = sorted(brightness_levels.items())

    for (previous_level, previous_value), (current_level, current_value) in itertools.pairwise(
      ordered_levels
    ):
      if previous_value >= current_value:
        raise AssertionError(
          f'Physical brightness does not increase with configured brightness. '
          f'{previous_level}%={previous_value:.1f}, '
          f'{current_level}%={current_value:.1f}. '
          f'All measurements: {brightness_levels}.'
        )

  def _measure_brightness(self) -> float:
    """Measure median physical brightness using several camera frames."""
    samples = [self.measure_roi_intensity(self.capture()) for _ in range(BRIGHTNESS_SAMPLES)]

    return float(np.median(samples))
  
  # endregion
