import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

SSID = os.environ['SSID']
PASSWORD = os.environ['PASSWORD']

HIL_PORT = os.environ['HIL_PORT']

ROOT_DIR = Path(__file__).resolve().parent
FIRMWARE_PATH = ROOT_DIR / 'firmware' / 'device' / 'station_WiFi_v1.3.0_merged.bin'
