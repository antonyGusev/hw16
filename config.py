import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

SSID = os.getenv('SSID')
PASSWORD = os.getenv('PASSWORD')

HIL_PORT = os.getenv('HIL_PORT')

OTA_INVALID_IMAGE_HEADER = os.getenv('OTA_INVALID_IMAGE_HEADER')
OTA_CORRUPTED_IMAGE = os.getenv('OTA_CORRUPTED_IMAGE')

OTA_HTTPS_URL = os.getenv('OTA_HTTPS_URL')
OTA_HTTPS_VERSION = os.getenv('OTA_HTTPS_VERSION')

ROOT_DIR = Path(__file__).resolve().parent
FIRMWARE_PATH = ROOT_DIR / 'artifacts' / 'firmware' / 'device' / 'station_WiFi_v1.3.0_merged.bin'

LAMP_DEFAULT_COLOR = 'white'
LAMP_DEFAULT_RGB = (255, 255, 255)
LAMP_DEFAULT_BRIGHTNESS = 50
LAMP_DEFAULT_MODE = 'solid'
