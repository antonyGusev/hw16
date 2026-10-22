# Bug–Requirement Matrix

**Source:** Latest firmware-matrix run (1.3.0 → 1.4.0 → 1.5.0), the corresponding full bug reports, and a separate post-flash startup observation for FW 1.3.0. **Run date:** October 21, 2026. Keep the reports in the same directory as this matrix.

## Defects by requirement and firmware version

| Requirement ID | Scenario / Verification | FW 1.3.0 | FW 1.4.0 | FW 1.5.0 | Regression status |
|---|---|---|---|---|---|
| OTA-9 (related) / PRD §2 | Firmware boot and UART readiness after full flash; extra power cycle required | [BUG-BOOT-001](BUG_REPORTS_FW_1.3.0.md#bug-boot-001--firmware-130-does-not-start-responding-after-flashing-until-the-device-is-rebooted) | NOT TESTED | NOT TESTED | Not established |
| FR-L2 | Named color — physical LED output | [BUG-LAMP-001](BUG_REPORTS_FW_1.3.0.md#bug-lamp-001--physical-led-colors-differ-from-named-and-explicit-rgb-commands) | PASS | PASS | No |
| FR-L3 | Arbitrary RGB — physical LED output | [BUG-LAMP-001](BUG_REPORTS_FW_1.3.0.md#bug-lamp-001--physical-led-colors-differ-from-named-and-explicit-rgb-commands) | PASS | PASS | No |
| FR-L4 | Physical LED color matches the requested value | [BUG-LAMP-001](BUG_REPORTS_FW_1.3.0.md#bug-lamp-001--physical-led-colors-differ-from-named-and-explicit-rgb-commands) | PASS | PASS | No |
| FR-L5 | Reject brightness values outside 0–100% | [BUG-LAMP-003](BUG_REPORTS_FW_1.3.0.md#bug-lamp-003--out-of-range-lamp-brightness-values-are-accepted) | PASS | PASS | No |
| FR-L5 | Active-phase `blink` brightness compared with `solid` | PASS | PASS | [REGRESSION-LAMP-004](BUG_REPORTS_FW_1.5.0.md#regression-lamp-004--blink-peak-brightness-differs-from-solid-brightness-on-fw-150-regression) | **REGRESSION: 1.5.0** |
| FR-L1 / FR-W6 | Red Wi-Fi indication after `lamp off` | [BUG-LAMP-002](BUG_REPORTS_FW_1.3.0.md#bug-lamp-002--wi-fi-disconnected-led-indication-is-not-red-after-lamp-off) | [BUG-LAMP-002](BUG_REPORTS_FW_1.4.0.md#bug-lamp-002--wi-fi-disconnected-led-indication-is-not-red-after-lamp-off) | [BUG-LAMP-002](BUG_REPORTS_FW_1.5.0.md#bug-lamp-002--wi-fi-disconnected-led-indication-is-not-red-after-lamp-off) | No — observed on all three versions |
| FR-L7 / FR-W6 | Red indication after the lamp timer expires | PASS | PASS | [REGRESSION-LAMP-005](BUG_REPORTS_FW_1.5.0.md#regression-lamp-005--red-indicator-assertion-fails-after-auto-off-timer-expires-on-fw-150) | **REGRESSION: 1.5.0** (verify Wi-Fi precondition) |
| FR-L7 | Stable color after canceling the lamp timer | PASS | PASS | [REGRESSION-LAMP-006](BUG_REPORTS_FW_1.5.0.md#regression-lamp-006--canceled-timer-test-observes-changing-led-color-on-fw-150) | **REGRESSION: 1.5.0** (verify mode isolation) |
| OTA-5 | K2 changes the physical relay state during OTA | PASS | [REGRESSION-HIL-001](BUG_REPORTS_FW_1.4.0.md#regression-hil-001--k2-relay-does-not-change-physical-hil-state-during-ota-although-dut-logs-relay-on) | [REGRESSION-HIL-001](BUG_REPORTS_FW_1.5.0.md#regression-hil-001--k2-relay-does-not-change-physical-hil-state-during-ota-although-dut-logs-relay-on) | **REGRESSION: since 1.4.0** (verify HIL) |
| OTA-6 / FR-W5 | Retry OTA after K3 interrupts Wi-Fi | [BUG-OTA-001](BUG_REPORTS_FW_1.3.0.md#bug-ota-001--ota-retry-is-blocked-after-wi-fi-interruption-via-k3) | PASS | SKIPPED (no newer FW available) | No — reproduced only on 1.3.0 |
| OTA-7 / OTA-12 | `ota-test-server` response without Wi-Fi | [BUG-OTA-002](BUG_REPORTS_FW_1.3.0.md#bug-ota-002--ota-test-server-reports-no-wi-fi-error-without-the-expected-ota-prefix) | [BUG-OTA-002](BUG_REPORTS_FW_1.4.0.md#bug-ota-002--ota-test-server-reports-no-wi-fi-error-without-the-expected-ota-prefix) | [BUG-OTA-002](BUG_REPORTS_FW_1.5.0.md#bug-ota-002--ota-test-server-reports-no-wi-fi-error-without-the-expected-ota-prefix) | No — all three versions; response contract/parser |
| OTA-8 / FR-L3 / FR-L5 / FR-L6 | Preserve lamp color and settings across OTA update | PASS (1.3→1.4) | [REGRESSION-OTA-004](BUG_REPORTS_FW_1.4.0.md#regression-ota-004--lamp-rgb-configuration-changes-to-white-after-ota-140--150) (1.4→1.5) | SKIPPED (no newer FW available) | **REGRESSION: transition to 1.5.0** |
| OTA-8 / FR-L10 | Preserve scenes after OTA firmware reinstall | N/A (scenes unsupported) | N/A (scenes unsupported) | [REGRESSION-OTA-005](BUG_REPORTS_FW_1.5.0.md#regression-ota-005--scenes-disappear-after-force-reinstall-of-firmware-150) | **REGRESSION: 1.5.0** (no comparable earlier FW) |
| OTA-11 | OTA recovery after rejection of an invalid image | [BUG-OTA-003](BUG_REPORTS_FW_1.3.0.md#bug-ota-003--ota-stays-locked-after-an-invalid-image-is-rejected) | PASS | [BUG-OTA-003](BUG_REPORTS_FW_1.5.0.md#bug-ota-003--ota-stays-locked-after-an-invalid-image-is-rejected) | **REGRESSION: recurrence in 1.5.0** |

**Requirement mapping note — BUG-BOOT-001:** The PRD has **no explicit requirement for readiness after a full UART/esptool flash**. **OTA-9** is the closest numbered requirement because it covers booting and validating a new firmware image after a reset; **PRD §2** describes the related boot/image mechanism. Neither specifies the UART-flashing scenario directly. This observed issue is therefore linked to the closest related requirement, **not** presented as a proven OTA-9 nonconformance. The issue was observed outside pytest and is not included in its FAILED count.

**Legend:** `PASS` means the associated automated test passed in the latest run (not that the entire requirement was exhaustively verified); `SKIPPED` means the test did not execute for the stated reason; `NOT TESTED` means no comparable post-flash verification was supplied; `N/A` means the feature is unavailable in that firmware version; `BUG-*` denotes an existing issue ID; `REGRESSION-*` denotes a regression issue record, while root causes involving tests or HIL may still require independent verification. **Links point to full reports for the relevant firmware version.**

## Regression bugs

All newly recorded `REGRESSION-*` issues are labeled **REGRESSION**. This classification preserves the uncertainties documented in test/HIL evidence; it does not independently prove that the root cause is firmware.

| Issue ID | Verification | Firmware comparison / result | Regression classification |
|---|---|---|---|
| [REGRESSION-LAMP-004](BUG_REPORTS_FW_1.5.0.md#regression-lamp-004--blink-peak-brightness-differs-from-solid-brightness-on-fw-150-regression) | `blink` vs `solid`: 56 vs 23 | 1.3.0 PASS; 1.4.0 PASS; 1.5.0 FAIL | **REGRESSION 1.5.0**; measurement method requires validation |
| [REGRESSION-LAMP-005](BUG_REPORTS_FW_1.5.0.md#regression-lamp-005--red-indicator-assertion-fails-after-auto-off-timer-expires-on-fw-150) | Red indication after timer expiry | 1.3.0 PASS; 1.4.0 PASS; 1.5.0 FAIL | **REGRESSION 1.5.0**; verify Wi-Fi precondition |
| [REGRESSION-LAMP-006](BUG_REPORTS_FW_1.5.0.md#regression-lamp-006--canceled-timer-test-observes-changing-led-color-on-fw-150) | Stable color after canceling timer | 1.3.0 PASS; 1.4.0 PASS; 1.5.0 FAIL | **REGRESSION 1.5.0**; verify initial lamp mode |
| [REGRESSION-OTA-004](BUG_REPORTS_FW_1.4.0.md#regression-ota-004--lamp-rgb-configuration-changes-to-white-after-ota-140--150) | RGB `(12,34,56)` → `(255,255,255)` after upgrade | 1.3.0→1.4.0 PASS; 1.4.0→1.5.0 FAIL | **REGRESSION: upgrade to 1.5.0** |
| [REGRESSION-OTA-005](BUG_REPORTS_FW_1.5.0.md#regression-ota-005--scenes-disappear-after-force-reinstall-of-firmware-150) | Scene is empty after OTA reinstall | 1.3.0/1.4.0 N/A; 1.5.0 FAIL | **REGRESSION 1.5.0**; no earlier comparable firmware |
| [REGRESSION-HIL-001](BUG_REPORTS_FW_1.4.0.md#regression-hil-001--k2-relay-does-not-change-physical-hil-state-during-ota-although-dut-logs-relay-on) · [1.5.0](BUG_REPORTS_FW_1.5.0.md#regression-hil-001--k2-relay-does-not-change-physical-hil-state-during-ota-although-dut-logs-relay-on) | K2: UART `relay ON`, HIL `OFF → OFF` | 1.3.0 PASS; 1.4.0 FAIL; 1.5.0 FAIL | **REGRESSION since 1.4.0**; verify relay state independently |
| [BUG-OTA-003](BUG_REPORTS_FW_1.5.0.md#bug-ota-003--ota-stays-locked-after-an-invalid-image-is-rejected) | OTA lock after invalid-image rejection | 1.3.0 FAIL; 1.4.0 PASS; 1.5.0 FAIL | **REGRESSION 1.5.0** (recurrence) |

Other `BUG-*` records retain their existing IDs without renaming. Evidence of test-framework issues and missing preconditions remains documented in the full reports.

## Latest run summary

| Firmware | Passed | Failed | Skipped | Documented issue records |
|---|---:|---:|---:|---:|
| 1.3.0 | 66 | 14 | 13 | 7 (including 1 post-flash observation) |
| 1.4.0 | 75 | 4 | 14 | 4 |
| 1.5.0 | 76 | 8 | 9 | 8 |

**Total:** 26 FAILED pytest cases and **13 distinct issue IDs** across the three firmware reports, including 1 additional post-flash observation outside pytest. Do not equate failed test cases with unique firmware bugs. The table excludes `deselected` tests (8 in each suite).

**Firmware-version note:** `REGRESSION-OTA-004` occurs during the 1.4.0 suite but tests the **1.4.0 → 1.5.0** transition. The matrix lists it under the 1.4.0 starting firmware with the target version noted; this does not imply that the defect necessarily belongs to firmware 1.4.0.
