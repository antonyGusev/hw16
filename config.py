import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

SSID = os.environ['SSID']
PASSWORD = os.environ['PASSWORD']

HIL_PORT = os.environ['HIL_PORT']

ROOT_DIR = Path(__file__).resolve().parent
FIRMWARE_PATH = ROOT_DIR / 'artifacts' / 'firmware' / 'device' / 'station_WiFi_v1.3.0_merged.bin'

LAMP_DEFAULT_COLOR = 'white'
LAMP_DEFAULT_RGB = (255, 255, 255)
LAMP_DEFAULT_BRIGHTNESS = 50
LAMP_DEFAULT_MODE = 'solid'
