from config import FIRMWARE_PATH
from lib import FirmwareFlasher, find_device_port


def main():
  port = find_device_port()

  flasher = FirmwareFlasher()
  flasher.erase(port)
  flasher.flash(port, str(FIRMWARE_PATH))


if __name__ == '__main__':
  main()
