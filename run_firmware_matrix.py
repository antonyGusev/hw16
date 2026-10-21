"""Flash 1.3.0 once, then run pytest on 1.3.0, 1.4.0, and 1.5.0.

Run from the hw16 project root: python run_firmware_matrix.py
"""

import re
import subprocess
import sys
from pathlib import Path

from packaging.version import Version

from config import PASSWORD, SSID
from framework import DeviceDriver
from lib import UARTConnector, find_device_port, has_active_wifi_connection, read_firmware

ROOT = Path(__file__).resolve().parent
VERSIONS = (Version('1.3.0'), Version('1.4.0'), Version('1.5.0'))
SCENE_FIRST = 'tests/lamp/test_09_lamp_scenes.py::test_reject_loading_empty_scene'


FAILURE_REPORTS = []
ANSI_ESCAPE = re.compile(r'\x1b\[[0-9;]*m')


def print_failure_reports() -> None:
  if not FAILURE_REPORTS:
    return

  print('\n=== Pytest failure reports (all firmware stages) ===', flush=True)
  for label, report in FAILURE_REPORTS:
    print(f'\n=== {label} ===', flush=True)
    print(report, end='\n' if not report.endswith('\n') else '', flush=True)


def run_pytest(label: str, args: list[str], allow_failures: bool = True) -> bool:
  print(f'\n=== {label} ===', flush=True)
  process = subprocess.Popen(
    [sys.executable, '-m', 'pytest', '--color=yes', '-rs', *args],
    cwd=ROOT,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    errors='replace',
    bufsize=1,
  )

  report_lines = []
  collecting_report = False
  assert process.stdout is not None
  for line in process.stdout:
    if re.match(r'^=+ (FAILURES|ERRORS|short test summary info) =+', ANSI_ESCAPE.sub('', line)):
      collecting_report = True
    if collecting_report:
      report_lines.append(line)
    else:
      print(line, end='', flush=True)

  returncode = process.wait()
  if report_lines:
    report = ''.join(report_lines)
    skipped = [
      line for line in report.splitlines() if re.match(r'^SKIPPED\s+', ANSI_ESCAPE.sub('', line))
    ]
    if skipped:
      print(f'\nSkipped tests in {label}:', flush=True)
      for line in skipped:
        print(line, flush=True)
    FAILURE_REPORTS.append((label, report))
  if returncode == 0:
    return True
  if returncode == 1 and allow_failures:
    summary = re.findall(r'\b(\d+) failed\b', ANSI_ESCAPE.sub('', ''.join(report_lines)))
    count = f'{summary[-1]} FAILED tests' if summary else 'FAILED tests'
    print(f'{count} in {label}; continuing to collect results.', flush=True)
    return False
  raise RuntimeError(f'{label}: pytest exited with code {returncode}')


def get_version() -> Version:
  connector = UARTConnector(find_device_port())
  connector.open()
  try:
    device = DeviceDriver(connector)
    current, _, state = read_firmware(device)
    assert state.lower() == 'valid', f'Firmware {current} state is {state}'
    return current
  finally:
    connector.close()


def check_version(expected: Version) -> None:
  current = get_version()
  assert current == expected, f'Expected firmware {expected}, got {current}'


def install_version(expected: Version, target: Version) -> None:
  print(f'\n=== OTA {expected} -> {target} ===', flush=True)
  connector = UARTConnector(find_device_port())
  connector.open()
  try:
    device = DeviceDriver(connector)
    current, _, state = read_firmware(device)
    assert current == expected, f'Expected {expected} before OTA, got {current}'
    assert state.lower() == 'valid', f'Unexpected firmware state: {state}'

    if not has_active_wifi_connection(device):
      result = device.wifi.connect(SSID, PASSWORD)
      assert result.connected, f'Wi-Fi connection failed: {result.response}'

    response = device.ota.install(str(target))
    assert '[OTA] success:' in '\n'.join(response), f'OTA install failed: {response}'
    device.wait_for_log("ready. Type 'help' for commands", timeout=60)
    current, _, state = read_firmware(device)
    assert current == target, f'Expected {target} after OTA, got {current}'
    assert state.lower() == 'valid', f'Firmware {current} state is {state}'
  finally:
    connector.close()


def main() -> int:
  print('=== Full flash: 1.3.0 ===', flush=True)
  subprocess.run([sys.executable, 'flash_device.py'], cwd=ROOT, check=True)
  check_version(VERSIONS[0])

  failed_stages = []

  if not run_pytest(f'{VERSIONS[0]}: first', ['-m', 'first']):
    failed_stages.append(f'{VERSIONS[0]}: first')

  # Gatekeeper tests perform their own OTA upgrades and downgrades,
  # returning the DUT to 1.3.0. Any failure blocks the whole matrix.
  run_pytest(f'{VERSIONS[0]}: OTA gatekeeper', ['-m', 'ota_gatekeeper'], allow_failures=False)
  check_version(VERSIONS[0])

  for index, version in enumerate(VERSIONS):
    if index:
      current = get_version()
      if current == VERSIONS[index - 1]:
        install_version(current, version)
      elif current == version:
        print(f'Firmware {version} already installed; skipping OTA.', flush=True)
      else:
        raise RuntimeError(f'Unexpected firmware {current} before {version} stage')

    print(f'\n######## Firmware {version} ########', flush=True)
    check_version(version)

    # The empty scene must be checked before other 1.5.0 tests save scenes.
    if version >= Version('1.5.0') and not run_pytest(f'{version}: empty scene', [SCENE_FIRST]):
      failed_stages.append(f'{version}: empty scene')

    if not run_pytest(f'{version}: suite', ['-m', 'not first and not ota_gatekeeper']):
      failed_stages.append(f'{version}: suite')

    current = get_version()
    next_version = VERSIONS[index + 1] if index + 1 < len(VERSIONS) else None
    if current != version and current != next_version:
      raise RuntimeError(f'Unexpected firmware {current} after {version} suite')
    if current == next_version:
      print(f'Firmware advanced to {next_version} during {version} suite.', flush=True)

  print('\n=== Firmware matrix finished ===', flush=True)
  if failed_stages:
    print('Stages with failed tests:', ', '.join(failed_stages), flush=True)
    return 1
  print('All executed stages passed.', flush=True)
  return 0


if __name__ == '__main__':
  try:
    sys.exit(main())
  except (AssertionError, OSError, RuntimeError, subprocess.CalledProcessError) as error:
    print(f'Runner stopped: {error}', file=sys.stderr, flush=True)
    sys.exit(2)
  finally:
    print_failure_reports()
