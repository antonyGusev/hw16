import subprocess
import sys


class FirmwareFlasher:
  def erase(self, port: str) -> None:
    subprocess.run(
      [sys.executable, '-m', 'esptool', '--chip', 'esp32s3', '--port', port, 'erase-flash'],
      check=True,
    )

  def flash(self, port: str, firmware_path: str) -> None:
    subprocess.run(
      [
        sys.executable,
        '-m',
        'esptool',
        '--chip',
        'esp32s3',
        '--port',
        port,
        'write-flash',
        '0x0',
        firmware_path,
      ],
      check=True,
    )
