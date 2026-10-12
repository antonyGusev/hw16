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

  Smart Lamp  35          35          0           0           HIL-enabled full
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
