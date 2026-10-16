# station_WiFi Smart Lamp + OTA --- Test Cases

## Wi-Fi

| TC ID | Requirement | Title | Preconditions | Steps | Expected Result | Automation | Automation Notes | Status |
|---|---|---|---|---|---|---|---|---|
| TC-WIFI-001 | FR-W1 | Connect using SSID name | Clean/disconnected device; target Wi-Fi network is available. | 1. Send `connect`. <br>2. Select target SSID by name. <br>3. Enter valid password. | Connection succeeds and response contains `successfully connected to SSID:<SSID>`. | Automated | UART. | Not Run |
| TC-WIFI-002 | FR-W1 | Connect using network number | Device has saved credentials and is disconnected; target SSID is present in scan results. | 1. Send `connect`. <br>2. Select target network by scan index. <br>3. Enter valid password. | Device connects successfully to the selected network. | Automated | UART; network index is resolved from scan results. | Not Run |
| TC-WIFI-003 | FR-W2 | Connect using saved credentials | Device has valid saved SSID/password and is disconnected. | 1. Send `connect` without providing new credentials. | Device connects using saved credentials and response contains `successfully connected to SSID:<SSID>`. | Automated | UART. | Not Run |
| TC-WIFI-004 | FR-W4 | Disconnect active Wi-Fi connection | Device is connected to Wi-Fi. | 1. Send `disconnect`. | Disconnect command succeeds. | Automated | UART. | Not Run |
| TC-WIFI-005 | FR-W2 | Saved credentials persist after reboot | Device has valid saved credentials; device has been rebooted and is disconnected. | 1. After reboot, send `connect` without entering new credentials. | Device reconnects successfully using saved credentials. | Automated | UART + reboot fixture. | Not Run |
| TC-WIFI-006 | FR-W4 | Status reports connected details | Device is connected to Wi-Fi. | 1. Send `status`. | Status reports connected state, expected SSID, valid IPv4 address, and RSSI value. | Automated | UART; validates SSID/IP/RSSI fields. | Not Run |
| TC-WIFI-007 | FR-W4 | Status reports disconnected state | Device has valid saved credentials but is disconnected. | 1. Send `status`. | Status reports `connected = False`. | Automated | UART. | Not Run |
| TC-WIFI-008 | FR-W4 | Scan reports RSSI and channel | Target Wi-Fi network is visible. | 1. Send `scan`. <br>2. Find configured SSID in scan results. | Target SSID is present; RSSI and channel are integers; channel is greater than 0. | Automated | UART; scan result parsing. | Not Run |
| TC-WIFI-009 | FR-W5 | K3 disconnects Wi-Fi | Device is connected to Wi-Fi; HIL button controller available. | 1. Press K3. <br>2. Poll Wi-Fi status until connection is inactive. | Device disconnects from Wi-Fi within 5 s. | Automated | HIL K3 + UART status polling. | Not Run |
| TC-WIFI-010 | FR-W5 | K3 reconnects Wi-Fi after reboot | Device has saved credentials; device has been rebooted and is disconnected; HIL available. | 1. Press K3. <br>2. Poll Wi-Fi status. | Device reconnects to configured SSID within 10 s. | Automated | HIL K3 + UART status polling. | Not Run |
| TC-WIFI-011 | FR-W5 | K3 reconnects Wi-Fi after disconnect | Device has saved credentials and is disconnected; HIL available. | 1. Press K3. <br>2. Poll Wi-Fi status. | Device reconnects to configured SSID within 10 s. | Automated | HIL K3 + UART status polling. | Not Run |
| TC-WIFI-012 | FR-W6 | Wi-Fi connected LED is green | Device is connected to Wi-Fi; HIL camera available. | 1. Observe WS2812 LED color. | WS2812 LED is detected as green. | Automated | HIL camera color detection with saved artifacts. | Not Run |
| TC-WIFI-013 | FR-W6 | Wi-Fi disconnected LED is red | Device has saved credentials but is disconnected; HIL camera available. | 1. Observe WS2812 LED color. | WS2812 LED is detected as red. | Automated | HIL camera color detection with saved artifacts. | Not Run |
| TC-WIFI-014 | FR-W1 | Reject wrong Wi-Fi password | Target SSID is available. | 1. Send `connect`. <br>2. Select target SSID. <br>3. Enter incorrect password. | Connection fails; result error is `connection_failed`; response contains `connect to the AP fail`. | Automated | UART. | Not Run |
| TC-WIFI-015 | FR-W1 | Reject password shorter than 8 characters | Target SSID is available. | 1. Send `connect`. <br>2. Select target SSID. <br>3. Enter password shorter than 8 characters. | Connection fails with `password_too_short`; response contains `password too short`; connection attempt does not start. | Automated | UART. | Not Run |
| TC-WIFI-016 | FR-W1 | Handle nonexistent SSID without losing CLI responsiveness | Device is disconnected. | 1. Attempt to connect to a nonexistent SSID using a valid-format password. <br>2. Wait for connection timeout. <br>3. Send `help`. | Connection fails with `connection_timeout`; device remains responsive and accepts `help`. | Automated | UART; validates recovery after failed connection attempt. | Not Run |
| TC-WIFI-017 | FR-W1 | Connect successfully after three failed connection attempts | Device has saved credentials and has been rebooted; device is disconnected. | 1. Connect using wrong password. <br>2. Connect using short password. <br>3. Connect to nonexistent SSID. <br>4. Connect to valid SSID with valid password. | First three attempts fail; the fourth valid attempt succeeds without DUT crash/reboot. | Automated | UART; regression test for Wi-Fi state recovery after consecutive failures. | Not Run |

## Smart Lamp

| TC ID | Requirement | Title | Preconditions | Steps | Expected Result | Automation | Automation Notes | Status |
|---|---|---|---|---|---|---|---|---|
| TC-LAMP-001 | FR-L1 / FR-L4 | Turn lamp on | Device booted; UART and HIL camera available; default lamp color is white. | 1. Send `lamp on`. <br>2. Send `lamp status`. <br>3. Observe WS2812 LED. | Response contains `[LAMP] on`; status reports lamp on with color `[255,255,255]`; physical LED is detected as white. | Automated | UART/status + HIL camera verification. | Not Run |
| TC-LAMP-002 | FR-L1 / FR-W6 | Turn lamp off | Device booted; UART and HIL camera available. | 1. Send `lamp on`. <br>2. Send `lamp off`. <br>3. Send `lamp status`. <br>4. Observe WS2812 LED. | Response contains `[LAMP] off`; status reports lamp off; physical LED is detected as red. | Automated | UART/status + HIL camera verification. | Not Run |
| TC-LAMP-003 | FR-L1 / FR-L7 / FR-W6 | Lamp is off after reboot | Lamp is on before reboot; HIL camera available. | 1. Reboot device. <br>2. Wait for boot. <br>3. Send `lamp status`. <br>4. Observe WS2812 LED. | Status reports lamp off and `timer_s = 0`; physical LED is detected as red. | Automated | UART + reboot + HIL camera verification. | Not Run |
| TC-LAMP-004 | FR-L2 / FR-L4 | Set supported named colors | Lamp is on; HIL camera/color detector available. | For each `red`, `green`, `blue`, `white`, `yellow`, `purple`, `cyan`: <br>1. Send `lamp color <name>`. <br>2. Verify command response. <br>3. Read `lamp status`. <br>4. Observe WS2812 LED. | Mappings are `red=(255,0,0)`, `green=(0,255,0)`, `blue=(0,0,255)`, `white=(255,255,255)`, `yellow=(255,180,0)`, `purple=(160,0,255)`, `cyan=(0,255,255)`; response/status and physical LED match the selected color. | Automated | Parameterized UART/status + HIL camera color verification. | Not Run |
| TC-LAMP-005 | FR-L2 | Reject unknown named color | Lamp is on; current color is known. | 1. Record `lamp status`. <br>2. Send `lamp color orange`. <br>3. Read status again. | Returns `error: unknown color 'orange'`; previous color remains unchanged. | Automated | UART/status negative test. | Not Run |
| TC-LAMP-006 | FR-L3 / FR-L4 | Set arbitrary RGB colors | Lamp is on; HIL camera/color detector available. | For each RGB value `(255,0,0)`, `(0,255,0)`, `(32,96,255)`, `(128,64,192)`, `(100,50,200)`: <br>1. Send `lamp color R G B`. <br>2. Verify response. <br>3. Read `lamp status`. <br>4. Observe WS2812 LED. | Each command returns `[LAMP] color set: (R,G,B)`; status stores the same RGB tuple; physical LED matches the configured color. | Automated | Parameterized UART/status + HIL camera color verification. | Not Run |
| TC-LAMP-007 | FR-L3 / FR-L4 | Accept RGB boundary values | Lamp is on; HIL camera available. | For `(0,0,0)` and `(255,255,255)`: <br>1. Send `lamp color R G B`. <br>2. Read `lamp status`. <br>3. Observe WS2812 LED. | Both boundary triplets are accepted and stored exactly; physical LED matches the configured boundary value. | Automated | Parameterized UART/status + HIL camera verification. | Not Run |
| TC-LAMP-008 | FR-L3 | Reject RGB values outside 0-255 | Lamp is on; current color is known. | 1. Record current status. <br>2. Send `lamp color -1 0 0`, `256 0 0`, `0 -1 0`, `0 256 0`, `0 0 -1`, and `0 0 256`. <br>3. Read status after each command. | Each command returns `error: rgb values must be 0-255`; color remains unchanged after every rejected command. | Automated | Parameterized negative UART/status test for each RGB component. | Not Run |
| TC-LAMP-009 | FR-L5 | Set brightness and verify physical levels | Lamp is on; color is set to white; mode is solid; HIL camera available. | Sequentially set brightness to `0`, `1`, `50`, and `100`; after each value verify command response/status and measure physical brightness. | Each value is accepted and reported exactly; measured physical brightness increases monotonically: `0% < 1% < 50% < 100%`. | Automated | UART/status + HIL brightness measurements. | Not Run |
| TC-LAMP-010 | FR-L5 | Accept brightness boundary values | Lamp is on; color is white; mode is solid. | 1. Set brightness to `0`. <br>2. Verify response/status. <br>3. Set brightness to `100`. <br>4. Verify response/status. | Both `0%` and `100%` are accepted and reported correctly. | Automated | Covered by `test_set_brightness` together with intermediate levels. | Not Run |
| TC-LAMP-011 | FR-L5 | Reject brightness outside 0-100 | Lamp is on; current brightness is known. | For `-5` and `150`: <br>1. Record status. <br>2. Send `lamp brightness <value>`. <br>3. Read status. | Each invalid command returns `error: brightness must be 0-100`; brightness remains unchanged. | Automated | Parameterized negative UART/status test. | Not Run |
| TC-LAMP-012 | FR-L5 | Brightness applies in all modes | Lamp is on; HIL camera/light measurement available. | 1. Set color to white and brightness to `30`. <br>2. Set `solid` and measure static brightness. <br>3. Set `blink` and measure maximum brightness for `3.0 s`. <br>4. Set `breathe` and measure maximum brightness for `7.0 s`. <br>5. On FW 1.5.0+, set `rainbow` and measure maximum brightness for `6.0 s`. | Maximum brightness in each dynamic mode matches solid-mode brightness within `10%` relative tolerance. | Automated | Rainbow parameter is version-gated for FW >= 1.5.0. | Not Run |
| TC-LAMP-013 | FR-L6 | Set solid mode | Lamp is on; HIL camera available. | 1. Send `lamp mode solid`. <br>2. Read status. <br>3. Observe the LED for stability. | Returns `[LAMP] mode set: solid`; status reports `solid`; physical color remains stable during observation. | Automated | UART/status + HIL stable-color video verification. | Not Run |
| TC-LAMP-014 | FR-L6 | Blink mode timing is 1 Hz | Lamp is on; HIL camera available. | 1. Send `lamp mode blink`. <br>2. Read status. <br>3. Observe the LED for about `3 s`. | Returns `[LAMP] mode set: blink`; status reports `blink`; at least 4 transitions are detected and each measured half-period is `0.5 s ± 0.2 s`. | Automated | HIL video timing verification. | Not Run |
| TC-LAMP-015 | FR-L6 | Breathe mode period is about 3 s | Lamp is on; HIL camera available. | 1. Send `lamp mode breathe`. <br>2. Read status. <br>3. Observe the LED for about `7 s`. | Returns `[LAMP] mode set: breathe`; status reports `breathe`; brightness pulse amplitude is at least 5% and at least one measured period is `3.0 s ± 0.8 s`. | Automated | HIL video intensity/timing verification. | Not Run |
| TC-LAMP-016 | FR-L6 | Rainbow mode works on FW 1.5.0+ | Firmware version is 1.5.0 or newer; lamp is on; HIL camera available. | 1. Send `lamp mode rainbow`. <br>2. Verify status. <br>3. Observe at least one full rainbow cycle. | Returns `[LAMP] mode set: rainbow`; status reports `rainbow`; colors cycle through the spectrum with a full cycle of approximately `5 s`. | Partial | Mode parameter is version-gated in pytest; dedicated rainbow video verification is still pending for FW 1.5.0. | Not Run |
| TC-LAMP-017 | FR-L6 | Rainbow mode is unavailable before FW 1.5.0 | Firmware version is 1.3.0 or 1.4.0; current mode is known. | 1. Record `lamp status`. <br>2. Send `lamp mode rainbow`. <br>3. Read `lamp status` again. | Rainbow mode is not enabled; command is rejected and previous mode remains unchanged. | Not Automated | Required pre-1.5 behavior is not covered by a dedicated current pytest test. | Not Run |
| TC-LAMP-018 | FR-L6 | Reject unknown lamp mode | Lamp is on; current mode is known. | 1. Record status. <br>2. Send `lamp mode disco`. <br>3. Read status. | Returns `error: unknown mode 'disco'`; previous mode remains unchanged. | Automated | UART/status negative test. | Not Run |
| TC-LAMP-019 | FR-L7 / FR-W6 | Auto-off timer expires and restores red indication | Lamp is on; HIL camera available. | 1. Send `lamp timer 1`. <br>2. Wait up to `2 s` for `[LAMP] timer expired, lamp off`. <br>3. Read status. <br>4. Observe WS2812 LED. | Initial response contains `[LAMP] auto-off in 1 s`; expiration log is received; lamp is off; `timer_s = 0`; physical LED is detected as red. | Automated | UART log/status + HIL camera verification. | Not Run |
| TC-LAMP-020 | FR-L7 | Cancel active timer | Lamp is on. | 1. Start `lamp timer 2`. <br>2. Send `lamp timer 0`. <br>3. Read status. <br>4. Observe stable lamp output for longer than the original timer period. | Returns `[LAMP] timer cancelled`; lamp remains on; `timer_s = 0`; physical color stays stable and lamp is still on after the original expiration point. | Automated | UART/status + HIL stable-color video verification. | Not Run |
| TC-LAMP-021 | FR-L7 | Accept timer boundary values | Lamp is on. | For `1` and `3600`: <br>1. Send `lamp timer N`. <br>2. Read status. <br>3. Verify `0 <= timer_s <= N` and lamp remains on. <br>4. Cancel the timer with `lamp timer 0`. | Both boundaries are accepted with `[LAMP] auto-off in N s`; cancellation returns `[LAMP] timer cancelled`; final `timer_s = 0`. | Automated | Parameterized UART/status test. | Not Run |
| TC-LAMP-022 | FR-L7 | Reject invalid timer values | Lamp is on; no timer active. | For `-1` and `3601`: <br>1. Send `lamp timer N`. <br>2. Read status. | Each command returns `error: timer must be 1-3600 s (0 = cancel)`; `timer_s` remains `0`. | Automated | Parameterized negative UART/status test. | Not Run |
| TC-LAMP-023 | FR-L7 | Reject timer when lamp is off | Lamp is off. | 1. Send `lamp timer 5`. <br>2. Read status. | Returns `error: lamp is off`; lamp remains off and `timer_s = 0`. | Automated | UART/status negative test. | Not Run |
| TC-LAMP-024 | FR-L7 | Timer does not survive reboot | Lamp is on; HIL camera available. | 1. Start `lamp timer 10`. <br>2. Reboot device before expiration. <br>3. Read `lamp status`. <br>4. Observe WS2812 LED. | After reboot lamp is off; `timer_s = 0`; physical LED is detected as red. | Automated | UART + reboot + HIL camera verification. | Not Run |
| TC-LAMP-025 | FR-L8 | Lamp status returns one valid JSON payload | Lamp is on; UART available. | 1. Send raw `lamp status`. <br>2. Select response lines beginning with `{`. <br>3. Verify exactly one JSON line. <br>4. Parse it as JSON and validate keys/types. | Exactly one JSON payload is found; keys are exactly `lamp`, `color`, `brightness`, `mode`, `timer_s`; `lamp` is string `on/off`, `color` is a 3-item integer list, and `brightness`, `timer_s` are integers while `mode` is a string. | Automated | Raw UART response + JSON parsing/schema assertions. | Not Run |
| TC-LAMP-026 | FR-L8 | Lamp status reflects configured state | Lamp is on. | 1. Set RGB to `(255,0,128)`. <br>2. Set brightness to `30`. <br>3. Set mode to `solid`. <br>4. Start `lamp timer 10`. <br>5. Read `lamp status`. <br>6. Cancel timer. | Status reports lamp on, color `(255,0,128)`, brightness `30`, mode `solid`, and `timer_s` between `8` and `10`. | Automated | UART/status validation. | Not Run |
| TC-LAMP-027 | FR-L1 / FR-L9 | Default settings on clean device | Clean freshly flashed device; no persisted lamp settings. | 1. Send `lamp status`. | Lamp is off; color is white `[255,255,255]`; brightness is `50`; mode is `solid`. | Automated | Marked `first`; currently requires manual clean-flash + physical reboot precondition because of the firmware post-flash issue. | Not Run |
| TC-LAMP-028 | FR-L9 | Lamp settings survive reboot | Lamp is on; HIL camera available. | 1. Set RGB `(12,34,56)`. <br>2. Set brightness `37`. <br>3. Set mode `breathe`. <br>4. Reboot. <br>5. Read status. <br>6. Turn lamp on. <br>7. Verify physical color and breathe behavior. | After reboot lamp is off, color remains `(12,34,56)`, brightness remains `37`, mode remains `breathe`, and `timer_s = 0`; after `lamp on`, physical color and breathe mode match the persisted settings. | Automated | UART/status + reboot + HIL camera/video verification. | Not Run |
| TC-LAMP-029 | FR-L10 | Save and load scenes 1-3 on FW 1.5.0+ | Firmware version is 1.5.0 or newer; lamp is on. | For scene 1 use `(255,0,0)`, `25%`, `solid`; scene 2 use `(0,255,0)`, `50%`, `blink`; scene 3 use `(0,0,255)`, `75%`, `breathe`. For each: <br>1. Configure values. <br>2. Save scene. <br>3. Change settings to `(1,2,3)`, `10%`, `solid`. <br>4. Load the scene. <br>5. Read status. <br>6. Verify physical LED behavior. | Save/load responses are returned and the original color/brightness/mode are restored exactly for every scene; physical output matches the loaded scene. | Partial | UART/status scene coverage is implemented and version-gated; HIL physical verification is still pending for FW 1.5.0. | Not Run |
| TC-LAMP-030 | FR-L10 | Reject invalid scene number on FW 1.5.0+ | Firmware version is 1.5.0 or newer; lamp is on. | 1. Configure scene 1 as `(12,34,56)`, `37%`, `solid` and save it. <br>2. Send `scene save 0`, `scene save 4`, `scene load 0`, and `scene load 4`. <br>3. After each rejection, change current settings to `(1,2,3)`, `10%`, `breathe`, then load scene 1. | Each invalid command returns `error: scene must be 1-3`; valid scene 1 still loads `(12,34,56)`, `37%`, `solid`. | Automated | Version-gated parameterized UART/status negative test. | Not Run |
| TC-LAMP-031 | FR-L10 | Reject loading empty scene on FW 1.5.0+ | Firmware version is 1.5.0 or newer; scene 3 is empty. | 1. Set current state to RGB `(12,34,56)`, brightness `37`, mode `solid`, timer `0`. <br>2. Record full status. <br>3. Send `scene load 3`. <br>4. Read status again. | Returns `error: scene 3 is empty`; complete lamp status remains unchanged. | Automated | Version-gated UART/status before/after comparison; marked `first` so it runs before scene-save tests in the same run. | Not Run |
| TC-LAMP-032 | FR-L10 | Scene survives reboot on FW 1.5.0+ | Firmware version is 1.5.0 or newer; lamp is on. | 1. Configure scene 1 as `(160,0,255)`, `42%`, `solid`. <br>2. Save scene 1. <br>3. Reboot. <br>4. Load scene 1. <br>5. Read status. | Scene remains stored after reboot; load response contains `[LAMP] scene 1 loaded`; status restores `(160,0,255)`, `42%`, `solid`. | Automated | Version-gated UART + reboot test. | Not Run |
| TC-LAMP-033 | FR-L10 | Scene commands are unavailable before FW 1.5.0 | Firmware version is 1.3.0 or 1.4.0; lamp is on. | For `scene save 1` and `scene load 1`: send the command. | Each command returns `error: scenes not implemented yet`. | Automated | Parameterized negative test explicitly limited to FW 1.3.0/1.4.0. | Not Run |
| TC-LAMP-034 | FR-L11 | Reject unknown lamp command | Device booted; UART available. | 1. Send `lamp blabla`. | Returns `error: unknown lamp command. See 'help'`. | Automated | UART negative test. | Not Run |
| TC-LAMP-035 | FR-W6 / Smart Lamp priority | Lamp overrides Wi-Fi and LED commands while on | Device is connected to Wi-Fi; HIL camera available. | 1. Set lamp to blue `(0,0,255)`, brightness `50`, mode `solid`, and turn it on. <br>2. Record status and verify physical blue. <br>3. Disconnect Wi-Fi. <br>4. Verify status and physical color are unchanged. <br>5. Send LED off command. <br>6. Verify status and physical color are unchanged. | While lamp is on, Wi-Fi disconnect and direct LED off command do not alter lamp status or physical blue output. | Automated | Connected-device fixture + UART/status + HIL camera verification. | Not Run |
| TC-LAMP-036 | FR-W6 / Smart Lamp priority | Wi-Fi indication is restored after lamp off | Run once with connected Wi-Fi and once with saved credentials but disconnected; LED auto mode enabled; HIL camera available. | For each Wi-Fi state: <br>1. Set lamp to blue, brightness `50`, mode `solid`, and turn it on. <br>2. Send `lamp off`. <br>3. Read status. <br>4. Observe WS2812 LED. | Lamp reports off; connected state restores green indication; disconnected state restores red indication. | Automated | Covered by separate connected and disconnected pytest tests with HIL camera verification. | Not Run |

## OTA

| TC ID | Requirement | Title | Preconditions | Steps | Expected Result | Automation | Automation Notes | Status |
|---|---|---|---|---|---|---|---|---|
| TC-OTA-001 | OTA-1 | Report firmware version, build, partition and image state | Known installed firmware. | Send `version`; parse output. | Output matches `FW: v<version> (build <date>)` and `partition: <ota_0\|ota_1> @ <address>, state: <state>`; partition and address are populated. | Automated | UART format and partition assertions. | Not Run |
| TC-OTA-002 | OTA-1 | Match firmware version across three sources | Wi-Fi connected; boot logs captured. | Read `version`; capture boot `App version`; run `ota check`. | Version values in all three sources match exactly. | Automated | UART + early boot logs. | Not Run |
| TC-OTA-003 | OTA-2 | Check stable/beta channels and update availability | Wi-Fi connected; stable and beta versions known; device can run both older-than-stable and current-stable FW. | For each baseline (older than stable; equal to stable), run `ota check`; record current/stable/beta channel versions and update availability. | Reports correct current, stable and beta versions. Below stable: `[OTA] update available. Type 'ota update'`; at stable: `[OTA] up to date (stable)`. | Automated | both `ota check` states must be asserted. | Not Run |
| TC-OTA-004 | OTA-3 | Update stable and beta channels | Wi-Fi connected; current version lower than the target version for each channel; server reachable. | Parameterized for stable and beta: run `ota update` / `ota update beta`; capture OTA, reboot and self-check; run `version`. | Correct channel firmware installed to inactive OTA partition, booted and marked `valid` for both variants. | Automated | two channel parameters. | Not Run |
| TC-OTA-005 | OTA-3 | Skip update when stable or beta already current | Wi-Fi connected; device version equals the selected stable/beta channel version. | Parameterized for stable and beta: run `ota update` / `ota update beta`; capture logs and check version/partition, transfer and reboot evidence. | For each channel: `[OTA] already up to date`; no firmware download, flash modification, partition switch or reboot. | Automated | two channel parameters. | Not Run |
| TC-OTA-006 | OTA-4 | Install specified newer version | Named newer version exists; Wi-Fi connected. | Run `ota install <ver>`; capture logs and reboot; run `version`. | Requested firmware boots from target partition and has `state: valid`. | Automated | Controlled version catalogue. | Not Run |
| TC-OTA-007 | OTA-4 | Block downgrade without force | Requested version older than current; Wi-Fi connected. | Record version and partition; run `ota install <older_ver>`; observe logs and state. | Exact `[OTA] downgrade blocked: <cur> -> <new>. Use 'ota install <ver> force'`; no download, firmware change or reboot. | Automated | Negative test; compare partition/state. | Not Run |
| TC-OTA-008 | OTA-4 | Allow forced downgrade | Older version available; Wi-Fi connected. | Run `ota install <older_ver> force`; wait through reboot; inspect `version`. | Older firmware installed successfully, state is `valid`. | Automated | UART + controlled server. | Not Run |
| TC-OTA-009 | OTA-4 | Allow forced reinstall | Current version available on server; Wi-Fi connected. | Run `ota install <current_ver> force`; capture download and reboot; run `version`. | Same-version image is actually downloaded and reinstalled; firmware boots valid. | Automated | Verify transfer rather than version alone. | Not Run |
| TC-OTA-010 | OTA-5 | Select inactive OTA partition and alternate slots | Wi-Fi connected; initial active OTA slot known; two installable images available. | Record initial partition; perform first successful OTA and verify target/active slot; perform second successful OTA and verify target/active slot; inspect `version` after each reboot. | Each OTA targets the previously inactive slot; active partitions alternate `ota_0` ↔ `ota_1` ↔ `ota_0` (or inverse); both images boot with `valid` state. | Automated | verify each of two successive installs. | Not Run |
| TC-OTA-011 | OTA-5 | Report complete download/progress/success log | Server image size known; update available. | Run successful OTA; capture complete UART output. | Logs include `current version`, `target partition`, `downloading: <url>`, `new version`, progress at each 10% from 10% to 100% with byte counts, `[OTA] success: <old> -> <new> in N s. Rebooting...`; values and byte count are consistent. | Automated | Capture UART while download occupies CLI. | Not Run |
| TC-OTA-012 | OTA-6 / FR-W5 | Recover interrupted OTA after K3 disconnect | Saved Wi-Fi credentials; HIL K3; throttled OTA download available. | Start OTA; press K3 during transfer; assert failure; reconnect to wifi; retry OTA immediately without reboot. | `[OTA] failed: download interrupted (...)`; old image remains valid and functional; subsequent OTA succeeds without intermediate DUT reboot. | Automated | Requires deterministic download window. | Not Run |
| TC-OTA-013 | OTA-6 | Recover interrupted OTA after AP outage | Controllable AP; valid OTA available. | Start OTA; disable AP while downloading; capture failure; restore AP; retry without reboot. | Interrupted-download error; current version stays operational; immediate retry works after reconnection. | Manual | Manual only: AP shutdown/restoration cannot be controlled by current HIL. | Not Run |
| TC-OTA-014 | OTA-7 | Reject every OTA command without Wi-Fi | Wi-Fi disconnected; command parser accessible; known baseline partition/version. | Parameterized: run `ota check`, `ota update`, `ota update beta`, `ota install <ver>`, `ota install <ver> force`, `ota broken`, `ota <url>`, and `ota-test-server` without reconnecting. | Every command prints exactly `[OTA] failed: WiFi not connected. Use 'connect' first.`; no download, flashing, partition switch or reboot. | Automated | Parameterized UART; include simulation command per "any OTA command". | Not Run |
| TC-OTA-015 | OTA-8 / FR-W3 | Preserve Wi-Fi and lamp after upgrade | Wi-Fi credentials stored; non-default color/brightness/mode configured; target firmware supports settings. | Record SSID and lamp values; perform successful upgrade; after reboot verify saved connection and lamp status; activate lamp for physical verification. | SSID/password still usable without re-entry; color, brightness and mode remain identical; device requires no reconfiguration. | Automated | Test persistent settings, not transient lamp on/off state. | Not Run |
| TC-OTA-016 | OTA-8 / FR-L10 | Preserve scenes after upgrade | Scene-capable source and target FW; scenes 1-3 saved with distinguishable values. | Save scenes; upgrade; load each scene after reboot; read `lamp status`. | Each saved scene restores its original color, brightness and mode. | Automated | Use FW versions with compatible scene feature. | Not Run |
| TC-OTA-017 | OTA-8 | Preserve all settings after forced downgrade | Both source and target FW support scenes; saved Wi-Fi, lamp settings and scenes exist; older target image available. | Record SSID, lamp color/brightness/mode and scenes; run forced downgrade; after boot reconnect without re-entering credentials; check lamp settings and load every saved scene. | Saved Wi-Fi credentials, lamp color/brightness/mode, and scenes survive downgrade; no reprovisioning. | Automated | If no older scene-capable version exists, mark as blocked, not passed; do not silently omit scenes. | Not Run |
| TC-OTA-018 | OTA-9 | Verify PENDING_VERIFY to VALID transition | Valid newer image available; boot UART capture configured. | Install OTA; capture first boot from reset; inspect self-check logs; send `version`. | Logs contain `[OTA] new firmware, state PENDING_VERIFY - running self-check...` then `[OTA] self-check passed, firmware marked VALID`; version points to newly activated partition and `state: valid`. | Automated | Capture initial boot from before reboot. | Not Run |
| TC-OTA-019 | OTA-10 | Rollback broken image and preserve settings | Known valid FW; Wi-Fi connected; saved credentials, lamp settings and scenes (where supported). | Record version/partition/settings; run `ota broken`; capture both boots; run `version`; validate persisted Wi-Fi, lamp and scene settings. | `self-check FAILED` then `rolling back to previous firmware...`; automatic reboot to original version AND partition with `state: valid`; settings intact. | Automated | UART + controlled reboots + persistence assertions. | Not Run |
| TC-OTA-020 | OTA-9 / OTA-10 (robustness) | Reset before firmware validation completes | New image enters PENDING_VERIFY; controllable reset with observable timing. | Start OTA; reset device before self-check confirms image; capture next boot; inspect version. | Firmware does not remain stuck or accept unverified image; bootloader rolls back to previously valid firmware when rollback conditions are met. | Automated | Additional robustness scenario; outcome depends on bootloader rollback configuration. | Not Run |
| TC-OTA-021 | OTA-5 / OTA-6 (robustness) | Power interruption during OTA download/write | HIL DUT power control; working baseline; reproducible OTA download. | Start OTA and cut DUT power at 10% progress; restore power with HIL `power_cycle`; reconnect UART; verify boot/version/partition/state. Repeat at additional download/write stages when implemented. | DUT boots functional previously valid firmware when new image has not completed validation; no unbootable state. | Automated | `test_ota_interrupt_power` in `tests/ota/test_04_interrupt.py` covers the 10% cut only; other cut points pending. | Not Run |
| TC-OTA-022 | OTA-11 | Reject invalid non-ESP32 image header | Wi-Fi connected; custom server serves deterministic non-ESP32 binary. | Record version/partition; run `ota <invalid_url>`; verify output and device responsiveness. | `[OTA] failed: invalid image header`; no switch/reboot; original version and partition remain valid. | Automated | Header-specific negative path. | Not Run |
| TC-OTA-023 | OTA-12 | Install firmware from HTTP and HTTPS URLs | Known valid firmware images served via accessible HTTP and HTTPS URLs; Wi-Fi connected. | For both schemes on controlled runs: run `ota <url>`, wait for reboot, check version/partition/state. | Correct hosted image is downloaded, boots from new slot, passes self-check and is `valid` for both URL schemes. | Automated | Parameterized HTTP/HTTPS with controlled server and cert support. | Not Run |
| TC-OTA-024 | OTA-12 | Simulate OTA without flashing firmware | Known version and partition; Wi-Fi connected. | Record firmware version, partition and image checksum if available; run `ota-test-server`; capture simulation logs and reboot; compare values after boot. | Simulation produces expected logs and reboot but no real firmware image download/write; original version/partition/image unchanged. | Automated | Use transfer or flash-write observation to prove no actual flashing. | Not Run |
| TC-OTA-025 | OTA-5 | Keep CLI occupied during OTA download | Throttled image delivery to allow reliable mid-download probe; Wi-Fi connected. | Start OTA; during download attempt another UART command; monitor response order; wait for OTA completion. | Second command is not executed concurrently with OTA download; OTA log/progress remains coherent. | Not Automated | Document actual command buffering policy before asserting whether input is ignored or delayed. | Not Run |
| TC-OTA-026 | OTA-5 | Keep physical buttons functional during OTA download | HIL button control and observable button action independent of UART; throttled OTA image. | Start download; actuate applicable non-Wi-Fi-disconnect button(s); observe physical side effect while transfer is active. | Button effects occur during download, without waiting for OTA completion; transfer can finish and reboot normally. | Not Automated | Do not use K3 disconnect as evidence that ordinary buttons remain functional. | Not Run |
| TC-OTA-027 | OTA-11 | Reject truncated or corrupted firmware image | Wi-Fi connected; server supplies known corrupted or deliberately truncated ESP32 image. | Record partition/version; run `ota <corrupt_url>`; capture validation logs; verify operation afterward. | `[OTA] failed: image validation failed (corrupted image)`; no partition switch; old FW remains valid and responsive. | Not Automated | Separate from invalid-header test; use reproducible fixture. | Not Run |

## Other Commands

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  TC ID        Requirement   Title         Preconditions     Steps                        Expected Result                                          Automation   Automation Notes Status
  ------------ ------------- ------------- ----------------- ---------------------------- -------------------------------------------------------- ------------ ---------------- --------
  TC-SYS-001   Section 6     Help lists    Device booted.    Send `help`.                 Supported command list is printed and includes command   Automated    UART parsing.    Not Run
                             supported                                                    families defined by PRD.                                                               
                             commands                                                                                                                                            

  TC-SYS-002   Section 6     Timed         HC-SR04           Send `distance 10`; collect  Distance is reported every \~0.5 s for \~10 s and then   Automated    Fully automated  Not Run
                             distance      connected; target output.                      stops.                                                                with HIL HC-SR04 
                             measurement   at known                                                                                                             emulator:        
                                           distance.                                                                                                            programmable     
                                                                                                                                                                distance and     
                                                                                                                                                                UART             
                                                                                                                                                                timing/output    
                                                                                                                                                                verification.    

  TC-SYS-003   Section 6     Continuous    HC-SR04           1\. Send                     Readings occur every \~0.5 s and stop after Enter.       Automated    UART timing;     Not Run
                             distance      connected.        `distance`.`<br>`{=html}2.                                                                         does not         
                             measurement                     Wait for several                                                                                   validate         
                             stops on                        readings.`<br>`{=html}3.                                                                           physical         
                             Enter                           Send Enter.                                                                                        accuracy.        

  TC-SYS-004   Section 6     Distance      HC-SR04 has no    Run distance measurement.    `sensor timeout` is reported and device remains          Automated    Requires HIL     Not Run
                             sensor        detectable object                              responsive.                                                           control of ECHO  
                             timeout       / echo                                                                                                               or physical      
                                           suppressed.                                                                                                          no-echo setup.   

  TC-SYS-005   Section 6     Relay UART    Relay connected.  Send `relay on`, then        UART logs `relay ON` / `relay OFF`; physical relay       Automated    Fully automated: Not Run
                             control                         `relay off`.                 contacts switch accordingly.                                          UART relay       
                                                                                                                                                                command plus     
                                                                                                                                                                independent      
                                                                                                                                                                physical COM/NO  
                                                                                                                                                                feedback on HIL  
                                                                                                                                                                GPIO32.          

  TC-SYS-006   Section 6     LED manual    Lamp off.         1\. Send                     Manual mode sets white/off and suppresses Wi-Fi          Automated    Fully automated: Not Run
                             on/off and                      `led on`.`<br>`{=html}2.     indication; auto restores Wi-Fi indication.                           UART             
                             auto mode                       Send                                                                                               command/mode     
                                                             `led off`.`<br>`{=html}3.                                                                          plus physical    
                                                             Send `led auto` under                                                                              diode state      
                                                             connected/disconnected                                                                             measured by      
                                                             Wi-Fi.                                                                                             calibrated LDR   
                                                                                                                                                                on HIL GPIO33.   

  TC-SYS-007   Section 6     LED RGB cycle Lamp off; Wi-Fi   Send `led rgb`; observe for  LED cycles colors for \~5 s, then returns to Wi-Fi auto  Manual       Automatable with Not Run
                             returns to    state known.      \>5 s.                       indication.                                                           RGB              
                             auto                                                                                                                               sensor/camera.   

  TC-SYS-008   Section 6     System        Device booted.    Send `sysinfo`.              Output includes chip, cores, frequency, flash, free      Automated    UART parsing;    Not Run
                             information                                                  memory, uptime and temperature.                                       sanity ranges    
                             command                                                                                                                            can be asserted. 

  TC-SYS-009   Section 6     Chip          Device booted.    Send `temp`.                 A chip temperature value is returned and device remains  Automated    UART parsing;    Not Run
                             temperature                                                  responsive.                                                           PRD defines no   
                             command                                                                                                                            accuracy         
                                                                                                                                                                tolerance.       

  TC-SYS-010   Section 6     Sensor status Device booted;    Send `sensor status`.        Output reports distance, relay, LED mode, Wi-Fi and      Automated    Fully automated  Not Run
                             aggregation   known                                          temperature consistently with current states.                         with independent 
                                           relay/Wi-Fi/LED                                                                                                      HIL feedback for 
                                           states.                                                                                                              distance, relay  
                                                                                                                                                                and physical LED 
                                                                                                                                                                state.           

  TC-SYS-011   Section 6     Reboot        Device booted;    Send `reboot`.               3-2-1 countdown is logged and device reboots             Automated    UART boot        Not Run
                             command       UART capture                                   successfully.                                                         detection.       
                             countdown     active.                                                                                                                               

  TC-SYS-012   Section 6     K1 starts     HIL button        Press K1 and capture UART    Distance measurement runs for about 10 s with \~0.5 s    Automated    Requires HIL     Not Run
                             10-second     control; HC-SR04  for \>10 s.                  sampling.                                                             GPIO/button      
                             distance      connected.                                                                                                           emulator.        
                             measurement                                                                                                                                         

  TC-SYS-013   Section 6     K2 toggles    HIL button        Press K2 twice.              Relay toggles state on each press.                       Automated    Fully automated: Not Run
                             relay         control; relay                                                                                                       HIL GPIO14 -\>   
                                           feedback                                                                                                             ULN2003 -\> K2,  
                                           available.                                                                                                           with physical    
                                                                                                                                                                relay COM/NO     
                                                                                                                                                                feedback on HIL  
                                                                                                                                                                GPIO32.          

  TC-SYS-014   Section 6     K4 toggles    HIL button        Press K4 twice.              GPIO4 diode toggles state on each press.                 Automated    Fully automated: Not Run
                             diode         control; diode                                                                                                       HIL GPIO15 -\>   
                                           observable.                                                                                                          ULN2003 -\> K4,  
                                                                                                                                                                with physical    
                                                                                                                                                                diode            
                                                                                                                                                                verification by  
                                                                                                                                                                calibrated LDR.  

  TC-SYS-015   Global        Unknown       Device booted.    Send an undefined top-level  `unknown command, type 'help' for available commands`;   Automated    UART only.       Not Run
                             command                         command.                     device remains responsive.                                                             
                             handling                                                                                                                                            

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 

                                                                                                                                                                                 
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Automation Summary

| Area | Total | Automated (listed) | Partial | Not Automated / Manual | Notes |
|---|---:|---:|---:|---:|---|
| Wi-Fi | 17 | 17 | 0 | 0 | Existing checklist automation classifications. |
| Smart Lamp | 36 | 33 | 2 | 1 | Preserve per-case statuses; some camera/firmware scenarios require implementation. |
| OTA | 31 | 26 | 0 | 5 | Existing 26 marked Automated; five newly added cases are Not Automated. **Implementation status must be verified against pytest.** |
| Other Commands | 15 | 14 | 0 | 1 | Existing checklist assessment. |
| **TOTAL** | **99** | **90** | **2** | **7** | Counts are checklist classifications, not evidence of executed or passing tests. |
