import os

from dotenv import load_dotenv

load_dotenv()

SSID = os.environ['SSID']
PASSWORD = os.environ['PASSWORD']

HIL_PORT = os.environ['HIL_PORT']
HIL_CAMERA_URL = os.environ['HIL_CAMERA_URL']
