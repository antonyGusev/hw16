# station_WiFi Smart Lamp + OTA --- Test Cases

## Wi-Fi

| TC ID | Requirement | Title | Preconditions | Steps | Expected Result | Automation | Automation Notes | Status |
|---|---|---|---|---|---|---|---|---|
| TC-WIFI-001 | FR-W6 | Wi-Fi disconnected LED is red on clean device | Clean device; device is not connected to Wi-Fi; HIL camera available. | 1. Observe WS2812 LED color. | WS2812 LED is detected as red. | Automated | HIL camera color detection with saved artifacts. | Not Run |
| TC-WIFI-002 | FR-W1 | Connect using SSID name | Clean/disconnected device; target Wi-Fi network is available. | 1. Send `connect`. <br>2. Select target SSID by name. <br>3. Enter valid password. | Connection succeeds and response contains `successfully connected to SSID:<SSID>`. | Automated | UART. | Not Run |
| TC-WIFI-003 | FR-W1 | Connect using network number | Device has saved credentials and is disconnected; target SSID is present in scan results. | 1. Send `connect`. <br>2. Select target network by scan index. <br>3. Enter valid password. | Device connects successfully to the selected network. | Automated | UART; network index is resolved from scan results. | Not Run |
| TC-WIFI-004 | FR-W2 | Connect using saved credentials | Device has valid saved SSID/password and is disconnected. | 1. Send `connect` without providing new credentials. | Device connects using saved credentials and response contains `successfully connected to SSID:<SSID>`. | Automated | UART. | Not Run |
| TC-WIFI-005 | FR-W4 | Disconnect active Wi-Fi connection | Device is connected to Wi-Fi. | 1. Send `disconnect`. | Disconnect command succeeds. | Automated | UART. | Not Run |
| TC-WIFI-006 | FR-W2 | Saved credentials persist after reboot | Device has valid saved credentials; device has been rebooted and is disconnected. | 1. After reboot, send `connect` without entering new credentials. | Device reconnects successfully using saved credentials. | Automated | UART + reboot fixture. | Not Run |
| TC-WIFI-007 | FR-W4 | Status reports connected details | Device is connected to Wi-Fi. | 1. Send `status`. | Status reports connected state, expected SSID, valid IPv4 address, and RSSI value. | Automated | UART; validates SSID/IP/RSSI fields. | Not Run |
| TC-WIFI-008 | FR-W4 | Status reports disconnected state | Device has valid saved credentials but is disconnected. | 1. Send `status`. | Status reports `connected = False`. | Automated | UART. | Not Run |
| TC-WIFI-009 | FR-W4 | Scan reports RSSI and channel | Target Wi-Fi network is visible. | 1. Send `scan`. <br>2. Find configured SSID in scan results. | Target SSID is present; RSSI and channel are integers; channel is greater than 0. | Automated | UART; scan result parsing. | Not Run |
| TC-WIFI-010 | FR-W5 | K3 disconnects Wi-Fi | Device is connected to Wi-Fi; HIL button controller available. | 1. Press K3. <br>2. Poll Wi-Fi status until connection is inactive. | Device disconnects from Wi-Fi within 5 s. | Automated | HIL K3 + UART status polling. | Not Run |
| TC-WIFI-011 | FR-W5 | K3 reconnects Wi-Fi after reboot | Device has saved credentials; device has been rebooted and is disconnected; HIL available. | 1. Press K3. <br>2. Poll Wi-Fi status. | Device reconnects to configured SSID within 10 s. | Automated | HIL K3 + UART status polling. | Not Run |
| TC-WIFI-012 | FR-W5 | K3 reconnects Wi-Fi after disconnect | Device has saved credentials and is disconnected; HIL available. | 1. Press K3. <br>2. Poll Wi-Fi status. | Device reconnects to configured SSID within 10 s. | Automated | HIL K3 + UART status polling. | Not Run |
| TC-WIFI-013 | FR-W6 | Wi-Fi connected LED is green | Device is connected to Wi-Fi; HIL camera available. | 1. Observe WS2812 LED color. | WS2812 LED is detected as green. | Automated | HIL camera color detection with saved artifacts. | Not Run |
| TC-WIFI-014 | FR-W6 | Wi-Fi disconnected LED is red | Device has saved credentials but is disconnected; HIL camera available. | 1. Observe WS2812 LED color. | WS2812 LED is detected as red. | Automated | HIL camera color detection with saved artifacts. | Not Run |
| TC-WIFI-015 | FR-W1 | Reject wrong Wi-Fi password | Target SSID is available. | 1. Send `connect`. <br>2. Select target SSID. <br>3. Enter incorrect password. | Connection fails; result error is `connection_failed`; response contains `connect to the AP fail`. | Automated | UART. | Not Run |
| TC-WIFI-016 | FR-W1 | Reject password shorter than 8 characters | Target SSID is available. | 1. Send `connect`. <br>2. Select target SSID. <br>3. Enter password shorter than 8 characters. | Connection fails with `password_too_short`; response contains `password too short`; connection attempt does not start. | Automated | UART. | Not Run |
| TC-WIFI-017 | FR-W1 | Handle nonexistent SSID without losing CLI responsiveness | Device is disconnected. | 1. Attempt to connect to a nonexistent SSID using a valid-format password. <br>2. Wait for connection timeout. <br>3. Send `help`. | Connection fails with `connection_timeout`; device remains responsive and accepts `help`. | Automated | UART; validates recovery after failed connection attempt. | Not Run |
| TC-WIFI-018 | FR-W1 | Connect successfully after three failed connection attempts | Device has saved credentials and has been rebooted; device is disconnected. | 1. Connect using wrong password. <br>2. Connect using short password. <br>3. Connect to nonexistent SSID. <br>4. Connect to valid SSID with valid password. | First three attempts fail; the fourth valid attempt succeeds without DUT crash/reboot. | Automated | UART; regression test for Wi-Fi state recovery after consecutive failures. | Not Run |

## Smart Lamp

| TC ID       | Requirement                 | Title                                           | Preconditions                                                                              | Steps                                                                                                                                             | Expected Result                                                                                                                  | Automation | Automation Notes                                                  | Status  |
| ----------- | --------------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ---------- | ----------------------------------------------------------------- | ------- |
| TC-LAMP-001 | FR-L1                       | Turn lamp on and off                            | Device booted; UART available.                                                             | 1. Send `lamp on`. <br>2. Send `lamp status`. <br>3. Verify physical LED is controlled by lamp. <br>4. Send `lamp off`. <br>5. Send `lamp status`. | `lamp on` returns `[LAMP] on` and status reports `"lamp":"on"`; `lamp off` returns `[LAMP] off` and status reports `"lamp":"off"`. | Automated  | UART + status; physical LED behavior is HIL-verified.              | Not Run |
| TC-LAMP-002 | FR-L1                       | Lamp is always off after reboot                 | Lamp is on before reboot.                                                                  | 1. Reboot device. <br>2. Wait for boot. <br>3. Send `lamp status`.                                                                                | Status reports `"lamp":"off"` after reboot.                                                                                      | Automated  | UART + reboot fixture.                                            | Not Run |
| TC-LAMP-003 | FR-L2                       | Set supported named colors                      | Lamp is on.                                                                                | For each `red`, `green`, `blue`, `white`, `yellow`, `purple`, `cyan`: <br>1. Send `lamp color <name>`. <br>2. Read `lamp status`.                 | Command returns `[LAMP] color set: <name> (r,g,b)` with the specified mapping; status contains the same RGB values.              | Automated  | Parameterized UART/status test.                                   | Not Run |
| TC-LAMP-004 | FR-L2                       | Reject unknown named color                      | Lamp is on; current color is known.                                                        | 1. Record `lamp status`. <br>2. Send `lamp color orange`. <br>3. Read status again.                                                               | Returns `error: unknown color 'orange'`; previous color remains unchanged.                                                       | Automated  | UART; validates state is not modified.                            | Not Run |
| TC-LAMP-005 | FR-L3                       | Set arbitrary RGB color                         | Lamp is on.                                                                                | 1. Send `lamp color 255 0 128`. <br>2. Read `lamp status`.                                                                                        | Returns `[LAMP] color set: (255,0,128)`; status contains `[255,0,128]`.                                                          | Automated  | UART/status validation.                                           | Not Run |
| TC-LAMP-006 | FR-L3                       | Accept RGB boundary values                      | Lamp is on.                                                                                | 1. Set `lamp color 0 0 0`. <br>2. Verify status. <br>3. Set `lamp color 255 255 255`. <br>4. Verify status.                                       | Both boundary RGB triplets are accepted and stored exactly.                                                                      | Automated  | Parameterized UART/status test.                                   | Not Run |
| TC-LAMP-007 | FR-L3                       | Reject RGB values outside 0-255                 | Lamp is on; current color is known.                                                        | 1. Record current status. <br>2. Send `lamp color -1 0 0`, `256 0 0`, `0 -1 0`, `0 256 0`, `0 0 -1`, and `0 0 256`. <br>3. Read status after each command. | Each command returns `error: rgb values must be 0-255`; color remains unchanged after every rejected command.                    | Automated  | Parameterized negative UART/status test for each RGB component.   | Not Run |
| TC-LAMP-008 | FR-L4                       | Physical LED matches named color                | Lamp is on; HIL camera/color detector available.                                           | For each supported named color: <br>1. Set color. <br>2. Observe WS2812 LED.                                                                      | Physical LED color corresponds to the selected named color.                                                                      | Automated  | HIL camera/color detection.                                       | Not Run |
| TC-LAMP-009 | FR-L4                       | Physical LED matches arbitrary RGB color        | Lamp is on; HIL camera/color detector available.                                           | 1. Send `lamp color 255 0 128`. <br>2. Observe WS2812 LED.                                                                                        | Physical LED output corresponds to the configured RGB color within detector tolerance.                                           | Automated  | HIL camera/color detection.                                       | Not Run |
| TC-LAMP-010 | FR-L5                       | Set brightness                                  | Lamp is on.                                                                                | 1. Send `lamp brightness 30`. <br>2. Read `lamp status`.                                                                                          | Returns `[LAMP] brightness set: 30%`; status reports `"brightness":30`.                                                          | Automated  | UART/status validation.                                           | Not Run |
| TC-LAMP-011 | FR-L5                       | Accept brightness boundary values               | Lamp is on.                                                                                | 1. Set brightness to `0`. <br>2. Verify status. <br>3. Set brightness to `100`. <br>4. Verify status.                                             | Both `0%` and `100%` are accepted and reported correctly.                                                                        | Automated  | Parameterized UART/status test.                                   | Not Run |
| TC-LAMP-012 | FR-L5                       | Reject brightness outside 0-100                 | Lamp is on; current brightness is known.                                                   | 1. Record status. <br>2. Send `lamp brightness -5`. <br>3. Send `lamp brightness 150`. <br>4. Read status after each.                             | Each invalid command returns `error: brightness must be 0-100`; brightness remains unchanged.                                    | Automated  | Parameterized negative UART/status test.                          | Not Run |
| TC-LAMP-013 | FR-L5                       | Brightness applies in all modes                 | Lamp is on; HIL camera/light measurement available.                                        | 1. Set a non-default brightness. <br>2. Run `solid`, `blink`, `breathe`, and `rainbow` where supported. <br>3. Measure intensity in the active/maximum phase of each mode. | `solid` intensity matches configured brightness; `blink` ON phase matches configured brightness; `breathe` maximum matches configured brightness; `rainbow` is rendered at the configured brightness. | Automated  | HIL optical measurement with agreed sensor tolerance; rainbow only on FW >= 1.5.0. | Not Run |
| TC-LAMP-014 | FR-L6                       | Set solid mode                                  | Lamp is on.                                                                                | 1. Send `lamp mode solid`. <br>2. Read status.                                                                                                    | Returns `[LAMP] mode set: solid`; status reports `"mode":"solid"`; LED is steady.                                                | Automated  | UART/status + HIL observation.                                    | Not Run |
| TC-LAMP-015 | FR-L6                       | Blink mode timing is 1 Hz                       | Lamp is on; HIL camera/light sensor available.                                             | 1. Send `lamp mode blink`. <br>2. Observe and measure multiple ON/OFF cycles.                                                                      | Returns `[LAMP] mode set: blink`; measured ON and OFF durations are each approximately 0.5 s and satisfy the agreed timing tolerance. | Automated  | HIL timing measurement; acceptance tolerance must be defined by the test environment/specification. | Not Run |
| TC-LAMP-016 | FR-L6                       | Breathe mode period is about 3 s                | Lamp is on; HIL camera/light sensor available.                                             | 1. Send `lamp mode breathe`. <br>2. Observe and measure multiple full pulse cycles.                                                                | Returns `[LAMP] mode set: breathe`; LED pulses smoothly and measured period is approximately 3 s within the agreed timing tolerance. | Automated  | HIL timing/intensity measurement; tolerance must be defined by the test environment/specification. | Not Run |
| TC-LAMP-017 | FR-L6                       | Rainbow mode works on FW 1.5.0+                 | Firmware version is 1.5.0 or newer; lamp is on; HIL camera available.                      | 1. Send `lamp mode rainbow`. <br>2. Observe and measure at least one full color cycle.                                                             | Returns `[LAMP] mode set: rainbow`; colors change smoothly around the spectrum and full-cycle duration is approximately 5 s within the agreed timing tolerance. | Automated  | Version-gated HIL timing/color test; tolerance must be defined by the test environment/specification. | Not Run |
| TC-LAMP-018 | FR-L6                       | Rainbow mode is rejected on FW 1.3.0/1.4.0      | Firmware version is 1.3.0 or 1.4.0.                                                        | 1. Send `lamp mode rainbow`.                                                                                                                      | Returns `error: mode 'rainbow' not implemented yet`.                                                                             | Automated  | Version-gated UART negative test.                                 | Not Run |
| TC-LAMP-019 | FR-L6                       | Reject unknown lamp mode                        | Lamp is on; current mode is known.                                                         | 1. Record status. <br>2. Send `lamp mode disco`. <br>3. Read status.                                                                              | Returns `error: unknown mode 'disco'`; previous mode remains unchanged.                                                          | Automated  | UART/status validation.                                           | Not Run |
| TC-LAMP-020 | FR-L7                       | Auto-off timer expires                          | Lamp is on.                                                                                | 1. Send `lamp timer 5`. <br>2. Wait for expiration. <br>3. Read `lamp status`.                                                                    | Returns `[LAMP] auto-off in 5 s`, then `[LAMP] timer expired, lamp off`; status reports `"lamp":"off"` with `timer_s:0`.          | Automated  | UART + timed status polling. Physical LED restoration is covered by TC-LAMP-026. | Not Run |
| TC-LAMP-021 | FR-L7                       | Cancel active timer                             | Lamp is on with an active timer.                                                           | 1. Send `lamp timer 0`. <br>2. Read status. <br>3. Wait past the original expiration time.                                                        | Returns `[LAMP] timer cancelled`; `timer_s` becomes `0`; lamp does not auto-off from the cancelled timer.                        | Automated  | UART/status + timing.                                             | Not Run |
| TC-LAMP-022 | FR-L7                       | Accept timer boundary values                    | Lamp is on.                                                                                | 1. Send `lamp timer 1`. <br>2. Verify acceptance. <br>3. Turn lamp on again if needed. <br>4. Send `lamp timer 3600`.                             | Both boundary values are accepted with `[LAMP] auto-off in N s`.                                                                 | Automated  | Parameterized UART test; cancel 3600 s timer after validation.    | Not Run |
| TC-LAMP-023 | FR-L7                       | Reject invalid timer values                     | Lamp is on; no timer active.                                                               | 1. Send `lamp timer -1`, `lamp timer 3601`, and `lamp timer 5000`. <br>2. Read status after each command.                                         | Each command returns `error: timer must be 1-3600 s (0 = cancel)`; `timer_s` remains `0` and no invalid timer starts.            | Automated  | Parameterized negative UART/status test with boundary-invalid values. | Not Run |
| TC-LAMP-024 | FR-L7                       | Reject timer when lamp is off                   | Lamp is off.                                                                               | 1. Send `lamp timer 5`.                                                                                                                           | Returns `error: lamp is off`; timer is not started.                                                                              | Automated  | UART negative test.                                               | Not Run |
| TC-LAMP-025 | FR-L7                       | Timer does not survive reboot                   | Lamp is on with an active timer.                                                           | 1. Start a timer long enough to reboot before expiration. <br>2. Wait briefly. <br>3. Reboot before it expires. <br>4. Read `lamp status`. <br>5. Send `lamp on`. <br>6. Wait longer than the timer's remaining pre-reboot duration. <br>7. Read `lamp status` and monitor UART. | After reboot lamp is off and `timer_s` is `0`; after turning the lamp on again it remains on past the old expiration point and no stale `[LAMP] timer expired` event occurs. | Automated  | UART + reboot fixture + timed observation.                        | Not Run |
| TC-LAMP-026 | FR-L7 / FR-W6               | Wi-Fi indication returns after timer expiration | Lamp is on with a short timer; Wi-Fi state is known; HIL camera available.                 | 1. Start short timer. <br>2. Wait for expiration. <br>3. Observe WS2812 LED.                                                                      | After lamp auto-off, WS2812 returns to the correct Wi-Fi indication for the current Wi-Fi state.                                 | Automated  | HIL camera + UART/status.                                         | Not Run |
| TC-LAMP-027 | FR-L8                       | Lamp status returns one valid JSON line         | Device booted; UART available.                                                             | 1. Send `lamp status`. <br>2. Capture the complete command response. <br>3. Verify exactly one response line is returned. <br>4. Parse that line as JSON. | Exactly one response line containing one valid JSON object is returned with keys `lamp`, `color`, `brightness`, `mode`, and `timer_s` using expected data types. | Automated  | UART framing + JSON parsing/schema assertions.                    | Not Run |
| TC-LAMP-028 | FR-L8                       | Lamp status reflects configured state           | Lamp is on.                                                                                | 1. Set known color, brightness, and mode. <br>2. Start `lamp timer 10`. <br>3. Send `lamp status` and record `timer_s`. <br>4. Wait about 2 s. <br>5. Send `lamp status` again. | JSON values match the configured logical state; first `timer_s` is close to 10, second value is lower by approximately the elapsed time, and both remain consistent with the active timer. | Automated  | UART/status validation with timer countdown tolerance.            | Not Run |
| TC-LAMP-029 | FR-L8                       | Lamp status matches physical LED behavior       | Lamp is on; HIL camera/light sensor available.                                             | 1. Configure a known state. <br>2. Read `lamp status`. <br>3. Observe physical LED.                                                               | JSON state corresponds to what the LED is physically doing.                                                                      | Automated  | UART + HIL correlation.                                           | Not Run |
| TC-LAMP-030 | FR-L9                       | Default settings on clean device                | Clean freshly flashed device; no lamp settings in NVS.                                     | 1. Send `lamp status`.                                                                                                                            | Defaults are color `white` = `[255,255,255]`, brightness `50`, mode `solid`; lamp itself is off.                                 | Automated  | UART/status; requires clean device at test-run start.             | Not Run |
| TC-LAMP-031 | FR-L9                       | Each lamp setting survives reboot               | Device is available for reboot testing.                                                    | For each setting independently: <br>1. Set one non-default value (`color`, `brightness`, or `mode`) while keeping the others known. <br>2. Reboot immediately after the change. <br>3. Read `lamp status`. <br>4. Send `lamp on`. | Lamp is off immediately after every reboot; the just-changed setting is restored from NVS and applied correctly. Color, brightness, and mode persistence are each verified independently. | Automated  | Parameterized UART + reboot fixture; proves immediate per-setting NVS persistence. | Not Run |
| TC-LAMP-032 | FR-L9                       | Lamp settings survive OTA update                | Device has non-default color, brightness, and mode; defined source and target FW versions are available for OTA. | 1. Record source FW version and lamp settings. <br>2. Perform OTA to the defined target FW version. <br>3. Read status after boot. <br>4. Turn lamp on. | Saved color, brightness, and mode survive OTA and are applied after `lamp on`; lamp is off immediately after reboot.             | Automated  | OTA regression suite + UART; source→target FW pair must be explicit in test data. | Not Run |
| TC-LAMP-033 | FR-L10                      | Save and load scenes 1-3 on FW 1.5.0+           | Firmware version is 1.5.0 or newer; lamp settings are known.                               | For each scene `1`, `2`, and `3`: <br>1. Set known color/brightness/mode. <br>2. Send `lamp scene save <N>`. <br>3. Change settings. <br>4. Send `lamp scene load <N>`. <br>5. Read status. | For every scene slot, returns `[LAMP] scene N saved` and `[LAMP] scene N loaded`; the saved color/brightness/mode are restored exactly. | Automated  | Parameterized UART/status test for scene IDs 1, 2, and 3.         | Not Run |
| TC-LAMP-034 | FR-L10                      | Reject invalid scene number on FW 1.5.0+        | Firmware version is 1.5.0 or newer; at least one valid scene contains known settings.      | 1. Record the known valid scene contents/state. <br>2. Send `lamp scene save 0`, `save 4`, `load 0`, and `load 4`. <br>3. Re-load the known valid scene and read status. | Each invalid command returns `error: scene must be 1-3`; the known valid scene remains unchanged and still restores its original settings. | Automated  | Parameterized UART/status negative test using boundary-invalid scene IDs. | Not Run |
| TC-LAMP-035 | FR-L10                      | Reject loading empty scene on FW 1.5.0+         | Firmware version is 1.5.0 or newer; selected scene slot is empty.                          | 1. Set and record known current color/brightness/mode. <br>2. Send `lamp scene load 2`. <br>3. Read `lamp status`.                                | Returns `error: scene 2 is empty`; color, brightness, and mode remain exactly unchanged.                                         | Automated  | UART/status negative test with before/after state comparison.     | Not Run |
| TC-LAMP-036 | FR-L10                      | Scenes survive reboot on FW 1.5.0+              | Firmware version is 1.5.0 or newer; scene 1 contains known settings.                       | 1. Reboot device. <br>2. Send `lamp scene load 1`. <br>3. Read status.                                                                            | Scene remains stored in NVS and loads the previously saved color/brightness/mode.                                                | Automated  | UART + reboot fixture.                                            | Not Run |
| TC-LAMP-037 | FR-L10                      | Scenes survive OTA on FW 1.5.0+                 | Source firmware is 1.5.0 or newer; scene 1 contains known settings; defined newer target FW is available. | 1. Record source FW and scene contents. <br>2. Perform OTA to the newer target FW. <br>3. Send `lamp scene load 1`. <br>4. Read status.            | Saved scene survives OTA and restores the expected color/brightness/mode.                                                        | Automated  | OTA regression suite + UART; use a source FW where scenes already exist. | Not Run |
| TC-LAMP-038 | FR-L10                      | Scene commands are rejected on FW 1.3.0/1.4.0   | Firmware version is 1.3.0 or 1.4.0.                                                        | For each command `lamp scene save 1` and `lamp scene load 1`: <br>1. Send the command. <br>2. Verify the response.                               | Each command independently returns `error: scenes not implemented yet`.                                                          | Automated  | Version-gated parameterized UART negative test.                   | Not Run |
| TC-LAMP-039 | FR-L11                      | Reject unknown lamp command                     | Device booted; UART available.                                                             | 1. Send `lamp blabla`.                                                                                                                            | Returns `error: unknown lamp command. See 'help'`.                                                                               | Automated  | UART negative test.                                               | Not Run |
| TC-LAMP-040 | FR-W6 / Smart Lamp priority | Lamp overrides Wi-Fi and led commands while on  | Lamp is on with known visible output; Wi-Fi state is known.                                | 1. Set lamp to a known visible color/brightness/mode. <br>2. Trigger a Wi-Fi state change. <br>3. Verify physical LED and lamp status remain unchanged. <br>4. Issue a supported `led ...` command. <br>5. Verify physical LED and lamp status remain unchanged. | While lamp is on, neither Wi-Fi indication changes nor direct `led ...` commands alter the lamp-controlled LED output or lamp state. | Automated  | UART + HIL physical LED verification.                             | Not Run |
| TC-LAMP-041 | FR-W6 / Smart Lamp priority | Wi-Fi indication is restored after lamp off     | Lamp is on; current Wi-Fi state is known; HIL camera available.                            | 1. Send `lamp off`. <br>2. Read `lamp status`. <br>3. Observe WS2812 LED.                                                                         | Returns `[LAMP] off`; status reports `"lamp":"off"`; lamp releases the LED and the correct Wi-Fi indication for the current Wi-Fi state becomes visible. | Automated  | UART/status + HIL physical LED verification.                      | Not Run |

## OTA

  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  TC ID        Requirement   Title                 Preconditions        Steps                                        Expected Result                                Automation   Automation Notes          Status
  ------------ ------------- --------------------- -------------------- -------------------------------------------- ---------------------------------------------- ------------ ------------------------- --------
  TC-OTA-001   OTA-1         Version command       Device running known Send `version`.                              Output contains FW version/build plus active   Automated    UART parsing.             Not Run
                             reports version,      firmware.                                                         ota_0/ota_1 address and image state.                                                  
                             partition and state                                                                                                                                                           

  TC-OTA-002   OTA-1         Version consistency   Device running known Compare `version`, boot `App version`, and   All three version values are identical.        Automated    UART parsing.             Not Run
                             across sources        firmware and         `ota check` current version.                                                                                                       
                                                   connected to Wi-Fi.                                                                                                                                     

  TC-OTA-003   OTA-2         OTA check reports     Wi-Fi connected; OTA Send `ota check`.                            Current, stable and beta versions are printed  Automated    Requires internet/test    Not Run
                             stable and beta       server reachable.                                                 and update/up-to-date status is correct.                    server.                   
                             channels                                                                                                                                                                      

  TC-OTA-004   OTA-3         Update to stable      Device on version    Send `ota update`; wait through reboot; send Stable image downloads, installs to inactive   Automated    UART + network + reboot   Not Run
                             channel               older than stable;   `version`.                                   partition, reboots, self-check passes and new               handling.                 
                                                   Wi-Fi connected.                                                  stable version is valid.                                                              

  TC-OTA-005   OTA-3         Update to beta        Device below beta;   Send `ota update beta`; wait through reboot; Beta image installs successfully and becomes   Automated    UART + network.           Not Run
                             channel               Wi-Fi connected.     send `version`.                              valid after self-check.                                                               

  TC-OTA-006   OTA-3         Already up to date    Device already on    Send `ota update` and monitor logs/network.  `[OTA] already up to date`; no firmware        Automated    UART sufficient; network  Not Run
                             does not download     current stable.                                                   download or reboot occurs.                                  capture optional.         

  TC-OTA-007   OTA-4         Install a specific    Wi-Fi connected;     Send `ota install <ver>`; wait for reboot;   Requested version becomes active and valid.    Automated    UART + server.            Not Run
                             newer version         requested version    check version.                                                                                                                     
                                                   exists and is newer.                                                                                                                                    

  TC-OTA-008   OTA-4         Block downgrade       Current version      Send `ota install <older_ver>`.              Downgrade blocked message is logged; no        Automated    UART only after setup.    Not Run
                             without force         newer than requested                                              firmware change/reboot.                                                               
                                                   version.                                                                                                                                                

  TC-OTA-009   OTA-4         Allow forced          Current version      Send `ota install <older_ver> force`; wait   Older version installs, boots, passes          Automated    UART + server.            Not Run
                             downgrade             newer than requested through reboot.                              self-check and becomes valid.                                                         
                                                   existing version.                                                                                                                                       

  TC-OTA-010   OTA-4         Allow forced          Current version      Send `ota install <current_ver> force`; wait Same version is downloaded/reinstalled and     Automated    UART + server.            Not Run
                             reinstall of same     available on server. through reboot.                              boots valid according to force policy.                                                
                             version                                                                                                                                                                       

  TC-OTA-011   OTA-5         OTA logs target       Device running from  1\. Record active partition using            Target partition is the inactive slot: ota_0   Automated    UART parsing.             Not Run
                             inactive partition    known active OTA     `version`.`<br>`{=html}2. Start              -\> ota_1 or ota_1 -\> ota_0.                                                         
                                                   slot; Wi-Fi          OTA.`<br>`{=html}3. Capture                                                                                                        
                                                   connected.           `target partition`.                                                                                                                

  TC-OTA-012   OTA-5         OTA progress and      Update available;    Start OTA and capture full log.              Log includes current version, target           Automated    UART parsing with         Not Run
                             success logging       Wi-Fi connected.                                                  partition, URL, new version, progress at 10%                tolerant timing.          
                                                                                                                     increments, success old-\>new with duration,                                          
                                                                                                                     and reboot.                                                                           

  TC-OTA-013   OTA-6 / FR-W5 Interrupt OTA using   Saved credentials    1\. Start OTA.`<br>`{=html}2. During         Download fails as interrupted; current         Automated    Requires HIL GPIO/button  Not Run
                             K3 Wi-Fi disconnect   exist; Wi-Fi         download press K3.`<br>`{=html}3. Observe    firmware remains operational; retry works                   emulator and sufficiently 
                                                   connected; update    failure.`<br>`{=html}4. Reconnect with       immediately after reconnect without device                  controllable download     
                                                   available; HIL       K3.`<br>`{=html}5. Retry OTA without reboot. reboot.                                                     timing.                   
                                                   button control.                                                                                                                                         

  TC-OTA-014   OTA-6         Network loss during   Wi-Fi connected;     1\. Start OTA.`<br>`{=html}2. Disable        Interrupted-download failure is logged; old    Automated    Requires controllable     Not Run
                             OTA download          update available;    AP/network during download.`<br>`{=html}3.   firmware remains active; next OTA attempt                   AP/router.                
                                                   controllable AP.     Restore network.`<br>`{=html}4. Retry OTA    succeeds without reboot.                                                              
                                                                        without reboot.                                                                                                                    

  TC-OTA-015   OTA-7         Reject OTA commands   Wi-Fi disconnected.  Run `ota check`, `ota update`,               Each applicable OTA command fails with         Automated    UART only.                Not Run
                             without Wi-Fi                              `ota update beta`, `ota install <ver>` and   `WiFi not connected. Use 'connect' first.`;                                           
                                                                        custom URL OTA.                              firmware unchanged.                                                                   

  TC-OTA-016   OTA-8 / FR-W3 Preserve Wi-Fi and    Saved Wi-Fi          Perform successful upgrade; after reboot     Wi-Fi credentials and lamp                     Automated    UART + OTA.               Not Run
               / FR-L9       lamp settings across  credentials and      inspect saved settings and reconnect using   color/brightness/mode remain stored.                                                  
                             upgrade               non-default lamp     saved credentials.                                                                                                                 
                                                   settings exist.                                                                                                                                         

  TC-OTA-017   OTA-8 /       Preserve scenes       Firmware/scenario    Perform successful OTA to a version that     Scenes remain stored and restore correct       Automated    Applicable where both     Not Run
               FR-L10        across OTA            supports scenes;     supports scenes; load saved scenes           settings.                                                   source/target support     
                                                   scenes saved.        afterward.                                                                                               scene storage semantics.  

  TC-OTA-018   OTA-8         Preserve data across  Saved Wi-Fi/lamp     Perform forced downgrade; verify settings    Persistent settings remain; update does not    Automated    Scene behavior may be     Not Run
                             forced downgrade      data exist; target   supported by target version.                 require reprovisioning.                                     version-dependent; only   
                                                   older version                                                                                                                 assert features supported 
                                                   exists.                                                                                                                       by target.                

  TC-OTA-019   OTA-9         New image enters      Valid update         Perform OTA and capture first boot log; then First boot logs PENDING_VERIFY self-check,     Automated    UART must                 Not Run
                             pending verify and    available.           send `version`.                              then self-check passed/marked VALID; version                reconnect/capture early   
                             becomes valid                                                                           reports state valid.                                        boot logs.                

  TC-OTA-020   OTA-10        Rollback from         Wi-Fi connected;     1\. Record current                           Broken image fails self-check, rollback occurs Automated    UART + reboot handling.   Not Run
                             intentionally broken  known valid current  version/partition/settings.`<br>`{=html}2.   automatically, previous version/partition                                             
                             firmware              version.             Send `ota broken`.`<br>`{=html}3. Capture    becomes active and valid, settings remain.                                            
                                                                        reboot/rollback logs.`<br>`{=html}4. Send                                                                                          
                                                                        `version` after recovery.                                                                                                          

  TC-OTA-021   OTA rollback  Reset before new      Valid update image   1\. Start OTA and allow reboot into new      Bootloader rolls back to previous valid        Automated    Requires precise HIL      Not Run
               mechanics     image confirms itself available; HIL       image.`<br>`{=html}2. Reset/power-cycle      firmware because new image did not confirm                  reset/power control and   
                                                   power/reset control. while image is PENDING_VERIFY before         itself.                                                     observable pending-verify 
                                                                        confirmation.`<br>`{=html}3. Observe next                                                                window.                   
                                                                        boot.                                                                                                                              

  TC-OTA-022   OTA           Power loss during     Current image valid; Repeat OTA with power cut at several         Device remains bootable; previous valid        Automated    Requires                  Not Run
               robustness    firmware              update available;    download percentages; restore power and      firmware is retained when update was not                    relay/MOSFET-controlled   
                             download/write        HIL power control.   query version.                               completed/selected.                                         DUT power; run at         
                                                                                                                                                                                 multiple cut points.      

  TC-OTA-023   OTA-11        Reject                Wi-Fi connected;     Run OTA against invalid/corrupted image.     `invalid image header` or                      Automated    Requires controlled       Not Run
                             non-ESP32/corrupted   custom URL serves                                                 `image validation failed (corrupted image)`;                HTTP/HTTPS test artifact. 
                             image                 invalid image.                                                    current firmware remains active.                                                      

  TC-OTA-024   OTA-12        OTA from custom       Wi-Fi connected;     Send `ota <url>`; wait through reboot.       Image from supplied URL is installed according Automated    Use deterministic test    Not Run
                             HTTP/HTTPS URL        valid firmware                                                    to OTA validation rules.                                    server.                   
                                                   hosted at custom                                                                                                                                        
                                                   URL.                                                                                                                                                    

  TC-OTA-025   OTA-12        OTA test server does  Device in known      Send `ota-test-server`; capture log/reboot;  Simulation logs/reboots as specified but       Automated    UART/reboot.              Not Run
                             not flash firmware    version/partition.   check `version`.                             firmware version/partition content is not                                             
                                                                                                                     replaced.                                                                             

  TC-OTA-026   OTA partition Successive updates    At least two         Perform two successful OTA installs,         Each new image is written to inactive slot;    Automated    UART + multiple server    Not Run
               alternation   alternate OTA slots   installable versions checking `version` after each.               active slot alternates ota_0 \<-\> ota_1.                   versions.                 
                                                   available.                                                                                                                                              

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           

                                                                                                                                                                                                           
  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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

  -------------------------------------------------------------------------------------
  Area        Total       Automated   Partial     Manual      Automation assessment
  ----------- ----------- ----------- ----------- ----------- -------------------------
  Wi-Fi       13          13          0           0           HIL-enabled full
                                                              automation available for
                                                              UART/state plus physical
                                                              verification where
                                                              supported by OV3660
                                                              camera, HC-SR04 emulator,
                                                              relay contact feedback,
                                                              ULN2003 button actuation
                                                              and calibrated LDR.

  Smart Lamp  30          27          0           3           HIL-enabled full
                                                              automation available for
                                                              UART/state plus physical
                                                              verification where
                                                              supported by OV3660
                                                              camera, HC-SR04 emulator,
                                                              relay contact feedback,
                                                              ULN2003 button actuation
                                                              and calibrated LDR.

  OTA         26          26          0           0           HIL-enabled full
                                                              automation available for
                                                              UART/state plus physical
                                                              verification where
                                                              supported by OV3660
                                                              camera, HC-SR04 emulator,
                                                              relay contact feedback,
                                                              ULN2003 button actuation
                                                              and calibrated LDR.

  Other       15          14          0           1           HIL-enabled full
  Commands                                                    automation available for
                                                              UART/state plus physical
                                                              verification where
                                                              supported by OV3660
                                                              camera, HC-SR04 emulator,
                                                              relay contact feedback,
                                                              ULN2003 button actuation
                                                              and calibrated LDR.

  TOTAL       84          80          0           4           After HIL integration: 80
                                                              of 84 tests are fully
                                                              automatable. The
                                                              remaining 4 require
                                                              reliable
                                                              time-series/color-cycle
                                                              optical measurement.

                                                              

                                                              

                                                              

                                                              
  -------------------------------------------------------------------------------------
