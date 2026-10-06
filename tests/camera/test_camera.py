def test_camera_capture(camera):
  frame = camera.capture()

  assert frame is not None
  assert frame.size > 0


def test_ws2812_color_measurement(camera):
  frame = camera.capture()

  camera.save_debug_image(
    frame,
    'artifacts/camera/ws2812_debug.jpg',
  )

  camera.save_roi(
    frame,
    'artifacts/camera/ws2812_roi.jpg',
  )

  hue, saturation, value = camera.measure_roi_color(frame)

  print(
    f'\nWS2812 HSV: '
    f'H={hue}, S={saturation}, V={value}'
  )
  