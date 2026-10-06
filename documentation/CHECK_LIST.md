# station_WiFi Smart Lamp + OTA --- Test Cases (HIL Updated)

## Wi-Fi

  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  TC ID         Requirement   Title          Preconditions   Steps                          Expected Result                                        Automation   Automation      Status
                                                                                                                                                                Notes           
  ------------- ------------- -------------- --------------- ------------------------------ ------------------------------------------------------ ------------ --------------- --------
  TC-WIFI-001   FR-W1         Connect using  Device powered  1\. Send                       Scan lists networks with RSSI. Device logs             Automated    UART +          Not Run
                              SSID name      on; UART 115200 `connect`.`<br>`{=html}2. Wait `got ip:<IP>` and                                                   controllable    
                                             8N1; Wi-Fi      for scan list.`<br>`{=html}3.  `successfully connected to SSID:<SSID>`.                            Wi-Fi AP.       
                                             network         Enter target                                                                                                       
                                             available.      SSID.`<br>`{=html}4. Enter                                                                                         
                                                             valid password.                                                                                                    

  TC-WIFI-002   FR-W1         Connect using  Device powered  1\. Send                       Device connects to the SSID represented by the         Automated    Parse scan      Not Run
                              network number on; target      `connect`.`<br>`{=html}2.      selected number and logs successful connection.                     output and      
                                             network appears Enter the target network                                                                           select index.   
                                             in scan.        number.`<br>`{=html}3. Enter                                                                                       
                                                             valid password.                                                                                                    

  TC-WIFI-003   FR-W1         Reject         Target Wi-Fi    1\. Send                       `password too short (min 8 chars)` is logged.          Automated    UART only.      Not Run
                              password       network         `connect`.`<br>`{=html}2.      Connection attempt does not start.                                                  
                              shorter than 8 available.      Select SSID.`<br>`{=html}3.                                                                                        
                              characters                     Enter password shorter than 8                                                                                      
                                                             characters.                                                                                                        

  TC-WIFI-004   FR-W1         Reject invalid Target Wi-Fi    1\. Send                       `failed to connect to SSID:<SSID>` or                  Automated    Requires known  Not Run
                              Wi-Fi          network         `connect`.`<br>`{=html}2.      `connection timeout` is logged. Device remains                      AP credentials. 
                              credentials    available.      Select SSID.`<br>`{=html}3.    responsive.                                                                         
                                                             Enter incorrect                                                                                                    
                                                             password.`<br>`{=html}4. Wait                                                                                      
                                                             up to 10 s.                                                                                                        

  TC-WIFI-005   FR-W2         Save           No saved        1\. Connect successfully       Saved SSID/password are used and device reconnects     Automated    UART only after Not Run
                              credentials    credentials;    once.`<br>`{=html}2. Send      successfully.                                                       initial         
                              and connect    target network  `disconnect`.`<br>`{=html}3.                                                                       provisioning.   
                              with empty     available.      Send `connect`.`<br>`{=html}4.                                                                                     
                              input                          At SSID prompt press Enter.                                                                                        

  TC-WIFI-006   FR-W2         Saved          Valid           1\. Send                       Boot log contains                                      Automated    UART + reboot   Not Run
                              credentials do credentials     `reboot`.`<br>`{=html}2.       `saved credentials found but auto-connect disabled`.                detection.      
                              not            saved and Wi-Fi Observe boot                   `status` reports disconnected until explicit                                        
                              auto-connect   connected.      log.`<br>`{=html}3. Send       connect/K3 reconnect.                                                               
                              after reboot                   `status`.                                                                                                          

  TC-WIFI-007   FR-W4         Disconnect     Device          1\. Send                       Device disconnects. `status` reports                   Automated    UART only.      Not Run
                              active Wi-Fi   connected to    `disconnect`.`<br>`{=html}2.   `WiFi: disconnected`.                                                               
                              connection     Wi-Fi.          Send `status`.                                                                                                     

  TC-WIFI-008   FR-W4         Status reports Device          1\. Send `status`.             Output contains `WiFi: connected`, correct SSID, IP    Automated    UART only.      Not Run
                              connected      connected to                                   and RSSI.                                                                           
                              Wi-Fi details  Wi-Fi.                                                                                                                             

  TC-WIFI-009   FR-W4         Scan reports   At least one    1\. Send                       Network list is returned and entries include RSSI and  Automated    UART;           Not Run
                              network RSSI   Wi-Fi network   `scan`.`<br>`{=html}2. Inspect channel.                                                            deterministic   
                              and channel    is visible.     scan output.                                                                                       SSID can be     
                                                                                                                                                                provided by     
                                                                                                                                                                test AP.        

  TC-WIFI-010   FR-W5         K3 disconnects Device          1\. Press K3.`<br>`{=html}2.   Wi-Fi disconnects and status becomes disconnected.     Automated    Requires HIL    Not Run
                              when connected connected to    Observe UART.`<br>`{=html}3.                                                                       GPIO/button     
                                             Wi-Fi.          Send `status`.                                                                                     emulator.       

  TC-WIFI-011   FR-W5         K3 reconnects  Saved           1\. Press K3.`<br>`{=html}2.   Log contains `[K3] wifi reconnect (saved credentials)` Automated    Requires HIL    Not Run
                              using saved    credentials     Observe UART.`<br>`{=html}3.   and device reconnects.                                              GPIO/button     
                              credentials    exist; device   Send `status`.                                                                                     emulator.       
                                             disconnected.                                                                                                                      

  TC-WIFI-012   FR-W5         K3 reconnect   NVS has no      1\. Press K3.`<br>`{=html}2.   `no saved credentials, use 'connect' first` is logged; Automated    Requires NVS    Not Run
                              without saved  saved Wi-Fi     Observe UART.                  device remains stable.                                              reset + HIL     
                              credentials    credentials;                                                                                                       GPIO/button     
                                             device                                                                                                             emulator.       
                                             disconnected.                                                                                                                      

  TC-WIFI-013   FR-W6         Wi-Fi LED      Lamp off; LED   1\. Disconnect Wi-Fi and       Disconnected state is dim red; connected state is dim  Automated    Fully automated Not Run
                              indication     auto mode.      observe RGB                    green.                                                              with OV3660     
                              when lamp is                   LED.`<br>`{=html}2. Connect                                                                        camera: verify  
                              off                            Wi-Fi and observe RGB LED.                                                                         physical WS2812 
                                                                                                                                                                indication      
                                                                                                                                                                while lamp is   
                                                                                                                                                                off.            

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                

                                                                                                                                                                                
  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Smart Lamp

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  TC ID         Requirement   Title          Preconditions   Steps                                   Expected Result                                 Automation   Automation Notes     Status
  ------------- ------------- -------------- --------------- --------------------------------------- ----------------------------------------------- ------------ -------------------- --------
  TC-LAMP-001   FR-L1         Lamp on and    Device booted;  1\. Send `lamp on`.`<br>`{=html}2. Send Logs `[LAMP] on` then `[LAMP] off`; physical    Automated    Fully automated:     Not Run
                              off            UART available. `lamp off`.                             lamp follows commands.                                       UART command/state   
                                                                                                                                                                  plus physical WS2812 
                                                                                                                                                                  verification with    
                                                                                                                                                                  OV3660 camera.       

  TC-LAMP-002   FR-L1         Lamp is off    Lamp is on      1\. Send `reboot`.`<br>`{=html}2. Wait  Lamp is off after reboot regardless of          Automated    Status via UART;     Not Run
                              after reboot   before reboot.  for boot.`<br>`{=html}3. Send           pre-reboot on/off state.                                     physical off can     
                                                             `lamp status`.                                                                                       additionally be      
                                                                                                                                                                  HIL-verified.        

  TC-LAMP-003   FR-L2         Set each       Lamp on.        For each: red, green, blue, white,      Response reports exact specified RGB mapping    Automated    UART/state           Not Run
                              supported                      yellow, purple, cyan:`<br>`{=html}1.    and status stores the same RGB values.                       validation.          
                              named color                    Send                                                                                                                      
                                                             `lamp color <name>`.`<br>`{=html}2.                                                                                       
                                                             Check response and `lamp status`.                                                                                         

  TC-LAMP-004   FR-L2         Reject unknown Lamp on; known  1\. Record current                      `error: unknown color 'orange'`; previous color Automated    UART only.           Not Run
                              named color    color already   status.`<br>`{=html}2. Send             remains unchanged.                                                                
                                             set.            `lamp color orange`.`<br>`{=html}3.                                                                                       
                                                             Read status again.                                                                                                        

  TC-LAMP-005   FR-L3         Set RGB        Lamp on.        Set `0 0 0`, `255 255 255`, and         Each valid RGB triplet is accepted and status   Automated    UART/state           Not Run
                              boundary and                   `255 0 128`; check status after each.   matches exactly.                                             validation.          
                              arbitrary                                                                                                                                                
                              values                                                                                                                                                   

  TC-LAMP-006   FR-L3         Reject RGB     Lamp on; known  Try values such as `300 0 0` and        `error: rgb values must be 0-255`; previous     Automated    UART only.           Not Run
                              values outside RGB already     `-1 0 0`.                               color remains unchanged.                                                          
                              0-255          set.                                                                                                                                      

  TC-LAMP-007   FR-L4         Physical named Lamp on;        Set each supported named color and      Physical LED color corresponds to requested     Automated    Fully automatable    Not Run
                              colors match   optical         observe/measure LED output.             named color.                                                 with fixed camera    
                              requested      observation                                                                                                          ROI and calibrated   
                              colors         available.                                                                                                           OV3660 color         
                                                                                                                                                                  measurement. Color   
                                                                                                                                                                  references are       
                                                                                                                                                                  calibrated against   
                                                                                                                                                                  the physical WS2812. 

  TC-LAMP-008   FR-L5         Set brightness Lamp on.        Set brightness 0, 1, 50, 100 and query  `[LAMP] brightness set: N%`; status reports     Automated    UART/state           Not Run
                              boundaries                     status after each.                      exact value.                                                 validation.          

  TC-LAMP-009   FR-L5         Reject invalid Lamp on;        Send `lamp brightness 150`, then        Error `brightness must be 0-100`; brightness    Automated    UART only.           Not Run
                              brightness     brightness 50%. `lamp brightness -5`; query status.     remains 50%.                                                                      

  TC-LAMP-010   FR-L5         Brightness     Lamp on; known  For solid, blink, breathe and rainbow   Peak/steady physical brightness changes         Automated    Fully automatable    Not Run
                              physically     color.          where supported, set two brightness     according to configured brightness in every                  with fixed-exposure  
                              applies in all                 levels and measure output.              supported mode.                                              OV3660 and ROI       
                              modes                                                                                                                               intensity            
                                                                                                                                                                  measurement for      
                                                                                                                                                                  physical brightness  
                                                                                                                                                                  verification.        

  TC-LAMP-011   FR-L6         Solid mode     Lamp on.        Set `lamp mode solid`; observe LED and  Log reports solid; LED remains continuously on  Automated    Fully automated:     Not Run
                              behavior                       query status.                           at configured color/brightness; status mode is               UART state plus      
                                                                                                     solid.                                                       continuous physical  
                                                                                                                                                                  WS2812 output        
                                                                                                                                                                  verified by camera.  

  TC-LAMP-012   FR-L6         Blink mode     Lamp on.        Set `lamp mode blink`; measure several  LED alternates \~0.5 s on / \~0.5 s off (1 Hz)  Manual       Automatable with     Not Run
                              timing                         cycles.                                 at configured brightness.                                    photodiode/light     
                                                                                                                                                                  sensor + timestamped 
                                                                                                                                                                  sampling.            

  TC-LAMP-013   FR-L6         Breathe mode   Lamp on.        Set `lamp mode breathe`;                Brightness changes smoothly with \~3 s period;  Manual       Automatable with     Not Run
                              timing                         observe/measure multiple cycles.        maximum equals configured brightness.                        photodiode/light     
                                                                                                                                                                  sensor.              

  TC-LAMP-014   FR-L6         Rainbow        Test firmware   On each version send                    1.3.0/1.4.0 return                              Automated    Requires             Not Run
                              availability   1.3.0, 1.4.0    `lamp mode rainbow`.                    `mode 'rainbow' not implemented yet`; 1.5.0                  version-controlled   
                              by firmware    and 1.5.0.                                              accepts rainbow.                                             OTA/flash setup.     
                              version                                                                                                                                                  

  TC-LAMP-015   FR-L6         Rainbow        Firmware 1.5.0; Set rainbow mode and observe/measure    Color changes smoothly around the color wheel   Manual       Automatable with RGB Not Run
                              physical cycle lamp on.        one or more cycles.                     with \~5 s cycle and configured brightness.                  sensor/camera +      
                              on 1.5.0                                                                                                                            timing analysis.     

  TC-LAMP-016   FR-L6         Reject unknown Lamp on; known  Send `lamp mode disco`; query status.   `error: unknown mode 'disco'`; previous mode    Automated    UART only.           Not Run
                              lamp mode      mode set.                                               remains unchanged.                                                                

  TC-LAMP-017   FR-L7         Lamp auto-off  Lamp on.        1\. Send `lamp timer 5`.`<br>`{=html}2. Logs auto-off, then                             Automated    UART/timing;         Not Run
                              timer expires                  Observe for \>5 s.`<br>`{=html}3. Query `[LAMP] timer expired, lamp off`; status is off              physical off can be  
                                                             status.                                 and timer_s=0.                                               HIL-verified.        

  TC-LAMP-018   FR-L7         Cancel active  Lamp on; timer  1\. Send `lamp timer 0` before          `[LAMP] timer cancelled`; lamp remains on and   Automated    UART/timing.         Not Run
                              lamp timer     active.         expiry.`<br>`{=html}2. Wait beyond      timer_s=0.                                                                        
                                                             original expiry.`<br>`{=html}3. Query                                                                                     
                                                             status.                                                                                                                   

  TC-LAMP-019   FR-L7         Reject invalid Lamp on.        Send timer 5000 and other out-of-range  `error: timer must be 1-3600 s (0 = cancel)`;   Automated    UART only.           Not Run
                              timer values                   values.                                 no invalid timer starts.                                                          

  TC-LAMP-020   FR-L7         Reject timer   Lamp off.       Send `lamp timer 5`.                    `error: lamp is off`; timer is not started.     Automated    UART only.           Not Run
                              when lamp is                                                                                                                                             
                              off                                                                                                                                                      

  TC-LAMP-021   FR-L7         Timer is not   Lamp on; timer  1\. Start timer.`<br>`{=html}2. Reboot  Lamp is off after reboot and timer_s=0; old     Automated    UART/reboot.         Not Run
                              preserved      active with     before expiry.`<br>`{=html}3. Query     timer does not resume.                                                            
                              after reboot   enough          status.                                                                                                                   
                                             remaining time.                                                                                                                           

  TC-LAMP-022   FR-L8         Lamp status    Lamp configured Send `lamp status` and parse one-line   JSON contains lamp, color\[3\], brightness,     Automated    Direct JSON parsing. Not Run
                              JSON schema    to known state. JSON.                                   mode, timer_s with values matching configured                                     
                              and values                                                             logical state.                                                                    

  TC-LAMP-023   FR-L9         Default lamp   NVS erased /    Boot and send `lamp status`.            Defaults are white, 50%, solid; lamp itself is  Automated    Requires controlled  Not Run
                              settings on    clean device.                                           off after boot.                                              NVS erase.           
                              clean device                                                                                                                                             

  TC-LAMP-024   FR-L9         Lamp settings  Set non-default 1\. Change settings.`<br>`{=html}2.     Color, brightness and mode are restored from    Automated    UART/reboot.         Not Run
                              survive reboot color,          Reboot.`<br>`{=html}3. Query status.    NVS; lamp remains off after reboot.                                               
                                             brightness and                                                                                                                            
                                             mode.                                                                                                                                     

  TC-LAMP-025   FR-L10        Save and load  Firmware 1.5.0. 1\. Configure                           Scene save/load succeeds and restores saved     Automated    UART/state           Not Run
                              scenes on                      color/brightness/mode.`<br>`{=html}2.   color, brightness and mode.                                  validation.          
                              1.5.0                          Save scene 1.`<br>`{=html}3. Change                                                                                       
                                                             settings.`<br>`{=html}4. Load scene                                                                                       
                                                             1.`<br>`{=html}5. Query status.                                                                                           

  TC-LAMP-026   FR-L10        Scene          Firmware 1.5.0; Send scene save 7 and scene load 2.     Out-of-range returns `scene must be 1-3`; empty Automated    UART only.           Not Run
                              validation     scene 2 empty.                                          scene returns `scene 2 is empty`.                                                 
                              errors on                                                                                                                                                
                              1.5.0                                                                                                                                                    

  TC-LAMP-027   FR-L10        Scenes         Firmware 1.3.0  Send `lamp scene save 1`.               `error: scenes not implemented yet`.            Automated    Version-controlled   Not Run
                              unavailable    or 1.4.0.                                                                                                            test.                
                              before 1.5.0                                                                                                                                             

  TC-LAMP-028   FR-L10        Scenes survive Firmware 1.5.0; 1\. Reboot.`<br>`{=html}2. Load saved   Saved scene remains available and restores      Automated    UART/reboot.         Not Run
                              reboot         scene saved.    scene.`<br>`{=html}3. Query status.     stored settings.                                                                  

  TC-LAMP-029   FR-L11        Reject unknown Device booted.  Send `lamp blabla`.                     `error: unknown lamp command. See 'help'`.      Automated    UART only.           Not Run
                              lamp command                                                                                                                                             

  TC-LAMP-030   FR-W6 / Smart Lamp overrides Lamp on; known  1\. Issue `led on`, `led off`,          While lamp is on, its output is not altered by  Automated    Fully automated:     Not Run
                Lamp priority Wi-Fi and led  lamp            `led auto` and change Wi-Fi state while Wi-Fi indication or `led ...`. After lamp off,               logical priority via 
                              commands while color/mode;     lamp is on.`<br>`{=html}2. Query lamp   LED returns to Wi-Fi indication.                             UART plus physical   
                              on             Wi-Fi state     status/observe LED.`<br>`{=html}3. Turn                                                              WS2812 result        
                                             known.          lamp off.                                                                                            verified by camera.  

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       

                                                                                                                                                                                       
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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
