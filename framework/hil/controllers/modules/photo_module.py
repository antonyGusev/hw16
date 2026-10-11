import cv2
import numpy as np
import requests

from lib import wait_for_condition

from .base_camera_module import BaseCameraModule


class PhotoModule(BaseCameraModule):
  """Camera controller for single-frame capture and static color validation."""

  def capture(self) -> np.ndarray:
    """Capture and decode a single frame from the camera snapshot endpoint."""
    # Request the latest JPEG frame from the HIL camera.
    response = requests.get(self._endpoints.capture_url, timeout=self.timeout)
    response.raise_for_status()

    # Convert raw response bytes into an OpenCV-compatible image buffer.
    image = np.frombuffer(response.content, dtype=np.uint8)

    # Decode the JPEG buffer into a BGR OpenCV frame.
    frame = cv2.imdecode(image, cv2.IMREAD_COLOR)

    if frame is None:
      raise RuntimeError('Failed to decode camera frame.')

    return frame

  def capture_artifacts(self, name: str) -> np.ndarray:
    """Capture a frame and save both full-frame and ROI debug artifacts."""
    frame = self.capture()

    # Save the full frame with the ROI marked for easier debugging.
    self.save_debug_image(frame, f'artifacts/camera/{name}_debug.jpg')

    # Save only the analyzed lamp ROI as a separate artifact.
    self.save_roi(frame, f'artifacts/camera/{name}_roi.jpg')

    return frame

  def wait_for_rgb_color(
    self, color: str, expected_rgb: tuple[int, int, int], timeout: float = 2, interval: float = 0.2
  ) -> None:
    """Wait until the physical lamp matches the expected RGB color."""
    # Convert expected RGB once so it can be included in the failure message.
    expected_hsv = self.rgb_to_hsv(expected_rgb)

    # Include both logical color name and RGB values in artifact filenames.
    name = f'{color}_{expected_rgb[0]}_{expected_rgb[1]}_{expected_rgb[2]}'

    actual_hsv = None
    last_frame = None

    def color_matches() -> bool:
      nonlocal actual_hsv, last_frame

      # Capture a fresh frame on every polling attempt.
      last_frame = self.capture()

      # Measure the current physical lamp color inside the configured ROI.
      actual_hsv = self.measure_roi_color(last_frame)

      # Compare the measured color against the expected RGB value.
      return self._matches_rgb(actual_hsv, expected_rgb)

    try:
      # Poll until the expected color is detected or the timeout expires.
      wait_for_condition(
        color_matches,
        timeout=timeout,
        interval=interval,
        error_message=lambda: (
          f'Lamp did not reach RGB {expected_rgb}. '
          f'Expected HSV: {expected_hsv}, actual HSV: {actual_hsv}.'
        ),
      )
    except TimeoutError:
      # Preserve the last observed frame when validation fails.
      if last_frame is not None:
        self.save_debug_image(last_frame, f'artifacts/camera/failed/{name}_debug.jpg')
        self.save_roi(last_frame, f'artifacts/camera/failed/{name}_roi.jpg')

      raise

    # Save the successfully validated ROI for the test report.
    self.save_roi(last_frame, f'artifacts/camera/passed/{name}_roi.jpg')
