import pytest


COLOR_REFERENCES = {
  'red': (7, 244, 160),
  'green': (62, 252, 146),
  'blue': (105, 255, 145),
  'yellow': (36, 195, 153),
  'purple': (157, 147, 143),
  'cyan': (85, 249, 149),
  'white': (36, 108, 92),
}


@pytest.mark.parametrize(
  'color',
  COLOR_REFERENCES.keys(),
)
def test_calibrate_color(device, hil, color):
  device.lamp.on()
  device.lamp.set_color(color)

  # Wait until the physical LED reaches the requested color
  # before taking the calibration frame.
  hil.camera.wait_for_color(color)

  frame = hil.camera.capture_artifacts(color)
  hsv = hil.camera.measure_roi_color(frame)

  print(f'{color}: {hsv}')
  