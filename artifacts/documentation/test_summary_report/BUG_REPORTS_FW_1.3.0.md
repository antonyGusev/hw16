# Bug Reports — Firmware 1.3.0

**Test environment:** ESP32-S3 Smart Lamp DUT; UART/pytest/HIL automation.  
**Detected on:** FW `1.3.0`.  
**Other firmware versions:** `1.4.0` and `1.5.0` — **Not Tested** for the defects below.  
**Evidence source:** OTA pytest output (`3 failed, 33 passed, 2 skipped`) and Smart Lamp pytest output (`11 failed, 40 passed, 11 skipped`) supplied with this report.  
**Reproducibility:** each specific failure is documented in **one supplied run (1/1 observed)**; repeated reproduction has **not** been confirmed.  
**Hardware revision / build number:** not specified in the supplied logs.  

> **Important:** Severity and priority below are proposed triage assessments, not approved Jira classifications. Camera/HIL measurements alone do not conclusively distinguish firmware faults from optical setup or camera calibration issues.

## BUG-OTA-001 — OTA retry is blocked after Wi-Fi interruption via K3

| Field | Details |
|---|---|
| **ID** | `BUG-OTA-001` |
| **Title** | OTA remains “already in progress” after interrupted download and Wi-Fi recovery |
| **Found in** | `1.3.0` |
| **Also reproduces in** | `1.4.0`: Not Tested; `1.5.0`: Not Tested |
| **Severity / Priority** | **Major / High** (proposed) |
| **Requirement** | **OTA-6** — after Wi-Fi is restored, a new OTA attempt must work immediately **without reboot** |
| **Automated test** | `tests/ota/test_04_interrupt.py::test_ota_interrupt_wifi_by_k3_button` |
| **Reproducibility** | **1/1 observed**; repeated runs not supplied |

**Preconditions**

- DUT running FW `1.3.0`, active Wi-Fi connection, firmware image in `valid` state.
- Version `1.4.0` available on OTA server; HIL button K3 controls Wi-Fi disconnect.

**Steps to reproduce**

1. Start `ota install 1.4.0`.
2. Wait for `[OTA] progress: 10%`.
3. Press K3 to disconnect Wi-Fi during download.
4. Wait for the OTA interruption message; verify that the current firmware version/partition remain unchanged.
5. Reconnect Wi-Fi.
6. Retry `ota install 1.4.0` **without rebooting the DUT**.

**Expected result (OTA-6):** download interruption is handled, internal OTA state is cleared, and a new OTA attempt can start and complete after Wi-Fi reconnects without reboot.

**Actual result:** the retry is rejected because firmware reports that an update is already running.

**Evidence — UART / pytest**

```text
ota install 1.4.0
E (14346) wifi station: [OTA] error: update already in progress
AssertionError: OTA retry failed: ['ota install 1.4.0', 'E (14346) wifi station: [OTA] error: update already in progress']
```

**Photo/video:** not supplied. **Note:** the failed assertion confirms the locked retry; the provided excerpt does not contain the entire initial interruption log.

---

## BUG-OTA-002 — `ota-test-server` outputs a nonconforming no-Wi-Fi error

| Field | Details |
|---|---|
| **ID** | `BUG-OTA-002` |
| **Title** | `ota-test-server` omits `[OTA]` prefix on missing-Wi-Fi error, causing automation timeout |
| **Found in** | `1.3.0` |
| **Also reproduces in** | `1.4.0`: Not Tested; `1.5.0`: Not Tested |
| **Severity / Priority** | **Minor / Medium** (proposed) |
| **Requirements** | **OTA-7** — OTA commands without Wi-Fi must reject the operation; **OTA-12** — `ota-test-server` simulation |
| **Automated test** | `tests/ota/test_05_no_wifi.py::test_ota_without_wifi[ota-test-server]` |
| **Reproducibility** | **1/1 observed**; repeated runs not supplied |

**Preconditions**

- DUT running FW `1.3.0`, with no active Wi-Fi connection.
- UART console available.

**Steps to reproduce**

1. Verify the device has no active Wi-Fi connection.
2. Execute `ota-test-server` over UART.
3. Observe the returned error string and the pytest controller response.

**Expected result (OTA-7):** the command is rejected promptly and follows the OTA error-message contract used by the test:

```text
[OTA] failed: WiFi not connected. Use 'connect' first.
```

**Actual result:** the device **does reject the command**, but returns `OTA failed: ...` instead of `[OTA] failed: ...`. The UART controller expects the latter prefix, so it times out after 30 seconds.

**Evidence — UART / pytest**

```text
ota-test-server
E (961) wifi station: OTA failed: WiFi not connected. Use 'connect' first.

DeviceTimeoutError: Expected response (
  "[OTA] failed: WiFi not connected. Use 'connect' first.",
  '[OTA] check failed:', '[OTA] failed:', '[OTA] error:',
  '=== OTA Update Started ==='
) was not received within 30s.
```

**Photo/video:** not applicable to console-text behavior; not supplied.  
**Triage note:** this proves a message-format mismatch with the automated controller. If the PRD requires only the error meaning rather than the exact `[OTA]` prefix, the defect may belong in the test parser instead of firmware; confirm the intended output contract before assignment.

---

## BUG-OTA-003 — OTA remains locked after invalid-image rejection

| Field | Details |
|---|---|
| **ID** | `BUG-OTA-003` |
| **Title** | A failed invalid-image OTA attempt blocks subsequent valid installation |
| **Found in** | `1.3.0` |
| **Also reproduces in** | `1.4.0`: Not Tested; `1.5.0`: Not Tested |
| **Severity / Priority** | **Major / High** (proposed) |
| **Requirements** | **OTA-11** — invalid/corrupted image must be rejected while current firmware remains operational; related OTA recovery behavior |
| **Automated test** | `tests/ota/test_08_invalid_image.py::test_ota_install_after_invalid_image` |
| **Reproducibility** | **1/1 observed**; repeated runs not supplied |

**Preconditions**

- DUT running FW `1.3.0`, connected to Wi-Fi, firmware state `valid`.
- Invalid-image URL configured for the OTA test.

**Steps to reproduce**

1. Start OTA installation using a URL pointing to an invalid firmware image.
2. Wait until validation fails (`ESP_ERR_OTA_VALIDATE_FAILED`).
3. Without rebooting, execute `ota install 1.3.0 force` to reinstall the current valid firmware.
4. Observe whether a new installation can start.

**Expected result (OTA-11 and OTA recovery expectation):** invalid image is rejected without affecting the active firmware; the OTA subsystem becomes available for a subsequent valid installation without manual reset.

**Actual result:** the invalid image is rejected, but the subsequent installation is blocked by `update already in progress`.

**Evidence — UART / pytest**

```text
ota install 1.3.0 force
E (7251) wifi station: [OTA] error: update already in progress
AssertionError: OTA remained locked after invalid image
```

**Photo/video:** not supplied. **Note:** `ESP_ERR_OTA_VALIDATE_FAILED` is checked earlier by the test, but the provided failure excerpt does not show that original UART line.

---

## BUG-LAMP-001 — Physical LED colors differ from requested RGB values

| Field | Details |
|---|---|
| **ID** | `BUG-LAMP-001` |
| **Title** | LED output colors do not match named or explicit RGB commands in camera verification |
| **Found in** | `1.3.0` |
| **Also reproduces in** | `1.4.0`: Not Tested; `1.5.0`: Not Tested |
| **Severity / Priority** | **Major / High** (proposed; verify root cause) |
| **Requirements** | **FR-L2**, **FR-L3**, **FR-L4** — named/explicit RGB values and physical LED correspondence |
| **Automated tests** | `test_02_lamp_named_colors.py::test_set_named_color` (red, green, purple, cyan); `test_03_lamp_rgb.py::test_set_rgb_color` (red, green, violet, purple) |
| **Reproducibility** | **8 failing parametrized cases in one run**; per-case rerun rate unverified |

**Preconditions**

- DUT running FW `1.3.0`, lamp enabled, camera ROI aligned with LED, stable observation environment.

**Steps to reproduce**

1. Set a named color (e.g., `lamp color red`) or explicit RGB (e.g., `lamp color 255 0 0`).
2. Observe the physical LED through the HIL camera.
3. Compare measured HSV with the HSV corresponding to the requested RGB.
4. Repeat for green, purple/violet, and cyan.

**Expected result (FR-L4):** physical LED colors correspond to the commanded RGB values.

**Actual result:** camera HSV readings do not match expected values for eight cases; test waits expire.

**Evidence — pytest / HIL camera**

```text
Named red:    Expected HSV (0, 255, 255),   actual (63, 250, 153)
Named green:  Expected HSV (60, 255, 255),  actual (6, 239, 159)
Named purple: Expected HSV (139, 255, 255), actual (87, 247, 151)
Named cyan:   Expected HSV (90, 255, 255),  actual (151, 142, 135)
RGB red:      Expected HSV (0, 255, 255),   actual (64, 236, 212)
RGB green:    Expected HSV (60, 255, 255),  actual (6, 232, 209)
RGB violet:   Expected HSV (135, 170, 192), actual (92, 141, 167)
RGB purple:   Expected HSV (130, 191, 200), actual (95, 155, 169)
TimeoutError: Lamp did not reach RGB (...)
```

**Photo evidence — HIL camera (`artifacts/camera/failed/`):**

| Test case | Debug frame | Camera ROI |
|---|---|---|
| Named red | [Debug](../../camera/failed/red_255_0_0_debug.jpg) | [ROI](../../camera/failed/red_255_0_0_roi.jpg) |
| Named green | [Debug](../../camera/failed/green_0_255_0_debug.jpg) | [ROI](../../camera/failed/green_0_255_0_roi.jpg) |
| Named purple | [Debug](../../camera/failed/purple_160_0_255_debug.jpg) | [ROI](../../camera/failed/purple_160_0_255_roi.jpg) |
| Named cyan | [Debug](../../camera/failed/cyan_0_255_255_debug.jpg) | [ROI](../../camera/failed/cyan_0_255_255_roi.jpg) |
| RGB red | [Debug](../../camera/failed/rgb_red_255_0_0_debug.jpg) | [ROI](../../camera/failed/rgb_red_255_0_0_roi.jpg) |
| RGB green | [Debug](../../camera/failed/rgb_green_0_255_0_debug.jpg) | [ROI](../../camera/failed/rgb_green_0_255_0_roi.jpg) |
| RGB violet | [Debug](../../camera/failed/rgb_violet_128_64_192_debug.jpg) | [ROI](../../camera/failed/rgb_violet_128_64_192_roi.jpg) |
| RGB purple | [Debug](../../camera/failed/rgb_purple_100_50_200_debug.jpg) | [ROI](../../camera/failed/rgb_purple_100_50_200_roi.jpg) |

**Triage note:** treat as a physical-output verification failure. The logs alone do not prove whether the issue is firmware LED control, physical wiring, or camera color sampling; investigate without weakening the color assertions.

---

## BUG-LAMP-002 — Wi-Fi disconnected LED indication is not restored to red after lamp off

| Field | Details |
|---|---|
| **ID** | `BUG-LAMP-002` |
| **Title** | Wi-Fi-disconnected indication does not show expected red LED after `lamp off` |
| **Found in** | `1.3.0` |
| **Also reproduces in** | `1.4.0`: Not Tested; `1.5.0`: Not Tested |
| **Severity / Priority** | **Major / Medium** (proposed; potentially related to `BUG-LAMP-001`) |
| **Requirements** | **FR-W6** and **Smart Lamp integration** — lamp relinquishes LED control to Wi-Fi indication after switch-off; disconnected indication expected red |
| **Automated test** | `tests/lamp/test_11_lamp_wifi_indication.py::test_wifi_disconnected_indication_is_restored_after_lamp_off` |
| **Reproducibility** | **1/1 observed**; repeated runs not supplied |

**Preconditions**

- DUT running FW `1.3.0`; Wi-Fi disconnected; lamp switched on before the check.

**Steps to reproduce**

1. Put Wi-Fi into the disconnected state.
2. Switch on the lamp.
3. Execute `lamp off`.
4. Measure the LED color through the HIL camera.

**Expected result (FR-W6):** after `lamp off`, the LED returns to Wi-Fi disconnected indication (red, RGB `255,0,0`).

**Actual result:** the camera measures HSV `(64, 236, 178)` instead of expected red HSV `(0, 255, 255)`; validation times out.

**Evidence — pytest / HIL camera**

```text
TimeoutError: Lamp did not reach RGB (255, 0, 0).
Expected HSV: (0, 255, 255), actual HSV: (64, 236, 178).
```

**Photo evidence — HIL camera:**

- [Debug frame](../../camera/failed/wifi_disconnected_indication_after_lamp_off_255_0_0_debug.jpg)
- [Camera ROI](../../camera/failed/wifi_disconnected_indication_after_lamp_off_255_0_0_roi.jpg)

**Triage note:** may share a root cause with `BUG-LAMP-001`; track separately until verified because this test also covers ownership transfer from lamp to Wi-Fi indication.

---

## BUG-LAMP-003 — Brightness values outside 0–100% are accepted

| Field | Details |
|---|---|
| **ID** | `BUG-LAMP-003` |
| **Title** | Firmware accepts `lamp brightness -5` and `150` instead of rejecting out-of-range values |
| **Found in** | `1.3.0` |
| **Also reproduces in** | `1.4.0`: Not Tested; `1.5.0`: Not Tested |
| **Severity / Priority** | **Minor / Medium** (proposed) |
| **Requirement** | **FR-L5** — valid brightness range `0–100%`; invalid values must be rejected without changing brightness |
| **Automated test** | `tests/lamp/test_04_lamp_brightness.py::test_reject_brightness_outside_range[-5]` and `[150]` |
| **Reproducibility** | **2/2 sampled invalid values failed in one run**; repeated runs not supplied |

**Preconditions**

- DUT running FW `1.3.0`; UART console available; note the previous brightness setting.

**Steps to reproduce**

1. Execute `lamp brightness -5`.
2. Read the response and `lamp status`.
3. Execute `lamp brightness 150`.
4. Read the response and `lamp status`.

**Expected result (FR-L5):** both commands return `error: brightness must be 0-100`; stored brightness remains unchanged.

**Actual result:** firmware replies with successful set messages for both invalid values. The supplied failure output proves incorrect acceptance, but does not establish what value is ultimately stored.

**Evidence — UART / pytest**

```text
lamp brightness -5
I (29541) wifi station: [LAMP] brightness set: -5%

lamp brightness 150
I (30341) wifi station: [LAMP] brightness set: 150%

AssertionError: expected 'error: brightness must be 0-100'
```

**Photo/video:** not supplied; UART is the primary evidence for invalid-input handling.

---

## Summary

| Bug ID | Area | Description | FW 1.3.0 | FW 1.4.0 | FW 1.5.0 |
|---|---|---|---|---|---|
| BUG-OTA-001 | OTA | Retry blocked after K3 interruption | Observed | Not Tested | Not Tested |
| BUG-OTA-002 | OTA | Incorrect no-Wi-Fi message format for `ota-test-server` | Observed | Not Tested | Not Tested |
| BUG-OTA-003 | OTA | OTA locked after invalid image | Observed | Not Tested | Not Tested |
| BUG-LAMP-001 | Lamp | Physical color mismatch (8 parameter cases) | Observed | Not Tested | Not Tested |
| BUG-LAMP-002 | Lamp/Wi-Fi | Wi-Fi indication after `lamp off` has wrong measured color | Observed | Not Tested | Not Tested |
| BUG-LAMP-003 | Lamp | Out-of-range brightness accepted (`-5`, `150`) | Observed | Not Tested | Not Tested |

**Total: 6 issue reports covering 14 failed pytest cases** (3 OTA + 11 Lamp). IDs are local proposed identifiers; replace with issue tracker IDs when created.
