import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

SSID = os.getenv('SSID')
PASSWORD = os.getenv('PASSWORD')

HIL_PORT = os.getenv('HIL_PORT')

OTA_INVALID_IMAGE_HEADERS = {
  '1.3.0': os.getenv('OTA_INVALID_IMAGE_HEADER_1_3_0'),
  '1.4.0': os.getenv('OTA_INVALID_IMAGE_HEADER_1_4_0'),
  '1.5.0': os.getenv('OTA_INVALID_IMAGE_HEADER_1_5_0'),
}

OTA_CORRUPTED_IMAGES = {
  '1.3.0': os.getenv('OTA_CORRUPTED_IMAGE_1_3_0'),
  '1.4.0': os.getenv('OTA_CORRUPTED_IMAGE_1_4_0'),
  '1.5.0': os.getenv('OTA_CORRUPTED_IMAGE_1_5_0'),
}

OTA_HTTPS_URL = os.getenv('OTA_HTTPS_URL')
OTA_HTTPS_VERSION = os.getenv('OTA_HTTPS_VERSION')

ROOT_DIR = Path(__file__).resolve().parent
FIRMWARE_PATH = ROOT_DIR / 'artifacts' / 'firmware' / 'device' / 'station_WiFi_v1.3.0_merged.bin'

LAMP_DEFAULT_COLOR = 'white'
LAMP_DEFAULT_RGB = (255, 255, 255)
LAMP_DEFAULT_BRIGHTNESS = 50
LAMP_DEFAULT_MODE = 'solid'
