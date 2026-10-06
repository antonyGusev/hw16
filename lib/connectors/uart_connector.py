import re
import time
from typing import TypeAlias

import serial

from ..utilities import DeviceNotConnectedError, DeviceTimeoutError

ResponsePattern: TypeAlias = str | tuple[str, ...]


class UARTConnector:
  BAUD_RATE = 115200
  BYTE_SIZE = serial.EIGHTBITS
  PARITY = serial.PARITY_NONE
  STOP_BITS = serial.STOPBITS_ONE

  # A period without serial data that marks the end of a regular response.
  RESPONSE_IDLE_TIMEOUT = 0.1

  ANSI_PATTERN = re.compile(r'\x1b\[[0-9;]*[mK]')

  def __init__(self, port: str, timeout: float = 2):
    self.port = port
    self.timeout = timeout
    self.ser: serial.Serial | None = None

  def open(self) -> None:
    self.ser = serial.Serial(
      port=self.port,
      baudrate=self.BAUD_RATE,
      bytesize=self.BYTE_SIZE,
      parity=self.PARITY,
      stopbits=self.STOP_BITS,
      timeout=self.RESPONSE_IDLE_TIMEOUT,
    )

    self.ser.reset_input_buffer()

  def close(self) -> None:
    if self.ser is not None and self.ser.is_open:
      self.ser.close()

    self.ser = None

  # Send a command without waiting for a response.
  def write_command(self, command: str) -> None:
    self._ensure_open()

    command = command.rstrip('\r\n') + '\r\n'

    self.ser.write(command.encode('utf-8'))
    self.ser.flush()

  # Send a command and collect its response.
  def execute_command(
    self,
    command: str,
    timeout: float | None = None,
    until: ResponsePattern | None = None,
  ) -> list[str]:
    self.write_command(command)

    return self._read_response(
      self.timeout if timeout is None else timeout,
      until,
    )

  # Wait for one of the expected patterns and return all lines received while waiting.
  def wait_for_response(self, pattern: ResponsePattern, timeout: float) -> list[str]:
    return self._read_response(timeout, pattern)

  # region Service methods

  # Read and collect response lines.
  #
  # Without an expected pattern, the first RESPONSE_IDLE_TIMEOUT period without data
  # marks the end of the response.
  #
  # With an expected pattern, temporary gaps in the serial output are ignored
  # and reading continues until the pattern is received or the overall timeout expires.
  def _read_response(
    self,
    timeout: float,
    until: ResponsePattern | None = None,
  ) -> list[str]:
    self._ensure_open()

    lines: list[str] = []
    patterns = (until,) if isinstance(until, str) else until
    deadline = time.monotonic() + timeout

    while time.monotonic() < deadline:
      line = self._read_line()

      if line is None:
        # Once a regular response has started, a period without
        # new data marks the end of that response.
        if patterns is None and lines:
          return lines

        continue

      lines.append(line)

      if patterns is not None and any(pattern in line for pattern in patterns):
        return lines

    if patterns is not None:
      raise DeviceTimeoutError(
        f'Expected response {patterns} was not received within {timeout}s. '
        f'Received: {lines}'
      )

    return lines

  # Ensure that serial operations are performed only on an open connection.
  def _ensure_open(self) -> None:
    if self.ser is None or not self.ser.is_open:
      raise DeviceNotConnectedError('Serial port is not open. Call open() before reading data.')

  # Read a single line using the idle timeout configured in pyserial.
  def _read_line(self) -> str | None:
    self._ensure_open()

    raw_line = self.ser.readline()

    if not raw_line:
      return None

    return self._clean_line(raw_line)

  # Decode raw serial bytes, remove ANSI escape sequences
  # and ignore empty lines.
  def _clean_line(self, raw_line: bytes) -> str | None:
    line = raw_line.decode('utf-8', errors='replace')
    line = self.ANSI_PATTERN.sub('', line).rstrip('\r\n')

    return line if line else None

  # endregion
