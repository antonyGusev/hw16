class FrameworkError(Exception):
  """Base exception for all framework-specific errors."""


class DeviceError(FrameworkError):
  """Base exception for device communication errors."""


class DeviceTimeoutError(DeviceError):
  """Raised when the device does not respond within the expected time."""


class DeviceNotConnectedError(DeviceError):
  """Raised when an operation requires an open device connection."""


class ResponseParseError(FrameworkError):
  """Raised when a device response cannot be parsed."""


class UnexpectedResponseError(FrameworkError):
  """Raised when the device returns an unsupported response."""
