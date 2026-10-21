# Bug Reports — Firmware 1.4.0

**Test environment:** ESP32-S3 Smart Lamp DUT; UART / pytest / HIL automation; HIL camera and button/relay sensing.
**Detected on:** FW `1.4.0` (firmware stage in the latest supplied matrix run).  
**Test date:** 2026-10-21 (date the run was supplied; the console extract itself does not give wall-clock start time).  
**Evidence source:** latest pytest firmware-matrix output; suite **4 failed, 75 passed, 14 skipped, 8 deselected**.
**Reproducibility:** `1/1` in the supplied run for each listed failed parameter/case; repeated-run reproduction rates are not inferred.  
**Hardware revision / firmware build ID:** ESP32-S3 platform known; exact board revision and build identifiers not present in this run excerpt.  

> **Note:** Existing `BUG-*` IDs are retained. Regression issues use `REGRESSION-*` IDs. Classification does not by itself establish a firmware root cause. Severity/priority are proposals, not approved classifications. A pytest FAILED case is not automatically a firmware bug. HIL media can be overwritten across runs; a named file without a firmware identifier does not by itself prove the capture originated in this exact stage.

## BUG-LAMP-002 — Wi-Fi disconnected LED indication is not red after `lamp off`

| Field | Details |
|---|---|
| **ID** | `BUG-LAMP-002` |
| **Title** | Wi-Fi disconnected LED indication is not red after `lamp off` |
| **Found in** | `1.4.0` |
| **Other firmware stages in this run** | `1.3.0`: Observed, `1.5.0`: Observed |
| **Severity / Priority** | **Major / Medium (proposed)** |
| **Requirement(s)** | **FR-W6**, **FR-L1** / lamp-vs-Wi-Fi LED ownership |
| **Test Case ID** | `TC-LAMP-036` |
| **Automated test** | `tests/lamp/test_11_lamp_wifi_indication.py::test_wifi_disconnected_indication_is_restored_after_lamp_off` |
| **Category** | Physical LED indication mismatch |
| **Reproducibility** | **1 failed pytest case(s) in 1 supplied run**; no independent rerun count |

**Preconditions**

- DUT Wi-Fi is disconnected and `has_active_wifi_connection` is false.
- LED is configured to `auto`; lamp is set blue at brightness 50%, mode `solid`, and switched on.

**Steps to reproduce**

1. Call `led.auto()` and configure/enable the lamp.
2. Confirm Wi-Fi remains disconnected.
3. Execute `lamp off` and confirm state says lamp off.
4. Capture the physical LED color.

**Expected result:** After lamp off, disconnected Wi-Fi indication is red (`RGB 255,0,0`, expected HSV `(0,255,255)`).

**Actual result:** Camera detects a green/yellow-green color rather than red; HIL color verification times out.

**Evidence — UART / pytest**

```text
TimeoutError: Lamp did not reach RGB (255, 0, 0).
Expected HSV: (0, 255, 255), actual HSV: (64, 236, 178).
```


**Photo evidence — HIL camera:**

![ROI: disconnected Wi-Fi indicator observed green](../../camera/failed/wifi_disconnected_indication_after_lamp_off_255_0_0_roi.jpg)

[Debug frame](../../camera/failed/wifi_disconnected_indication_after_lamp_off_255_0_0_debug.jpg) · [ROI image](../../camera/failed/wifi_disconnected_indication_after_lamp_off_255_0_0_roi.jpg)

*Media caveat:* The shared HIL filenames are overwritten/reused across firmware suites; their source firmware cannot be determined from the filenames alone.

**Note:** The same failed scenario occurs on all three firmware stages of the supplied run. The shared media filename is reused by HIL and does **not** encode firmware; it is visual evidence of the scenario, not proof of which per-version run generated the last saved file.

---

## REGRESSION-OTA-004 — Lamp RGB configuration changes to white after OTA 1.4.0 → 1.5.0

| Field | Details |
|---|---|
| **ID** | `REGRESSION-OTA-004` |
| **Issue type** | **Regression** |
| **Title** | Lamp RGB configuration changes to white after OTA 1.4.0 → 1.5.0 |
| **Found in** | `1.4.0` |
| **Other firmware stages in this run** | `1.3.0`: Not observed on 1.3.0 → 1.4.0, `1.5.0`: Skipped — no newer firmware |
| **Severity / Priority** | **Major / High (proposed)** |
| **Requirement(s)** | **OTA-8**, **FR-L3/FR-L5/FR-L6** |
| **Test Case ID** | `TC-OTA-015` |
| **Automated test** | `tests/ota/test_06_persistence.py::test_ota_preserves_wifi_and_lamp_settings` |
| **Category** | Candidate firmware migration/persistence defect |
| **Reproducibility** | **1 failed pytest case(s) in 1 supplied run**; no independent rerun count |

**Preconditions**

- DUT starts with FW 1.4.0 `valid` and active Wi-Fi.
- Target 1.5.0 is available via OTA.

**Steps to reproduce**

1. Set RGB `(12,34,56)`, brightness `37`, mode `breathe`.
2. Confirm all settings in `lamp status`.
3. Execute `ota install 1.5.0` and wait for reboot.
4. Read `lamp status` on 1.5.0.

**Expected result:** Firmware upgrade preserves color `(12,34,56)`, brightness `37`, mode `breathe`, and saved Wi-Fi.

**Actual result:** After upgrade, `lamp status` reports color `(255,255,255)` instead of `(12,34,56)`; test fails before later setting checks.

**Evidence — UART / pytest**

```text
test_ota_preserves_wifi_and_lamp_settings
assert after.color == expected_rgb
AssertionError: assert (255, 255, 255) == (12, 34, 56)
```


**Photo/video:** Not produced by the failed assertion; it stops before photo/video verification.

**Note:** Attributed to the **1.4.0 → 1.5.0 transition**, not simply to firmware 1.4.0. A saved ROI image named `persisted_color_after_ota...` is in the passed folder, but the current failure occurs **before** camera verification, so that image is not direct evidence of this failure.

---

## REGRESSION-HIL-001 — K2 relay does not change physical HIL state during OTA although DUT logs relay ON

| Field | Details |
|---|---|
| **ID** | `REGRESSION-HIL-001` |
| **Issue type** | **Regression** |
| **Title** | K2 relay does not change physical HIL state during OTA although DUT logs relay ON |
| **Found in** | `1.4.0` |
| **Other firmware stages in this run** | `1.3.0`: Not observed (K2 test not in FAILED list), `1.5.0`: Observed |
| **Severity / Priority** | **Major / High (proposed)** |
| **Requirement(s)** | **OTA-5** (button responsiveness during download) |
| **Test Case ID** | `TC-OTA-026` |
| **Automated test** | `tests/ota/test_12_buttons.py::test_ota_physical_button_during_download[k2]` |
| **Category** | Physical output / HIL wiring or sensing — investigate |
| **Reproducibility** | **1 failed pytest case(s) in 1 supplied run**; no independent rerun count |

**Preconditions**

- DUT actively downloading a force-reinstall OTA; test has reached 10% progress.
- HIL can press K2 and read physical relay state.

**Steps to reproduce**

1. Read initial HIL relay state.
2. Start `ota install <current_version> force` and wait for 10%.
3. Press K2 using HIL.
4. Within 2 seconds, poll the HIL relay output and capture DUT UART logs.

**Expected result:** K2 changes physical relay output while download is active; OTA can continue.

**Actual result:** DUT acknowledges K2 press and logs `[K2] relay ON`, but HIL reports `OFF → OFF` and times out waiting for a physical state change.

**Evidence — UART / pytest**

```text
K2 HIL response: ['[HIL] K2 press', '[HIL] K2 release']
K2 DUT logs: ['button 2 pressed (GPIO40)', '[K2] relay ON']
K2 physical state: OFF -> OFF
TimeoutError: K2 did not change physical output during OTA.
```


**Photo/video:** No K2-specific media in this archive. UART + HIL physical-state logs are the evidence.

**Note:** Observed on 1.4.0 and 1.5.0 in this run; cannot localize root cause to firmware without independently checking relay contacts and HIL sensing. The archive contains no K2-specific photo/video, so UART and HIL state logs are the available evidence.

---

## BUG-OTA-002 — `ota-test-server` reports no-Wi-Fi error without the expected `[OTA]` prefix

| Field | Details |
|---|---|
| **ID** | `BUG-OTA-002` |
| **Title** | `ota-test-server` reports no-Wi-Fi error without the expected `[OTA]` prefix |
| **Found in** | `1.4.0` |
| **Other firmware stages in this run** | `1.3.0`: Observed, `1.5.0`: Observed |
| **Severity / Priority** | **Minor / Medium** |
| **Requirement(s)** | **OTA-7**, **OTA-12** |
| **Test Case ID** | `TC-OTA-014` |
| **Automated test** | `tests/ota/test_05_no_wifi.py::test_ota_without_wifi[ota-test-server]` |
| **Category** | Firmware CLI contract / automation parser mismatch |
| **Reproducibility** | **1 failed pytest case(s) in 1 supplied run**; no independent rerun count |

**Preconditions**

- DUT has no active Wi-Fi; UART console reachable.
- No OTA download is in progress.

**Steps to reproduce**

1. Check that the DUT is disconnected from Wi-Fi.
2. Execute `ota-test-server` via the test/controller.
3. Compare the response to the expected OTA error-message contract.

**Expected result:** The command should reject promptly with `[OTA] failed: WiFi not connected. Use 'connect' first.` (the contract currently encoded in the test/checklist).

**Actual result:** DUT does reject the operation, but emits `OTA failed:` without `[OTA]`. The controller waits 30 seconds for the prefixed form and raises `DeviceTimeoutError`.

**Evidence — UART / pytest**

```text
ota-test-server
E (961) wifi station: OTA failed: WiFi not connected. Use 'connect' first.
DeviceTimeoutError: Expected response ("[OTA] failed: WiFi not connected. Use 'connect' first.", ...) was not received within 30s.
```


**Photo/video:** No direct image/video artifact for this UART-based failure in the supplied project.

**Note:** Missing Wi-Fi rejection behavior works; the observed discrepancy is **format**, not failure to block OTA. Confirm whether the exact prefix is part of firmware requirements; otherwise change the parser rather than claiming a firmware defect.

---

## Summary

| Issue ID | Area / symptom | Number of FAILED cases | Classification |
|---|---|---:|---|
| `BUG-LAMP-002` | Wi-Fi disconnected LED indication is not red after `lamp off` | 1 | Physical LED indication mismatch |
| `REGRESSION-OTA-004` | Lamp RGB configuration changes to white after OTA 1.4.0 → 1.5.0 | 1 | Candidate firmware migration/persistence defect |
| `REGRESSION-HIL-001` | K2 relay does not change physical HIL state during OTA although DUT logs relay ON | 1 | Physical output / HIL wiring or sensing — investigate |
| `BUG-OTA-002` | `ota-test-server` reports no-Wi-Fi error without the expected `[OTA]` prefix | 1 | Firmware CLI contract / automation parser mismatch |

**Total: 4 issue records accounting for all 4 FAILED pytest cases.** These are counts of failures, not confirmed unique root causes.

## Full-run screenshots

The screenshots are included as run context, not substitutes for the quoted UART/HIL evidence.

- [Regression 1.4.0 screenshot 1](screenshots/regression%201.4.0%20%281%29.png)
- [Regression 1.4.0 screenshot 2](screenshots/regression%201.4.0%20%282%29.png)
- [Regression 1.4.0 screenshot 3](screenshots/regression%201.4.0%20%283%29.png)

![Regression 1.4.0, screenshot 1](screenshots/regression%201.4.0%20%281%29.png)

## Skipped tests (pytest summary)

- `SKIPPED [1] tests\lamp\test_05_lamp_modes.py:8: Requires firmware >= 1.5.0, current firmware is 1.4.0`
- `SKIPPED [3] tests\lamp\test_09_lamp_scenes.py:32: Requires firmware >= 1.5.0, current firmware is 1.4.0`
- `SKIPPED [1] tests\lamp\test_04_lamp_brightness.py:41: Requires firmware >= 1.5.0, current firmware is 1.4.0`
- `SKIPPED [1] tests\lamp\test_09_lamp_scenes.py:65: Requires firmware >= 1.5.0, current firmware is 1.4.0`
- `SKIPPED [1] tests\ota\test_03_update.py:52: stable update requires firmware older than 1.4.0`
- `SKIPPED [1] tests\ota\test_06_persistence.py:132: No older firmware available for 1.4.0`
- `SKIPPED [1] tests\ota\test_06_persistence.py:209: Requires firmware == 1.5.0, current firmware is 1.4.0`
- `SKIPPED [4] tests\lamp\test_09_lamp_scenes.py:91: Requires firmware >= 1.5.0, current firmware is 1.4.0`
- `SKIPPED [1] tests\ota\test_02_install.py:90: No older firmware available for 1.4.0`

**Evidence limitations:** Original raw video/photo capture timestamps and names are retained, but HIL filenames may be reused across firmware stages. No unsupported per-version media attribution or new hardware/build numbers are asserted.
