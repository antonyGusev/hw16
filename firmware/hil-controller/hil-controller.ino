#include <WiFi.h>
#include <WebServer.h>
#include <Preferences.h>
#include "esp_camera.h"

// ============================================================
// Wi-Fi
// ============================================================

const char* HIL_WIFI_SSID = "antony_g5";
const char* HIL_WIFI_PASSWORD = "9kJTQ8SvaY!$";

// ============================================================
// HIL GPIO
// ============================================================

// Button emulation -> ULN2003
#define HIL_K1 13
#define HIL_K2 14
#define HIL_K3 12
#define HIL_K4 15

// Physical feedback
#define RELAY_FEEDBACK 32
#define LED_SENSOR 33

// HC-SR04 emulation
#define HCSR04_TRIG 2  // DUT -> HIL
#define HCSR04_ECHO 0  // HIL -> DUT

// ============================================================
// Freenove ESP32-WROVER camera
// CAMERA_MODEL_WROVER_KIT
// ============================================================

#define CAM_PWDN -1
#define CAM_RESET -1
#define CAM_XCLK 21
#define CAM_SIOD 26
#define CAM_SIOC 27

#define CAM_D7 35
#define CAM_D6 34
#define CAM_D5 39
#define CAM_D4 36
#define CAM_D3 19
#define CAM_D2 18
#define CAM_D1 5
#define CAM_D0 4

#define CAM_VSYNC 25
#define CAM_HREF 23
#define CAM_PCLK 22

// ============================================================
// General
// ============================================================

const uint32_t PRESS_TIME_MS = 150;

// ============================================================
// LED sensor
// ============================================================

const uint32_t LED_SETTLE_TIME_MS = 1000;
const int LED_SAMPLES = 50;
const uint32_t LED_SAMPLE_DELAY_MS = 5;
const int LED_MIN_CALIBRATION_DELTA = 200;

// ============================================================
// HC-SR04
// ============================================================

volatile bool hcTriggerDetected = false;

uint16_t simulatedDistanceCm = 50;

// ============================================================
// NVS
// ============================================================

Preferences preferences;

int ledOffLevel = 0;
int ledOnLevel = 0;
int ledThreshold = 0;

bool ledCalibrated = false;

// ============================================================
// Camera / HTTP
// ============================================================

WebServer server(80);

bool cameraReady = false;

// ============================================================
// BUTTONS
// ============================================================

void releaseAllButtons() {
  digitalWrite(HIL_K1, LOW);
  digitalWrite(HIL_K2, LOW);
  digitalWrite(HIL_K3, LOW);
  digitalWrite(HIL_K4, LOW);
}

void pressButton(uint8_t pin, const char* name) {
  Serial.printf("[HIL] %s press\n", name);

  digitalWrite(pin, HIGH);
  delay(PRESS_TIME_MS);
  digitalWrite(pin, LOW);

  Serial.printf("[HIL] %s release\n", name);
}

// ============================================================
// RELAY
// ============================================================

bool isRelayOn() {
  return digitalRead(RELAY_FEEDBACK) == LOW;
}

void printRelayStatus() {
  Serial.printf(
    "[HIL] RELAY: %s\n",
    isRelayOn() ? "ON" : "OFF");
}

// ============================================================
// LED ADC
// ============================================================

int readLedLevel() {
  long total = 0;

  for (int i = 0; i < LED_SAMPLES; i++) {
    total += analogRead(LED_SENSOR);
    delay(LED_SAMPLE_DELAY_MS);
  }

  return total / LED_SAMPLES;
}

void printLedLevel() {
  Serial.printf(
    "[HIL] LED ADC: %d\n",
    readLedLevel());
}

// ============================================================
// LED CALIBRATION STORAGE
// ============================================================

void loadLedCalibration() {
  preferences.begin("hil", true);

  ledCalibrated =
    preferences.getBool("led_cal", false);

  if (ledCalibrated) {
    ledOffLevel =
      preferences.getInt("led_off", 0);

    ledOnLevel =
      preferences.getInt("led_on", 0);

    ledThreshold =
      preferences.getInt("led_thr", 0);
  }

  preferences.end();
}

void saveLedCalibration() {
  preferences.begin("hil", false);

  preferences.putInt("led_off", ledOffLevel);
  preferences.putInt("led_on", ledOnLevel);
  preferences.putInt("led_thr", ledThreshold);
  preferences.putBool("led_cal", true);

  preferences.end();

  ledCalibrated = true;
}

// ============================================================
// LED CALIBRATION
// ============================================================

void calibrateLed() {
  Serial.println();
  Serial.println("[HIL] LED calibration started");

  delay(LED_SETTLE_TIME_MS);

  int levelA = readLedLevel();

  Serial.printf(
    "[HIL] State A ADC: %d\n",
    levelA);

  Serial.println(
    "[HIL] Toggling LED using K4...");

  pressButton(HIL_K4, "K4");

  delay(LED_SETTLE_TIME_MS);

  int levelB = readLedLevel();

  Serial.printf(
    "[HIL] State B ADC: %d\n",
    levelB);

  int delta = abs(levelA - levelB);

  Serial.printf(
    "[HIL] ADC delta: %d\n",
    delta);

  if (delta < LED_MIN_CALIBRATION_DELTA) {

    Serial.println(
      "[HIL] ERROR: LED calibration failed");

    Serial.println(
      "[HIL] Difference between ON/OFF is too small");

    Serial.println(
      "[HIL] Restoring original LED state...");

    pressButton(HIL_K4, "K4");
    delay(LED_SETTLE_TIME_MS);

    return;
  }

  if (levelA < levelB) {
    ledOffLevel = levelA;
    ledOnLevel = levelB;
  } else {
    ledOffLevel = levelB;
    ledOnLevel = levelA;
  }

  ledThreshold =
    ledOffLevel + ((ledOnLevel - ledOffLevel) / 2);

  saveLedCalibration();

  Serial.println();
  Serial.println("[HIL] Calibration complete");

  Serial.printf(
    "[HIL] LED OFF: %d\n",
    ledOffLevel);

  Serial.printf(
    "[HIL] LED ON: %d\n",
    ledOnLevel);

  Serial.printf(
    "[HIL] Threshold: %d\n",
    ledThreshold);

  Serial.println(
    "[HIL] Calibration saved to NVS");

  Serial.println(
    "[HIL] Restoring original LED state...");

  pressButton(HIL_K4, "K4");

  delay(LED_SETTLE_TIME_MS);

  Serial.println(
    "[HIL] Original LED state restored");

  Serial.println();
}

bool isLedOn(int level) {
  return level > ledThreshold;
}

void printLedStatus() {
  if (!ledCalibrated) {
    Serial.println(
      "[HIL] ERROR: LED is not calibrated");

    Serial.println(
      "[HIL] Run: led_calibrate");

    return;
  }

  int level = readLedLevel();

  Serial.printf(
    "[HIL] LED: %s\n",
    isLedOn(level) ? "ON" : "OFF");

  Serial.printf(
    "[HIL] LED ADC: %d\n",
    level);

  Serial.printf(
    "[HIL] Threshold: %d\n",
    ledThreshold);
}

void printLedCalibration() {
  if (!ledCalibrated) {
    Serial.println(
      "[HIL] LED calibration: NOT CALIBRATED");
    return;
  }

  Serial.println("[HIL] LED calibration:");

  Serial.printf(
    "[HIL] OFF:       %d\n",
    ledOffLevel);

  Serial.printf(
    "[HIL] ON:        %d\n",
    ledOnLevel);

  Serial.printf(
    "[HIL] Threshold: %d\n",
    ledThreshold);
}

// ============================================================
// HC-SR04
// ============================================================

void IRAM_ATTR onHcTrigger() {
  hcTriggerDetected = true;
}

void serviceHcSr04() {
  if (!hcTriggerDetected) {
    return;
  }

  noInterrupts();
  hcTriggerDetected = false;
  interrupts();

  uint32_t echoUs =
    (uint32_t)simulatedDistanceCm * 58;

  // Small response delay
  delayMicroseconds(100);

  digitalWrite(HCSR04_ECHO, HIGH);
  delayMicroseconds(echoUs);
  digitalWrite(HCSR04_ECHO, LOW);
}

void setDistance(String command) {
  String value =
    command.substring(9);

  value.trim();

  int cm = value.toInt();

  if (cm < 2 || cm > 400) {

    Serial.println(
      "[HIL] ERROR: distance must be 2-400 cm");

    return;
  }

  simulatedDistanceCm = cm;

  Serial.printf(
    "[HIL] HC-SR04 distance set to %d cm\n",
    cm);
}

void printDistanceStatus() {
  Serial.printf(
    "[HIL] HC-SR04 simulated distance: %u cm\n",
    simulatedDistanceCm);
}

// ============================================================
// CAMERA
// ============================================================

bool initCamera() {
  camera_config_t config = {};

  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;

  config.pin_d0 = CAM_D0;
  config.pin_d1 = CAM_D1;
  config.pin_d2 = CAM_D2;
  config.pin_d3 = CAM_D3;
  config.pin_d4 = CAM_D4;
  config.pin_d5 = CAM_D5;
  config.pin_d6 = CAM_D6;
  config.pin_d7 = CAM_D7;

  config.pin_xclk = CAM_XCLK;
  config.pin_pclk = CAM_PCLK;
  config.pin_vsync = CAM_VSYNC;
  config.pin_href = CAM_HREF;

  config.pin_sccb_sda = CAM_SIOD;
  config.pin_sccb_scl = CAM_SIOC;

  config.pin_pwdn = CAM_PWDN;
  config.pin_reset = CAM_RESET;

  config.xclk_freq_hz = 20000000;

  config.pixel_format = PIXFORMAT_JPEG;

  // VGA is plenty for LED color detection.
  config.frame_size = FRAMESIZE_VGA;

  config.jpeg_quality = 10;

  if (psramFound()) {
    config.fb_count = 2;
    config.fb_location = CAMERA_FB_IN_PSRAM;
    config.grab_mode = CAMERA_GRAB_LATEST;
  } else {
    config.fb_count = 1;
    config.fb_location = CAMERA_FB_IN_DRAM;
    config.grab_mode = CAMERA_GRAB_WHEN_EMPTY;
  }

  esp_err_t err =
    esp_camera_init(&config);

  if (err != ESP_OK) {

    Serial.printf(
      "[HIL] ERROR: Camera init failed: 0x%x\n",
      err);

    return false;
  }

  sensor_t* sensor = esp_camera_sensor_get();

  if (sensor != nullptr) {
    if (sensor->id.PID == OV3660_PID) {
      sensor->set_vflip(sensor, 1);
    }

    // Disable automatic exposure/gain.
    sensor->set_gain_ctrl(sensor, 0);
    sensor->set_exposure_ctrl(sensor, 0);

    // Low fixed gain.
    sensor->set_agc_gain(sensor, 0);

    // Short exposure.
    sensor->set_aec_value(sensor, 100);

    // Keep color processing neutral.
    sensor->set_brightness(sensor, 0);
    sensor->set_contrast(sensor, 0);
    sensor->set_saturation(sensor, 0);
  }

  Serial.println(
    "[HIL] Camera initialized");

  return true;
}

// ============================================================
// HTTP
// ============================================================

void handleRoot() {
  String message;

  message += "HIL Controller\n";
  message += "\n";
  message += "GET /capture\n";
  message += "GET /status\n";

  server.send(
    200,
    "text/plain",
    message);
}

void handleStatus() {
  String json = "{";

  json += "\"camera\":";
  json += cameraReady ? "\"ready\"" : "\"error\"";

  json += ",";

  json += "\"distance_cm\":";
  json += String(simulatedDistanceCm);

  json += ",";

  json += "\"relay\":";
  json += isRelayOn() ? "\"on\"" : "\"off\"";

  json += "}";

  server.send(
    200,
    "application/json",
    json);
}

void handleCapture() {
  if (!cameraReady) {

    server.send(
      503,
      "text/plain",
      "Camera not ready");

    return;
  }

  camera_fb_t* fb =
    esp_camera_fb_get();

  if (!fb) {

    server.send(
      500,
      "text/plain",
      "Camera capture failed");

    return;
  }

  server.setContentLength(fb->len);

  server.send(
    200,
    "image/jpeg",
    "");

  WiFiClient client =
    server.client();

  client.write(
    fb->buf,
    fb->len);

  esp_camera_fb_return(fb);
}

// ============================================================
// WIFI
// ============================================================

void connectWiFi() {
  Serial.printf(
    "[HIL] Connecting to Wi-Fi: %s\n",
    HIL_WIFI_SSID);

  WiFi.mode(WIFI_STA);

  WiFi.begin(
    HIL_WIFI_SSID,
    HIL_WIFI_PASSWORD);

  uint32_t started = millis();

  while (
    WiFi.status() != WL_CONNECTED && millis() - started < 15000) {
    delay(250);
    Serial.print(".");
  }

  Serial.println();

  if (WiFi.status() != WL_CONNECTED) {

    Serial.println(
      "[HIL] ERROR: Wi-Fi connection failed");

    return;
  }

  Serial.println(
    "[HIL] Wi-Fi connected");

  Serial.print(
    "[HIL] IP: ");

  Serial.println(
    WiFi.localIP());

  Serial.print(
    "[HIL] Capture URL: http://");

  Serial.print(
    WiFi.localIP());

  Serial.println(
    "/capture");
}

// ============================================================
// HELP
// ============================================================

void printHelp() {
  Serial.println();

  Serial.println("[HIL] Commands:");

  Serial.println(
    "  k1              - emulate K1 press");

  Serial.println(
    "  k2              - emulate K2 press");

  Serial.println(
    "  k3              - emulate K3 press");

  Serial.println(
    "  k4              - emulate K4 press");

  Serial.println(
    "  relay_status    - read physical relay state");

  Serial.println(
    "  led_level       - read raw LED ADC");

  Serial.println(
    "  led_status      - read physical LED state");

  Serial.println(
    "  led_calibrate   - calibrate LED sensor");

  Serial.println(
    "  led_calibration - show LED calibration");

  Serial.println(
    "  distance <cm>   - set HC-SR04 distance");

  Serial.println(
    "  distance_status - show HC-SR04 distance");

  Serial.println(
    "  camera_status   - show camera status");

  Serial.println(
    "  camera_url      - show capture URL");

  Serial.println(
    "  help");

  Serial.println();
}

// ============================================================
// CAMERA UART STATUS
// ============================================================

void printCameraStatus() {
  Serial.printf(
    "[HIL] CAMERA: %s\n",
    cameraReady ? "READY" : "ERROR");
}

void printCameraUrl() {
  if (WiFi.status() != WL_CONNECTED) {

    Serial.println(
      "[HIL] ERROR: Wi-Fi not connected");

    return;
  }

  Serial.print(
    "[HIL] Camera capture: http://");

  Serial.print(
    WiFi.localIP());

  Serial.println(
    "/capture");
}

// ============================================================
// SETUP
// ============================================================

void setup() {
  Serial.begin(115200);

  delay(500);

  // --------------------------------------------------------
  // Buttons
  // --------------------------------------------------------

  pinMode(HIL_K1, OUTPUT);
  pinMode(HIL_K2, OUTPUT);
  pinMode(HIL_K3, OUTPUT);
  pinMode(HIL_K4, OUTPUT);

  releaseAllButtons();

  // --------------------------------------------------------
  // Relay
  // --------------------------------------------------------

  pinMode(
    RELAY_FEEDBACK,
    INPUT_PULLUP);

  // --------------------------------------------------------
  // LDR
  // --------------------------------------------------------

  pinMode(
    LED_SENSOR,
    INPUT);

  // --------------------------------------------------------
  // HC-SR04
  // --------------------------------------------------------

  pinMode(
    HCSR04_TRIG,
    INPUT);

  pinMode(
    HCSR04_ECHO,
    OUTPUT);

  digitalWrite(
    HCSR04_ECHO,
    LOW);

  attachInterrupt(
    digitalPinToInterrupt(HCSR04_TRIG),
    onHcTrigger,
    RISING);

  // --------------------------------------------------------
  // NVS
  // --------------------------------------------------------

  loadLedCalibration();

  // --------------------------------------------------------
  // Camera
  // --------------------------------------------------------

  cameraReady =
    initCamera();

  // --------------------------------------------------------
  // Wi-Fi
  // --------------------------------------------------------

  connectWiFi();

  // --------------------------------------------------------
  // HTTP
  // --------------------------------------------------------

  if (WiFi.status() == WL_CONNECTED) {

    server.on(
      "/",
      HTTP_GET,
      handleRoot);

    server.on(
      "/status",
      HTTP_GET,
      handleStatus);

    server.on(
      "/capture",
      HTTP_GET,
      handleCapture);

    server.begin();

    Serial.println(
      "[HIL] HTTP server started");
  }

  // --------------------------------------------------------
  // Ready
  // --------------------------------------------------------

  Serial.println();
  Serial.println(
    "[HIL] Controller ready");

  if (ledCalibrated) {

    Serial.println(
      "[HIL] LED calibration loaded from NVS");

    Serial.printf(
      "[HIL] LED threshold: %d\n",
      ledThreshold);
  } else {

    Serial.println(
      "[HIL] LED is not calibrated");
  }

  Serial.printf(
    "[HIL] HC-SR04 distance: %u cm\n",
    simulatedDistanceCm);

  printCameraStatus();

  printHelp();
}

// ============================================================
// LOOP
// ============================================================

void loop() {
  // HTTP
  if (WiFi.status() == WL_CONNECTED) {
    server.handleClient();
  }

  // HC-SR04
  serviceHcSr04();

  // UART commands
  if (!Serial.available()) {
    return;
  }

  String command =
    Serial.readStringUntil('\n');

  command.trim();
  command.toLowerCase();

  if (command == "k1") {

    pressButton(
      HIL_K1,
      "K1");
  }

  else if (command == "k2") {

    pressButton(
      HIL_K2,
      "K2");
  }

  else if (command == "k3") {

    pressButton(
      HIL_K3,
      "K3");
  }

  else if (command == "k4") {

    pressButton(
      HIL_K4,
      "K4");
  }

  else if (
    command == "relay_status") {

    printRelayStatus();
  }

  else if (
    command == "led_level") {

    printLedLevel();
  }

  else if (
    command == "led_status") {

    printLedStatus();
  }

  else if (
    command == "led_calibrate") {

    calibrateLed();
  }

  else if (
    command == "led_calibration") {

    printLedCalibration();
  }

  else if (
    command.startsWith("distance ")) {

    setDistance(command);
  }

  else if (
    command == "distance_status") {

    printDistanceStatus();
  }

  else if (
    command == "camera_status") {

    printCameraStatus();
  }

  else if (
    command == "camera_url") {

    printCameraUrl();
  }

  else if (
    command == "help") {

    printHelp();
  }

  else if (
    command.length() > 0) {

    Serial.printf(
      "[HIL] Unknown command: %s\n",
      command.c_str());
  }
}
