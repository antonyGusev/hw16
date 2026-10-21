import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import cv2
import numpy as np

from .base_camera_module import BaseCameraModule

VIDEO_FPS = 15

SOLID_DURATION = 2.5
SOLID_STABILIZATION_TIME = 0.5
SOLID_REFERENCE_FRAMES = 5
SOLID_HUE_TOLERANCE = 10
SOLID_SATURATION_TOLERANCE = 30
SOLID_WHITE_SATURATION_MAX = 120

BLINK_DURATION = 3.0
BLINK_EXPECTED_HALF_PERIOD = 0.5
BLINK_PERIOD_TOLERANCE = 0.2
BLINK_MIN_TRANSITIONS = 4

BREATHE_DURATION = 7.0
BREATHE_EXPECTED_PERIOD = 3.0
BREATHE_PERIOD_TOLERANCE = 0.8
BREATHE_MIN_AMPLITUDE_RATIO = 0.05
BREATHE_MIN_SAMPLES = 10
BREATHE_SMOOTHING_WINDOW = 7

RAINBOW_DURATION = 12.0
RAINBOW_MIN_SAMPLES = 30
RAINBOW_MIN_HUE_SECTORS = 5
RAINBOW_MIN_HUE_PROGRESS = 150
RAINBOW_MAX_REVERSE_RATIO = 0.2

VideoMeasurement = Literal['max_brightness']


@dataclass(frozen=True)
class VerificationConfig:
  duration: float
  stabilization_time: float = 0


@dataclass
class VideoObservation:
  frames: list[np.ndarray]
  timestamps: list[float]


VideoCheck = Literal[
  'solid',
  'stable_color',
  'blink',
  'breathe',
  'rainbow',
]


VERIFICATION_CONFIGS: dict[VideoCheck, VerificationConfig] = {
  'solid': VerificationConfig(SOLID_DURATION, SOLID_STABILIZATION_TIME),
  'stable_color': VerificationConfig(SOLID_DURATION, SOLID_STABILIZATION_TIME),
  'blink': VerificationConfig(BLINK_DURATION),
  'breathe': VerificationConfig(BREATHE_DURATION),
  'rainbow': VerificationConfig(RAINBOW_DURATION),
}


class VideoModule(BaseCameraModule):
  """Camera controller for temporal lamp validation."""

  def open_stream(self) -> cv2.VideoCapture:
    """Open the current MJPEG camera stream."""
    stream = cv2.VideoCapture(self._endpoints.stream_url)

    if not stream.isOpened():
      stream.release()
      raise RuntimeError(f'Failed to open camera stream: {self._endpoints.stream_url}')

    return stream

  def verify(self, check: VideoCheck, name: str | None = None) -> None:
    """Run the requested temporal camera verification."""
    config = VERIFICATION_CONFIGS[check]

    validators: dict[VideoCheck, Callable[[VideoObservation], None]] = {
      'solid': self._validate_stable_color,
      'stable_color': self._validate_stable_color,
      'blink': self._validate_blink,
      'breathe': self._validate_breathe,
      'rainbow': self._validate_rainbow,
    }

    artifact_name = name or f'mode_{check}'
    observation = self._collect_observation(
      duration=config.duration,
      stabilization_time=config.stabilization_time,
    )

    try:
      validators[check](observation)
    except AssertionError:
      self._save_video(observation.frames, f'artifacts/camera/failed/{artifact_name}.mp4')
      raise

    self._save_video(observation.frames, f'artifacts/camera/passed/{artifact_name}.mp4')
    
  def measure(self, measurement: VideoMeasurement, duration: float) -> float:
    """Measure the requested temporal lamp property."""
    if measurement == 'max_brightness':
      return self._measure_max_brightness(duration)

    raise ValueError(f'Unsupported video measurement: {measurement}')

  # region Service methods

  def _validate_stable_color(self, observation: VideoObservation) -> None:
    """Verify that the physical lamp color remains stable."""
    hsv_samples = np.array([self.measure_roi_color(frame) for frame in observation.frames])

    if len(hsv_samples) <= SOLID_REFERENCE_FRAMES:
      raise AssertionError(
        f'Not enough camera samples for stable color validation: {len(hsv_samples)}.'
      )

    reference_hsv = tuple(
      int(value)
      for value in np.median(
        hsv_samples[:SOLID_REFERENCE_FRAMES],
        axis=0,
      )
    )

    reference_h, reference_s, _ = reference_hsv

    for actual_h, actual_s, actual_v in hsv_samples[SOLID_REFERENCE_FRAMES:]:
      if reference_s <= SOLID_WHITE_SATURATION_MAX:
        matches = abs(actual_s - reference_s) <= SOLID_SATURATION_TOLERANCE
      else:
        matches = self._hue_distance(actual_h, reference_h) <= SOLID_HUE_TOLERANCE

      if not matches:
        raise AssertionError(
          f'Lamp color changed during observation. '
          f'Reference HSV: {reference_hsv}, '
          f'actual HSV: {(actual_h, actual_s, actual_v)}.'
        )

  def _validate_blink(self, observation: VideoObservation) -> None:
    """Verify approximately 1 Hz blinking."""
    intensities = np.array([self.measure_roi_intensity(frame) for frame in observation.frames])

    low = float(np.percentile(intensities, 20))
    high = float(np.percentile(intensities, 80))
    threshold = (low + high) / 2

    states = intensities >= threshold

    transitions = [
      observation.timestamps[index]
      for index in range(1, len(states))
      if states[index] != states[index - 1]
    ]

    if len(transitions) < BLINK_MIN_TRANSITIONS:
      raise AssertionError(
        f'Not enough blink transitions. '
        f'Expected at least {BLINK_MIN_TRANSITIONS}, '
        f'actual: {len(transitions)}.'
      )

    half_periods = np.diff(transitions)

    if any(
      abs(period - BLINK_EXPECTED_HALF_PERIOD) > BLINK_PERIOD_TOLERANCE for period in half_periods
    ):
      raise AssertionError(
        f'Invalid blink timing. '
        f'Expected half-period: '
        f'{BLINK_EXPECTED_HALF_PERIOD}s ± {BLINK_PERIOD_TOLERANCE}s, '
        f'actual: {half_periods.tolist()}.'
      )

  def _validate_breathe(self, observation: VideoObservation) -> None:
    """Verify smooth brightness pulsing with an approximately 3-second period."""
    intensities = np.array([self.measure_roi_intensity(frame) for frame in observation.frames])

    if len(intensities) < BREATHE_MIN_SAMPLES:
      raise AssertionError(f'Not enough camera samples for breathe validation: {len(intensities)}.')

    window = min(BREATHE_SMOOTHING_WINDOW, len(intensities))

    if window % 2 == 0:
      window -= 1

    kernel = np.ones(window) / window
    smoothed = np.convolve(intensities, kernel, mode='same')

    low = float(np.percentile(smoothed, 10))
    high = float(np.percentile(smoothed, 90))

    amplitude = high - low
    amplitude_ratio = amplitude / high if high > 0 else 0

    if amplitude_ratio < BREATHE_MIN_AMPLITUDE_RATIO:
      raise AssertionError(
        f'Breathe amplitude is too small. '
        f'Expected at least {BREATHE_MIN_AMPLITUDE_RATIO:.0%}, '
        f'actual: {amplitude_ratio:.1%} '
        f'({low:.1f}..{high:.1f}).'
      )

    low_threshold = low + amplitude * 0.35
    high_threshold = low + amplitude * 0.65

    rising_transitions = []
    waiting_for_high = False

    for timestamp, intensity in zip(observation.timestamps, smoothed):
      if intensity <= low_threshold:
        waiting_for_high = True
        continue

      if waiting_for_high and intensity >= high_threshold:
        rising_transitions.append(timestamp)
        waiting_for_high = False

    periods = np.diff(rising_transitions)

    if not any(
      abs(period - BREATHE_EXPECTED_PERIOD) <= BREATHE_PERIOD_TOLERANCE
      for period in periods
    ):
      raise AssertionError(
        f'Invalid breathe period. '
        f'Expected: {BREATHE_EXPECTED_PERIOD}s ± '
        f'{BREATHE_PERIOD_TOLERANCE}s, '
        f'actual: {periods.tolist()}.'
      )

  def _validate_rainbow(self, observation: VideoObservation) -> None:
    """Verify continuous hue cycling in one direction across the color wheel."""
    hues = []

    for frame in observation.frames:
      try:
        hue, _, _ = self.measure_roi_color(frame)
      except RuntimeError as error:
        if 'No valid color pixels' not in str(error):
          raise
        continue

      hues.append(hue)

    if len(hues) < RAINBOW_MIN_SAMPLES:
      raise AssertionError(
        f'Not enough chromatic camera samples for rainbow validation. '
        f'Expected at least {RAINBOW_MIN_SAMPLES}, actual: {len(hues)}.'
      )

    # OpenCV hue wraps at 180; map consecutive differences into [-90, 90).
    # This preserves the direction when the hue crosses from red to red.
    differences = (np.diff(np.asarray(hues, dtype=float)) + 90) % 180 - 90
    forward = float(np.sum(np.maximum(differences, 0)))
    backward = float(np.sum(np.maximum(-differences, 0)))
    progress = forward - backward
    sectors = {hue // 30 for hue in hues}

    if (
      len(sectors) < RAINBOW_MIN_HUE_SECTORS
      or abs(progress) < RAINBOW_MIN_HUE_PROGRESS
      or min(forward, backward) > max(forward, backward) * RAINBOW_MAX_REVERSE_RATIO
    ):
      raise AssertionError(
        f'Invalid rainbow color cycling. '
        f'Expected at least {RAINBOW_MIN_HUE_SECTORS} hue sectors, '
        f'{RAINBOW_MIN_HUE_PROGRESS} degrees of net hue progress '
        f'and no more than {RAINBOW_MAX_REVERSE_RATIO:.0%} reverse motion. '
        f'Actual: {len(sectors)} sectors, net progress {progress:.1f}, '
        f'forward {forward:.1f}, backward {backward:.1f}; '
        f'sectors: {sorted(sectors)}.'
      )

  def _collect_observation(
    self, duration: float, stabilization_time: float = 0
  ) -> VideoObservation:
    """Collect camera frames and their timestamps."""
    stream = self.open_stream()

    frames = []
    timestamps = []

    try:
      started_at = time.monotonic()

      while time.monotonic() - started_at < stabilization_time:
        self._read_frame(stream)

      started_at = time.monotonic()

      while time.monotonic() - started_at < duration:
        frames.append(self._read_frame(stream))
        timestamps.append(time.monotonic() - started_at)

    finally:
      stream.release()

    return VideoObservation(
      frames=frames,
      timestamps=timestamps,
    )
    
  def _measure_max_brightness(self, duration: float) -> float:
    """Measure the maximum active brightness during an observation."""
    observation = self._collect_observation(duration)
    intensities = np.array([self.measure_roi_intensity(frame) for frame in observation.frames])

    return float(np.percentile(intensities, 90))

  @staticmethod
  def _read_frame(stream: cv2.VideoCapture) -> np.ndarray:
    """Read and validate a single stream frame."""
    success, frame = stream.read()

    if not success or frame is None:
      raise RuntimeError('Failed to read frame from camera stream.')

    return frame.copy()

  def _save_video(self, frames: list[np.ndarray], path: str) -> None:
    """Save captured frames as an MP4 artifact."""
    if not frames:
      raise RuntimeError('No camera frames were captured for video artifact.')

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    height, width = frames[0].shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(str(output_path), fourcc, VIDEO_FPS, (width, height))

    if not writer.isOpened():
      raise RuntimeError(f'Failed to create video artifact: {output_path}')

    try:
      for frame in frames:
        writer.write(frame)
    finally:
      writer.release()

  # endregion
