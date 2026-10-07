# Embedded HIL Test Automation Framework

Python-based Hardware-in-the-Loop (HIL) test automation framework for testing an ESP32-S3 device.

The framework communicates with the Device Under Test (DUT) and a dedicated ESP32 HIL controller over UART. The HIL controller provides physical interaction with the DUT, including button press emulation, relay state monitoring, sensor emulation, and visual LED verification.

Computer vision is used to verify the physical WS2812 LED indication. An OV3660 camera connected to the HIL controller captures the DUT, while OpenCV-based HSV analysis dynamically detects the LED region and determines its actual color. A predefined fallback ROI is used when dynamic detection is unavailable, and camera artifacts are saved for test analysis.

The project currently covers Wi-Fi functionality, physical controls, relay behavior, sensor interaction, and WS2812 LED indication.

## Key Features

- UART communication with DUT and HIL controller
- Wi-Fi connect, disconnect, status, and scan testing
- Physical button press emulation
- Relay state monitoring
- HC-SR04 distance sensor emulation
- WS2812 LED verification using computer vision
- Dynamic LED ROI detection with fallback ROI
- HSV-based LED color analysis
- Automatic camera artifacts for test analysis
- Independent pytest fixtures for reliable test setup
- Pytest-based automated test execution

## Project Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -e .
```

### 4. Configure the environment

Create a `.env` file in the project root and provide the required test configuration.

Example:

```env
HIL_PORT=your_com_port
SSID=your_wifi_ssid
PASSWORD=your_wifi_password
HIL_CAMERA_URL=http://<hil-ip>/capture
```

## Running Tests

Run the complete regression suite:

```bash
poe regression
```

Run Wi-Fi positive tests:

```bash
poe positive_tests
```

Tests can also be executed directly with pytest:

```bash
pytest tests
```

Run a specific test:

```bash
pytest tests/wifi/test_wifi_positive.py::test_connect_using_ssid
```

Use verbose output:

```bash
pytest tests -v
```

## Project Structure

```text
project/
├── framework/
│   ├── device/
│   │   ├── controllers/
│   │   └── device_driver.py
│   │
│   └── hil/
│       ├── controllers/
│       └── hil_driver.py
│
├── lib/
│   ├── connectors/
│   │   └── uart_connector.py
│   └── utilities/
│       ├── exceptions.py
│       └── utilities.py
│
├── tests/
│   ├── wifi/
│   └── conftest.py
│
├── artifacts/
│   └── camera/
│
├── config.py
├── pyproject.toml
└── README.md
```

### `framework/device`

Contains the DUT abstraction and feature-specific controllers.

Controllers expose high-level operations such as Wi-Fi connection, disconnection, status, and scanning while hiding UART communication details from tests.

### `framework/hil`

Contains the Hardware-in-the-Loop abstraction and controllers responsible for physical interaction with the DUT.

The HIL controller provides functionality for button press emulation, hardware signal monitoring, sensor emulation, and camera-based verification.

`CameraController` handles image capture, dynamic ROI detection, HSV color analysis, and generation of camera artifacts.

### `lib`

Contains reusable low-level components shared by the framework, including:

- UART communication
- Custom framework exceptions
- Device discovery
- Polling and waiting utilities

### `tests`

Contains pytest test suites and fixtures.

Fixtures prepare the required DUT and HIL state so tests remain independent from execution order.

### `artifacts`

Contains artifacts generated during test execution.

Camera artifacts include full debug frames and detected LED regions:

These artifacts can be used to verify the selected ROI and troubleshoot computer-vision or DUT LED indication failures.

## Architecture

The framework separates DUT control from HIL interaction:

```text
                         Tests
                           │
              ┌────────────┴────────────┐
              │                         │
        DeviceDriver                HILDriver
              │                         │
      Device Controllers         HIL Controllers
              │                         │
        UARTConnector              UARTConnector
              │                         │
          ESP32-S3              ESP32 HIL Controller
             DUT                  + OV3660 Camera
```

### DUT communication

```text
Test
  ↓
DeviceDriver
  ↓
Device Controller
  ↓
UARTConnector
  ↓
ESP32-S3 DUT
```

### HIL interaction

```text
Test
  ↓
HILDriver
  ↓
HIL Controller
  ↓
UARTConnector / Camera
  ↓
ESP32 HIL Controller
  ↓
Physical DUT
```

This separation keeps test cases focused on device behavior while UART protocol handling, hardware interaction, and computer-vision processing remain encapsulated inside the framework.