import re
from dataclasses import dataclass

from lib import DeviceDriver, ResponseParseError, UnexpectedResponseError


@dataclass
class WifiNetwork:
  ssid: str
  rssi: int
  channel: int


@dataclass
class WifiStatus:
  connected: bool
  ssid: str | None
  ip: str | None
  rssi: int | None


@dataclass
class WifiConnectResult:
  connected: bool
  error: str | None
  response: list[str]


class WifiModule:
  def __init__(self, driver: DeviceDriver):
    self._driver = driver

  def scan(self) -> list[WifiNetwork]:
    # Firmware reports the number of discovered networks before printing the AP list.
    # Use that count as the completion condition instead of waiting for a fixed timeout.
    response = self._driver.execute_command('scan', until='networks:', timeout=10)
    network_count = self._parse_network_count(response)

    if network_count == 0:
      return []

    # The first read stops on the count line. Continue until the indexed record for
    # the last reported network is received. Single-digit indexes are padded by firmware.
    last_network_pattern = f'[{network_count:2d}]'
    response.extend(self._driver.wait_for_response(last_network_pattern, timeout=5))

    return self._parse_networks(response)

  def connect(
    self,
    ssid: str | int | None = None,
    password: str | None = None,
  ) -> WifiConnectResult:
    self._driver.write_command('connect')
    self._driver.wait_for_response('Enter SSID', timeout=10)

    if ssid is None:
      self._driver.write_command('')

      response = self._driver.wait_for_response(
        (
          'successfully connected to SSID:',
          'connect to the AP fail',
        ),
        timeout=15,
      )

      return self._parse_connect_result(response)

    self._driver.write_command(str(ssid))
    self._driver.wait_for_response('Enter password:', timeout=5)
    self._driver.write_command(password or '')

    response = self._driver.wait_for_response(
      (
        'successfully connected to SSID:',
        'password too short',
        'connect to the AP fail',
        'connection timeout',
      ),
      timeout=15,
    )

    return self._parse_connect_result(response)

  def status(self) -> WifiStatus:
    # Wait until firmware returns either the disconnected state
    # or the last field of the connected state.
    response = self._driver.execute_command(
      'status',
      until=(
        'WiFi: disconnected',
        'RSSI:',
      ),
      timeout=5,
    )

    return self._parse_status(response)

  def disconnect(self) -> bool:
    # Wait until firmware confirms that the station
    # has been successfully disconnected from the access point.
    response = self._driver.execute_command(
      'disconnect',
      until='wifi station: disconnected',
      timeout=5,
    )

    return any('wifi station: disconnected' in line for line in response)

  # region Service Methods

  def _parse_network_count(self, response: list[str]) -> int:
    for line in response:
      match = re.search(r'found\s+(\d+)\s+networks:', line)

      if match:
        return int(match.group(1))

    raise ResponseParseError(f'WiFi scan network count was not found in response: {response}')

  def _parse_networks(self, response: list[str]) -> list[WifiNetwork]:
    networks: list[WifiNetwork] = []

    for line in response:
      if 'SSID:' not in line or 'RSSI:' not in line or 'CH:' not in line:
        continue

      ssid = line.split('SSID:', 1)[1].split('RSSI:', 1)[0].strip()
      rssi = line.split('RSSI:', 1)[1].split('dBm', 1)[0].strip()
      channel = line.split('CH:', 1)[1].strip()

      networks.append(
        WifiNetwork(
          ssid=ssid,
          rssi=int(rssi),
          channel=int(channel),
        )
      )

    return networks

  def _parse_connect_result(self, response: list[str]) -> WifiConnectResult:
    if any('successfully connected to SSID:' in line for line in response):
      return WifiConnectResult(
        connected=True,
        error=None,
        response=response,
      )

    if any('password too short' in line for line in response):
      return WifiConnectResult(
        connected=False,
        error='password_too_short',
        response=response,
      )

    if any('connect to the AP fail' in line for line in response):
      return WifiConnectResult(
        connected=False,
        error='connection_failed',
        response=response,
      )
      
    if any('connection timeout' in line for line in response):
      return WifiConnectResult(
        connected=False,
        error='connection_timeout',
        response=response,
      )

    raise UnexpectedResponseError(f'Unknown WiFi connection response: {response}')

  def _parse_status(self, response: list[str]) -> WifiStatus:
    connected = False
    ssid = None
    ip = None
    rssi = None

    for line in response:
      if 'wifi station:' not in line:
        continue

      if 'WiFi: connected' in line:
        connected = True

      elif 'SSID:' in line:
        ssid = line.split('SSID:', 1)[1].strip()

      elif 'IP:' in line:
        ip = line.split('IP:', 1)[1].strip()

      elif 'RSSI:' in line:
        value = line.split('RSSI:', 1)[1].split('dBm', 1)[0].strip()
        rssi = int(value)

    return WifiStatus(
      connected=connected,
      ssid=ssid,
      ip=ip,
      rssi=rssi,
    )

  # endregion
