**version**

```text
I (16203) wifi station: FW: v1.3.0 (build Sep 29 2026 14:15:56)
I (16203) wifi station:   partition: ota_0 @ 0x10000, state: valid
```

**ota check**

```text
I (250693) wifi:<ba-add>idx:1 (ifx:0, 32:16:9d:25:9c:16), tid:0, ssn:1, winSize:64
I (251073) esp-x509-crt-bundle: Certificate validated
I (252413) esp-x509-crt-bundle: Certificate validated
I (253273) wifi station: [OTA] current version: 1.3.0
I (253273) wifi station: [OTA] stable channel:  1.4.0
I (253273) wifi station: [OTA] beta channel:    1.5.0
I (253283) wifi station: [OTA] update available. Type 'ota update'
```

**ota update**

```text
I (298403) esp-x509-crt-bundle: Certificate validated
I (299043) wifi station: [OTA] stable channel: 1.4.0, current: 1.3.0
I (299043) wifi station: [OTA] current version: 1.3.0 (partition ota_0)
I (299043) wifi station: [OTA] target partition: ota_1
I (299053) wifi station: [OTA] downloading: https://raw.githubusercontent.com/BohdanHorbanych/esp32-ota-files/main/firmware/v1.4.0/station_WiFi.bin
I (299463) esp-x509-crt-bundle: Certificate validated
I (300613) esp_https_ota: Starting OTA...
I (300613) esp_https_ota: Writing to <ota_1> partition at offset 0x100000
I (302493) wifi station: [OTA] new version: 1.4.0
I (306183) wifi station: [OTA] progress: 10% (91136 / 907872 bytes)
I (308123) wifi station: [OTA] progress: 20% (185344 / 907872 bytes)
I (309913) wifi station: [OTA] progress: 30% (275456 / 907872 bytes)
I (311983) wifi station: [OTA] progress: 40% (365568 / 907872 bytes)
I (313713) wifi station: [OTA] progress: 50% (455680 / 907872 bytes)
I (315683) wifi station: [OTA] progress: 60% (545792 / 907872 bytes)
I (317653) wifi station: [OTA] progress: 70% (635904 / 907872 bytes)
I (319633) wifi station: [OTA] progress: 80% (730112 / 907872 bytes)
I (321483) wifi station: [OTA] progress: 90% (820224 / 907872 bytes)
I (323073) wifi station: [OTA] progress: 100% (907872 / 907872 bytes)
I (323073) esp_image: segment 0: paddr=00100020 vaddr=3c0a0020 size=3349ch (210076) map
I (323103) esp_image: segment 1: paddr=001334c4 vaddr=3fc97100 size=0506ch ( 20588) 
I (323113) esp_image: segment 2: paddr=00138538 vaddr=40374000 size=07ae0h ( 31456) 
I (323113) esp_image: segment 3: paddr=00140020 vaddr=42000020 size=923ech (599020) map
I (323193) esp_image: segment 4: paddr=001d2414 vaddr=4037bae0 size=0b5f4h ( 46580) 
I (323203) esp_image: segment 5: paddr=001dda10 vaddr=50000000 size=00024h (    36) 
I (323213) esp_image: segment 0: paddr=00100020 vaddr=3c0a0020 size=3349ch (210076) map
I (323243) esp_image: segment 1: paddr=001334c4 vaddr=3fc97100 size=0506ch ( 20588) 
I (323243) esp_image: segment 2: paddr=00138538 vaddr=40374000 size=07ae0h ( 31456) 
I (323243) esp_image: segment 3: paddr=00140020 vaddr=42000020 size=923ech (599020) map
I (323333) esp_image: segment 4: paddr=001d2414 vaddr=4037bae0 size=0b5f4h ( 46580) 
I (323333) esp_image: segment 5: paddr=001dda10 vaddr=50000000 size=00024h (    36) 
I (323383) wifi station: [OTA] success: 1.3.0 -> 1.4.0 in 20 s. Rebooting...
I (323883) wifi:state: run -> init (0x0)
I (323893) wifi:pm stop, total sleep time: 184615113 us / 235436373 us

I (323893) wifi:<ba-del>idx:1, tid:0
I (323893) wifi:<ba-del>idx:0, tid:5
I (323893) wifi:new:<5,0>, old:<5,1>, ap:<255,255>, sta:<5,1>, prof:1, snd_ch_cfg:0x0
I (323903) wifi station: retry to connect to the AP
I (323943) wifi:flush txq
I (323943) wifi:stop sw txq
I (323943) wifi:lmac stop hw txq
ESP-ROM:esp32s3-20210327
Build:Mar 27 2021
rst:0xc (RTC_SW_CPU_RST),boot:0x2b (SPI_FAST_FLASH_BOOT)
Saved PC:0x4037d308
SPIWP:0xee
mode:DIO, clock div:1
load:0x3fce2820,len:0x14f0
load:0x403c8700,len:0xda0
load:0x403cb700,len:0x2fa0
entry 0x403c8908
I (29) boot: ESP-IDF v6.0.1 2nd stage bootloader
I (29) boot: compile time Sep 29 2026 14:16:01
I (29) boot: Multicore bootloader
I (29) boot: chip revision: v0.2
I (32) boot: efuse block revision: v1.4
I (36) boot.esp32s3: Boot SPI Speed : 80MHz
I (40) boot.esp32s3: SPI Mode       : DIO
I (43) boot.esp32s3: SPI Flash Size : 2MB
I (47) boot: Enabling RNG early entropy source...
I (52) boot: Partition Table:
I (54) boot: ## Label            Usage          Type ST Offset   Length
I (61) boot:  0 nvs              WiFi data        01 02 00009000 00004000
I (67) boot:  1 otadata          OTA data         01 00 0000d000 00002000
I (74) boot:  2 ota_0            OTA app          00 10 00010000 000f0000
I (80) boot:  3 ota_1            OTA app          00 11 00100000 000f0000
I (87) boot: End of partition table
I (115) esp_image: segment 0: paddr=00100020 vaddr=3c0a0020 size=3349ch (210076) map
I (153) esp_image: segment 1: paddr=001334c4 vaddr=3fc97100 size=0506ch ( 20588) load
I (158) esp_image: segment 2: paddr=00138538 vaddr=40374000 size=07ae0h ( 31456) load
I (165) esp_image: segment 3: paddr=00140020 vaddr=42000020 size=923ech (599020) map
I (273) esp_image: segment 4: paddr=001d2414 vaddr=4037bae0 size=0b5f4h ( 46580) load
I (283) esp_image: segment 5: paddr=001dda10 vaddr=50000000 size=00024h (    36) load
I (292) boot: Loaded app from partition at offset 0x100000
I (292) boot: Disabling RNG early entropy source...
I (302) cpu_start: Multicore app
I (311) cpu_start: GPIO 44 and 43 are used as console UART I/O pins
I (311) cpu_start: Pro cpu start user code
I (311) cpu_start: cpu freq: 160000000 Hz
I (313) app_init: Application information:
I (317) app_init: Project name:     station_WiFi
I (321) app_init: App version:      1.4.0
I (325) app_init: Compile time:     Sep 29 2026 14:16:45
I (330) app_init: ELF file SHA256:  f7a307237...
I (334) app_init: ESP-IDF:          v6.0.1
I (338) efuse_init: Min chip rev:     v0.0
I (342) efuse_init: Max chip rev:     v0.99 
I (346) efuse_init: Chip rev:         v0.2
I (350) heap_init: Initializing. RAM available for dynamic allocation:
I (356) heap_init: At 3FCA0460 len 000492B0 (292 KiB): RAM
I (361) heap_init: At 3FCE9710 len 00005724 (21 KiB): RAM
I (366) heap_init: At 3FCF0000 len 00008000 (32 KiB): DRAM
I (372) heap_init: At 600FE000 len 00001FE8 (7 KiB): RTCRAM
I (378) spi_flash: detected chip: mxic
I (380) spi_flash: flash io: dio
W (383) spi_flash: Detected size(16384k) larger than the size in the binary image header(2048k). Using the size in the binary image header.
I (396) sleep_gpio: Configure to isolate all GPIO pins in sleep state
I (402) sleep_gpio: Enable automatic switching of GPIO sleep configuration
I (409) main_task: Started on CPU0
I (429) main_task: Calling app_main()
I (449) temperature_sensor: Range [-10°C ~ 80°C], error < 1°C
I (449) pp: pp rom version: e7ae62f
I (459) net80211: net80211 rom version: e7ae62f
I (469) wifi:wifi driver task: 3fced4cc, prio:23, stack:6656, core=0
I (469) wifi:wifi firmware version: b37c951
I (469) wifi:wifi certification version: v7.0
I (479) wifi:config NVS flash: enabled
I (479) wifi:config nano formatting: disabled
I (479) wifi:Init data frame dynamic rx buffer num: 32
I (479) wifi:Init static rx mgmt buffer num: 5
I (489) wifi:Init management short buffer num: 32
I (489) wifi:Init dynamic tx buffer num: 32
I (499) wifi:Init static tx FG buffer num: 2
I (499) wifi:Init static rx buffer size: 1600
I (499) wifi:Init static rx buffer num: 10
I (509) wifi:Init dynamic rx buffer num: 32
I (509) wifi_init: rx ba win: 6
I (519) wifi_init: accept mbox: 6
I (519) wifi_init: tcpip mbox: 32
I (519) wifi_init: udp mbox: 6
I (519) wifi_init: tcp mbox: 6
I (529) wifi_init: tcp tx win: 5760
I (529) wifi_init: tcp rx win: 5760
I (529) wifi_init: tcp mss: 1440
I (539) wifi_init: WiFi IRAM OP enabled
I (539) wifi_init: WiFi RX IRAM OP enabled
I (539) phy_init: phy_version 711,97bcf0a2,Aug 25 2025,19:04:10
I (599) wifi:mode : sta (90:70:69:31:a6:8c)
I (599) wifi:enable tsf
I (599) wifi station: wifi initialized. Type 'connect' to join a network (interactive)
I (599) wifi station: [OTA] running partition: ota_1, version 1.4.0
W (609) wifi station: [OTA] new firmware, state PENDING_VERIFY - running self-check...
I (649) wifi station: [OTA] self-check passed, firmware marked VALID
```

**ota update beta**

```text
I (265999) wifi:<ba-add>idx:1 (ifx:0, 32:16:9d:25:b8:9e), tid:0, ssn:0, winSize:64
I (266409) esp-x509-crt-bundle: Certificate validated
I (267239) wifi station: [OTA] beta channel: 1.5.0, current: 1.4.0
I (267239) wifi station: [OTA] current version: 1.4.0 (partition ota_1)
I (267239) wifi station: [OTA] target partition: ota_0
I (267239) wifi station: [OTA] downloading: https://raw.githubusercontent.com/BohdanHorbanych/esp32-ota-files/main/firmware/v1.5.0/station_WiFi.bin
I (267639) esp-x509-crt-bundle: Certificate validated
I (269279) esp_https_ota: Starting OTA...
I (269279) esp_https_ota: Writing to <ota_0> partition at offset 0x10000
I (269289) wifi station: [OTA] new version: 1.5.0
I (271219) wifi station: [OTA] progress: 10% (91136 / 908304 bytes)
I (273229) wifi station: [OTA] progress: 20% (185344 / 908304 bytes)
I (275019) wifi station: [OTA] progress: 30% (275456 / 908304 bytes)
I (276869) wifi station: [OTA] progress: 40% (365568 / 908304 bytes)
I (278529) wifi station: [OTA] progress: 50% (455680 / 908304 bytes)
I (280439) wifi station: [OTA] progress: 60% (545792 / 908304 bytes)
I (282189) wifi station: [OTA] progress: 70% (635904 / 908304 bytes)
I (284099) wifi station: [OTA] progress: 80% (730112 / 908304 bytes)
I (285789) wifi station: [OTA] progress: 90% (820224 / 908304 bytes)
I (287269) wifi station: [OTA] progress: 100% (908304 / 908304 bytes)
I (287269) esp_image: segment 0: paddr=00010020 vaddr=3c0a0020 size=3352ch (210220) map
I (287299) esp_image: segment 1: paddr=00043554 vaddr=3fc97100 size=0506ch ( 20588) 
I (287309) esp_image: segment 2: paddr=000485c8 vaddr=40374000 size=07a50h ( 31312) 
I (287309) esp_image: segment 3: paddr=00050020 vaddr=42000020 size=92508h (599304) map
I (287389) esp_image: segment 4: paddr=000e2530 vaddr=4037ba50 size=0b684h ( 46724) 
I (287399) esp_image: segment 5: paddr=000edbbc vaddr=50000000 size=00024h (    36) 
I (287409) esp_image: segment 0: paddr=00010020 vaddr=3c0a0020 size=3352ch (210220) map
I (287429) esp_image: segment 1: paddr=00043554 vaddr=3fc97100 size=0506ch ( 20588) 
I (287439) esp_image: segment 2: paddr=000485c8 vaddr=40374000 size=07a50h ( 31312) 
I (287439) esp_image: segment 3: paddr=00050020 vaddr=42000020 size=92508h (599304) map
I (287529) esp_image: segment 4: paddr=000e2530 vaddr=4037ba50 size=0b684h ( 46724) 
I (287529) esp_image: segment 5: paddr=000edbbc vaddr=50000000 size=00024h (    36) 
I (287569) wifi station: [OTA] success: 1.4.0 -> 1.5.0 in 18 s. Rebooting...
I (288069) wifi:state: run -> init (0x0)
I (288079) wifi:pm stop, total sleep time: 31237050 us / 57333596 us

I (288079) wifi:<ba-del>idx:1, tid:0
I (288079) wifi:<ba-del>idx:0, tid:5
I (288079) wifi:new:<5,0>, old:<5,1>, ap:<255,255>, sta:<5,1>, prof:1, snd_ch_cfg:0x0
I (288089) wifi station: retry to connect to the AP
I (288139) wifi:flush txq
I (288139) wifi:stop sw txq
I (288139) wifi:lmac stop hw txq
␀�ESP-ROM:esp32s3-20210327
Build:Mar 27 2021
rst:0xc (RTC_SW_CPU_RST),boot:0x2b (SPI_FAST_FLASH_BOOT)
Saved PC:0x4037d308
SPIWP:0xee
mode:DIO, clock div:1
load:0x3fce2820,len:0x14f0
load:0x403c8700,len:0xda0
load:0x403cb700,len:0x2fa0
entry 0x403c8908
I (29) boot: ESP-IDF v6.0.1 2nd stage bootloader
I (29) boot: compile time Sep 29 2026 14:16:01
I (29) boot: Multicore bootloader
I (29) boot: chip revision: v0.2
I (32) boot: efuse block revision: v1.4
I (36) boot.esp32s3: Boot SPI Speed : 80MHz
I (40) boot.esp32s3: SPI Mode       : DIO
I (43) boot.esp32s3: SPI Flash Size : 2MB
I (47) boot: Enabling RNG early entropy source...
I (52) boot: Partition Table:
I (54) boot: ## Label            Usage          Type ST Offset   Length
I (61) boot:  0 nvs              WiFi data        01 02 00009000 00004000
I (67) boot:  1 otadata          OTA data         01 00 0000d000 00002000
I (74) boot:  2 ota_0            OTA app          00 10 00010000 000f0000
I (80) boot:  3 ota_1            OTA app          00 11 00100000 000f0000
I (87) boot: End of partition table
I (115) esp_image: segment 0: paddr=00010020 vaddr=3c0a0020 size=3352ch (210220) map
I (153) esp_image: segment 1: paddr=00043554 vaddr=3fc97100 size=0506ch ( 20588) load
I (158) esp_image: segment 2: paddr=000485c8 vaddr=40374000 size=07a50h ( 31312) load
I (165) esp_image: segment 3: paddr=00050020 vaddr=42000020 size=92508h (599304) map
I (273) esp_image: segment 4: paddr=000e2530 vaddr=4037ba50 size=0b684h ( 46724) load
I (283) esp_image: segment 5: paddr=000edbbc vaddr=50000000 size=00024h (    36) load
I (292) boot: Loaded app from partition at offset 0x10000
I (292) boot: Disabling RNG early entropy source...
I (302) cpu_start: Multicore app
I (311) cpu_start: GPIO 44 and 43 are used as console UART I/O pins
I (311) cpu_start: Pro cpu start user code
I (311) cpu_start: cpu freq: 160000000 Hz
I (313) app_init: Application information:
I (317) app_init: Project name:     station_WiFi
I (321) app_init: App version:      1.5.0
I (325) app_init: Compile time:     Sep 29 2026 14:17:34
I (330) app_init: ELF file SHA256:  486cd296d...
I (334) app_init: ESP-IDF:          v6.0.1
I (338) efuse_init: Min chip rev:     v0.0
I (342) efuse_init: Max chip rev:     v0.99 
I (346) efuse_init: Chip rev:         v0.2
I (350) heap_init: Initializing. RAM available for dynamic allocation:
I (356) heap_init: At 3FCA0460 len 000492B0 (292 KiB): RAM
I (361) heap_init: At 3FCE9710 len 00005724 (21 KiB): RAM
I (366) heap_init: At 3FCF0000 len 00008000 (32 KiB): DRAM
I (372) heap_init: At 600FE000 len 00001FE8 (7 KiB): RTCRAM
I (378) spi_flash: detected chip: mxic
I (380) spi_flash: flash io: dio
W (383) spi_flash: Detected size(16384k) larger than the size in the binary image header(2048k). Using the size in the binary image header.
I (396) sleep_gpio: Configure to isolate all GPIO pins in sleep state
I (402) sleep_gpio: Enable automatic switching of GPIO sleep configuration
I (409) main_task: Started on CPU0
I (429) main_task: Calling app_main()
I (449) temperature_sensor: Range [-10°C ~ 80°C], error < 1°C
I (449) wifi station: [CFG] migrating settings to v2 format...
I (569) wifi station: [CFG] migration done
I (579) pp: pp rom version: e7ae62f
I (579) net80211: net80211 rom version: e7ae62f
I (599) wifi:wifi driver task: 3fceed90, prio:23, stack:6656, core=0
I (599) wifi:wifi firmware version: b37c951
I (599) wifi:wifi certification version: v7.0
I (599) wifi:config NVS flash: enabled
I (599) wifi:config nano formatting: disabled
I (609) wifi:Init data frame dynamic rx buffer num: 32
I (609) wifi:Init static rx mgmt buffer num: 5
I (609) wifi:Init management short buffer num: 32
I (619) wifi:Init dynamic tx buffer num: 32
I (619) wifi:Init static tx FG buffer num: 2
I (629) wifi:Init static rx buffer size: 1600
I (629) wifi:Init static rx buffer num: 10
I (639) wifi:Init dynamic rx buffer num: 32
I (639) wifi_init: rx ba win: 6
I (639) wifi_init: accept mbox: 6
I (639) wifi_init: tcpip mbox: 32
I (649) wifi_init: udp mbox: 6
I (649) wifi_init: tcp mbox: 6
I (649) wifi_init: tcp tx win: 5760
I (659) wifi_init: tcp rx win: 5760
I (659) wifi_init: tcp mss: 1440
I (659) wifi_init: WiFi IRAM OP enabled
I (669) wifi_init: WiFi RX IRAM OP enabled
I (669) phy_init: phy_version 711,97bcf0a2,Aug 25 2025,19:04:10
W (679) phy_init: failed to load RF calibration data (0x1102), falling back to full calibration
I (719) phy_init: Saving new calibration data due to checksum failure or outdated calibration data, mode(2)
I (739) wifi:mode : sta (90:70:69:31:a6:8c)
I (739) wifi:enable tsf
I (739) wifi station: wifi initialized. Type 'connect' to join a network (interactive)
I (739) wifi station: [OTA] running partition: ota_0, version 1.5.0
W (749) wifi station: [OTA] new firmware, state PENDING_VERIFY - running self-check...
I (789) wifi station: [OTA] self-check passed, firmware marked VALID
```

**ota install 1.4.0**

```text
I (168669) wifi station: [OTA] current version: 1.3.0 (partition ota_1)
I (168669) wifi station: [OTA] target partition: ota_0
I (168669) wifi station: [OTA] downloading: https://raw.githubusercontent.com/BohdanHorbanych/esp32-ota-files/main/firmware/v1.4.0/station_WiFi.bin
I (168709) wifi:<ba-add>idx:1 (ifx:0, 32:16:9d:25:9c:16), tid:0, ssn:2, winSize:64
I (169099) esp-x509-crt-bundle: Certificate validated
I (169919) esp_https_ota: Starting OTA...
I (169919) esp_https_ota: Writing to <ota_0> partition at offset 0x10000
I (169919) wifi station: [OTA] new version: 1.4.0
I (171569) wifi station: [OTA] progress: 10% (91136 / 907872 bytes)
I (173489) wifi station: [OTA] progress: 20% (185344 / 907872 bytes)
I (175169) wifi station: [OTA] progress: 30% (275456 / 907872 bytes)
I (177019) wifi station: [OTA] progress: 40% (365568 / 907872 bytes)
I (178619) wifi station: [OTA] progress: 50% (455680 / 907872 bytes)
I (180289) wifi station: [OTA] progress: 60% (545792 / 907872 bytes)
I (181739) wifi station: [OTA] progress: 70% (635904 / 907872 bytes)
I (183419) wifi station: [OTA] progress: 80% (730112 / 907872 bytes)
I (185069) wifi station: [OTA] progress: 90% (820224 / 907872 bytes)
I (186549) wifi station: [OTA] progress: 100% (907872 / 907872 bytes)
I (186549) esp_image: segment 0: paddr=00010020 vaddr=3c0a0020 size=3349ch (210076) map
I (186579) esp_image: segment 1: paddr=000434c4 vaddr=3fc97100 size=0506ch ( 20588) 
I (186589) esp_image: segment 2: paddr=00048538 vaddr=40374000 size=07ae0h ( 31456) 
I (186589) esp_image: segment 3: paddr=00050020 vaddr=42000020 size=923ech (599020) map
I (186669) esp_image: segment 4: paddr=000e2414 vaddr=4037bae0 size=0b5f4h ( 46580) 
I (186679) esp_image: segment 5: paddr=000eda10 vaddr=50000000 size=00024h (    36) 
I (186679) esp_image: segment 0: paddr=00010020 vaddr=3c0a0020 size=3349ch (210076) map
I (186709) esp_image: segment 1: paddr=000434c4 vaddr=3fc97100 size=0506ch ( 20588) 
I (186719) esp_image: segment 2: paddr=00048538 vaddr=40374000 size=07ae0h ( 31456) 
I (186719) esp_image: segment 3: paddr=00050020 vaddr=42000020 size=923ech (599020) map
I (186809) esp_image: segment 4: paddr=000e2414 vaddr=4037bae0 size=0b5f4h ( 46580) 
I (186809) esp_image: segment 5: paddr=000eda10 vaddr=50000000 size=00024h (    36) 
I (186859) wifi station: [OTA] success: 1.3.0 -> 1.4.0 in 16 s. Rebooting...
I (187359) wifi:state: run -> init (0x0)
I (187369) wifi:pm stop, total sleep time: 11530984 us / 30628796 us

I (187369) wifi:<ba-del>idx:1, tid:0
I (187369) wifi:<ba-del>idx:0, tid:5
I (187369) wifi:new:<5,0>, old:<5,1>, ap:<255,255>, sta:<5,1>, prof:1, snd_ch_cfg:0x0
I (187379) wifi station: retry to connect to the AP
I (187419) wifi:flush txq
I (187419) wifi:stop sw txq
I (187419) wifi:lmac stop hw txq
␀�ESP-ROM:esp32s3-20210327
Build:Mar 27 2021
rst:0xc (RTC_SW_CPU_RST),boot:0x2b (SPI_FAST_FLASH_BOOT)
Saved PC:0x4037d308
SPIWP:0xee
mode:DIO, clock div:1
load:0x3fce2820,len:0x14f0
load:0x403c8700,len:0xda0
load:0x403cb700,len:0x2fa0
entry 0x403c8908
I (29) boot: ESP-IDF v6.0.1 2nd stage bootloader
I (29) boot: compile time Sep 29 2026 14:16:01
I (29) boot: Multicore bootloader
I (29) boot: chip revision: v0.2
I (32) boot: efuse block revision: v1.4
I (36) boot.esp32s3: Boot SPI Speed : 80MHz
I (40) boot.esp32s3: SPI Mode       : DIO
I (43) boot.esp32s3: SPI Flash Size : 2MB
I (47) boot: Enabling RNG early entropy source...
I (52) boot: Partition Table:
I (54) boot: ## Label            Usage          Type ST Offset   Length
I (61) boot:  0 nvs              WiFi data        01 02 00009000 00004000
I (67) boot:  1 otadata          OTA data         01 00 0000d000 00002000
I (74) boot:  2 ota_0            OTA app          00 10 00010000 000f0000
I (80) boot:  3 ota_1            OTA app          00 11 00100000 000f0000
I (87) boot: End of partition table
I (115) esp_image: segment 0: paddr=00010020 vaddr=3c0a0020 size=3349ch (210076) map
I (153) esp_image: segment 1: paddr=000434c4 vaddr=3fc97100 size=0506ch ( 20588) load
I (158) esp_image: segment 2: paddr=00048538 vaddr=40374000 size=07ae0h ( 31456) load
I (165) esp_image: segment 3: paddr=00050020 vaddr=42000020 size=923ech (599020) map
I (273) esp_image: segment 4: paddr=000e2414 vaddr=4037bae0 size=0b5f4h ( 46580) load
I (283) esp_image: segment 5: paddr=000eda10 vaddr=50000000 size=00024h (    36) load
I (292) boot: Loaded app from partition at offset 0x10000
I (292) boot: Disabling RNG early entropy source...
I (302) cpu_start: Multicore app
I (311) cpu_start: GPIO 44 and 43 are used as console UART I/O pins
I (311) cpu_start: Pro cpu start user code
I (311) cpu_start: cpu freq: 160000000 Hz
I (313) app_init: Application information:
I (317) app_init: Project name:     station_WiFi
I (321) app_init: App version:      1.4.0
I (325) app_init: Compile time:     Sep 29 2026 14:16:45
I (330) app_init: ELF file SHA256:  f7a307237...
I (334) app_init: ESP-IDF:          v6.0.1
I (338) efuse_init: Min chip rev:     v0.0
I (342) efuse_init: Max chip rev:     v0.99 
I (346) efuse_init: Chip rev:         v0.2
I (350) heap_init: Initializing. RAM available for dynamic allocation:
I (356) heap_init: At 3FCA0460 len 000492B0 (292 KiB): RAM
I (361) heap_init: At 3FCE9710 len 00005724 (21 KiB): RAM
I (366) heap_init: At 3FCF0000 len 00008000 (32 KiB): DRAM
I (372) heap_init: At 600FE000 len 00001FE8 (7 KiB): RTCRAM
I (378) spi_flash: detected chip: mxic
I (380) spi_flash: flash io: dio
W (383) spi_flash: Detected size(16384k) larger than the size in the binary image header(2048k). Using the size in the binary image header.
I (396) sleep_gpio: Configure to isolate all GPIO pins in sleep state
I (402) sleep_gpio: Enable automatic switching of GPIO sleep configuration
I (409) main_task: Started on CPU0
I (429) main_task: Calling app_main()
I (449) temperature_sensor: Range [-10°C ~ 80°C], error < 1°C
I (449) pp: pp rom version: e7ae62f
I (459) net80211: net80211 rom version: e7ae62f
I (469) wifi:wifi driver task: 3fced4cc, prio:23, stack:6656, core=0
I (469) wifi:wifi firmware version: b37c951
I (469) wifi:wifi certification version: v7.0
I (479) wifi:config NVS flash: enabled
I (479) wifi:config nano formatting: disabled
I (479) wifi:Init data frame dynamic rx buffer num: 32
I (479) wifi:Init static rx mgmt buffer num: 5
I (489) wifi:Init management short buffer num: 32
I (489) wifi:Init dynamic tx buffer num: 32
I (499) wifi:Init static tx FG buffer num: 2
I (499) wifi:Init static rx buffer size: 1600
I (499) wifi:Init static rx buffer num: 10
I (509) wifi:Init dynamic rx buffer num: 32
I (509) wifi_init: rx ba win: 6
I (519) wifi_init: accept mbox: 6
I (519) wifi_init: tcpip mbox: 32
I (519) wifi_init: udp mbox: 6
I (519) wifi_init: tcp mbox: 6
I (529) wifi_init: tcp tx win: 5760
I (529) wifi_init: tcp rx win: 5760
I (529) wifi_init: tcp mss: 1440
I (539) wifi_init: WiFi IRAM OP enabled
I (539) wifi_init: WiFi RX IRAM OP enabled
I (539) phy_init: phy_version 711,97bcf0a2,Aug 25 2025,19:04:10
I (599) wifi:mode : sta (90:70:69:31:a6:8c)
I (599) wifi:enable tsf
I (599) wifi station: wifi initialized. Type 'connect' to join a network (interactive)
I (599) wifi station: [OTA] running partition: ota_0, version 1.4.0
W (609) wifi station: [OTA] new firmware, state PENDING_VERIFY - running self-check...
I (649) wifi station: [OTA] self-check passed, firmware marked VALID
```

**ota install 1.3.0 force**

```text
I (230899) wifi station: [OTA] current version: 1.5.0 (partition ota_0)
I (230899) wifi station: [OTA] target partition: ota_1
I (230899) wifi station: [OTA] downloading: https://raw.githubusercontent.com/BohdanHorbanych/esp32-ota-files/main/firmware/v1.3.0/station_WiFi.bin
I (230919) wifi:<ba-add>idx:1 (ifx:0, 32:16:9d:25:b8:9e), tid:0, ssn:1, winSize:64
I (231319) esp-x509-crt-bundle: Certificate validated
I (232329) esp_https_ota: Starting OTA...
I (232329) esp_https_ota: Writing to <ota_1> partition at offset 0x100000
I (232339) wifi station: [OTA] new version: 1.3.0
I (234149) wifi station: [OTA] progress: 10% (91136 / 907616 bytes)
I (235949) wifi station: [OTA] progress: 20% (185344 / 907616 bytes)
I (237689) wifi station: [OTA] progress: 30% (275456 / 907616 bytes)
I (239579) wifi station: [OTA] progress: 40% (365568 / 907616 bytes)
I (241279) wifi station: [OTA] progress: 50% (455680 / 907616 bytes)
I (243119) wifi station: [OTA] progress: 60% (545792 / 907616 bytes)
I (244979) wifi station: [OTA] progress: 70% (635904 / 907616 bytes)
I (246669) wifi station: [OTA] progress: 80% (730112 / 907616 bytes)
I (248419) wifi station: [OTA] progress: 90% (820224 / 907616 bytes)
I (250099) wifi station: [OTA] progress: 100% (907616 / 907616 bytes)
I (250099) esp_image: segment 0: paddr=00100020 vaddr=3c0a0020 size=3341ch (209948) map
I (250129) esp_image: segment 1: paddr=00133444 vaddr=3fc97100 size=0506ch ( 20588) 
I (250139) esp_image: segment 2: paddr=001384b8 vaddr=40374000 size=07b60h ( 31584) 
I (250139) esp_image: segment 3: paddr=00140020 vaddr=42000020 size=92368h (598888) map
I (250219) esp_image: segment 4: paddr=001d2390 vaddr=4037bb60 size=0b574h ( 46452) 
I (250229) esp_image: segment 5: paddr=001dd90c vaddr=50000000 size=00024h (    36) 
I (250229) esp_image: segment 0: paddr=00100020 vaddr=3c0a0020 size=3341ch (209948) map
I (250259) esp_image: segment 1: paddr=00133444 vaddr=3fc97100 size=0506ch ( 20588) 
I (250259) esp_image: segment 2: paddr=001384b8 vaddr=40374000 size=07b60h ( 31584) 
I (250269) esp_image: segment 3: paddr=00140020 vaddr=42000020 size=92368h (598888) map
I (250349) esp_image: segment 4: paddr=001d2390 vaddr=4037bb60 size=0b574h ( 46452) 
I (250359) esp_image: segment 5: paddr=001dd90c vaddr=50000000 size=00024h (    36) 
I (250399) wifi station: [OTA] success: 1.5.0 -> 1.3.0 in 18 s. Rebooting...
I (250899) wifi:state: run -> init (0x0)
I (250909) wifi:pm stop, total sleep time: 15334411 us / 36536401 us

I (250909) wifi:<ba-del>idx:1, tid:0
I (250909) wifi:<ba-del>idx:0, tid:5
I (250909) wifi:new:<5,0>, old:<5,1>, ap:<255,255>, sta:<5,1>, prof:1, snd_ch_cfg:0x0
I (250919) wifi station: retry to connect to the AP
I (250949) wifi:flush txq
I (250949) wifi:stop sw txq
I (250949) wifi:lmac stop hw txq
ESP-ROM:esp32s3-20210327
Build:Mar 27 2021
rst:0xc (RTC_SW_CPU_RST),boot:0x2b (SPI_FAST_FLASH_BOOT)
Saved PC:0x4037d308
SPIWP:0xee
mode:DIO, clock div:1
load:0x3fce2820,len:0x14f0
load:0x403c8700,len:0xda0
load:0x403cb700,len:0x2fa0
entry 0x403c8908
I (29) boot: ESP-IDF v6.0.1 2nd stage bootloader
I (29) boot: compile time Sep 29 2026 14:16:01
I (29) boot: Multicore bootloader
I (29) boot: chip revision: v0.2
I (32) boot: efuse block revision: v1.4
I (36) boot.esp32s3: Boot SPI Speed : 80MHz
I (40) boot.esp32s3: SPI Mode       : DIO
I (43) boot.esp32s3: SPI Flash Size : 2MB
I (47) boot: Enabling RNG early entropy source...
I (52) boot: Partition Table:
I (54) boot: ## Label            Usage          Type ST Offset   Length
I (61) boot:  0 nvs              WiFi data        01 02 00009000 00004000
I (67) boot:  1 otadata          OTA data         01 00 0000d000 00002000
I (74) boot:  2 ota_0            OTA app          00 10 00010000 000f0000
I (80) boot:  3 ota_1            OTA app          00 11 00100000 000f0000
I (87) boot: End of partition table
I (115) esp_image: segment 0: paddr=00100020 vaddr=3c0a0020 size=3341ch (209948) map
I (153) esp_image: segment 1: paddr=00133444 vaddr=3fc97100 size=0506ch ( 20588) load
I (158) esp_image: segment 2: paddr=001384b8 vaddr=40374000 size=07b60h ( 31584) load
I (165) esp_image: segment 3: paddr=00140020 vaddr=42000020 size=92368h (598888) map
I (273) esp_image: segment 4: paddr=001d2390 vaddr=4037bb60 size=0b574h ( 46452) load
I (283) esp_image: segment 5: paddr=001dd90c vaddr=50000000 size=00024h (    36) load
I (292) boot: Loaded app from partition at offset 0x100000
I (292) boot: Disabling RNG early entropy source...
I (302) cpu_start: Multicore app
I (311) cpu_start: GPIO 44 and 43 are used as console UART I/O pins
I (311) cpu_start: Pro cpu start user code
I (311) cpu_start: cpu freq: 160000000 Hz
I (313) app_init: Application information:
I (317) app_init: Project name:     station_WiFi
I (321) app_init: App version:      1.3.0
I (325) app_init: Compile time:     Sep 29 2026 14:15:53
I (330) app_init: ELF file SHA256:  7fc2e6354...
I (334) app_init: ESP-IDF:          v6.0.1
I (338) efuse_init: Min chip rev:     v0.0
I (342) efuse_init: Max chip rev:     v0.99 
I (346) efuse_init: Chip rev:         v0.2
I (350) heap_init: Initializing. RAM available for dynamic allocation:
I (356) heap_init: At 3FCA0460 len 000492B0 (292 KiB): RAM
I (361) heap_init: At 3FCE9710 len 00005724 (21 KiB): RAM
I (366) heap_init: At 3FCF0000 len 00008000 (32 KiB): DRAM
I (371) heap_init: At 600FE000 len 00001FE8 (7 KiB): RTCRAM
I (378) spi_flash: detected chip: mxic
I (380) spi_flash: flash io: dio
W (383) spi_flash: Detected size(16384k) larger than the size in the binary image header(2048k). Using the size in the binary image header.
I (396) sleep_gpio: Configure to isolate all GPIO pins in sleep state
I (402) sleep_gpio: Enable automatic switching of GPIO sleep configuration
I (409) main_task: Started on CPU0
I (429) main_task: Calling app_main()
I (449) temperature_sensor: Range [-10°C ~ 80°C], error < 1°C
I (449) pp: pp rom version: e7ae62f
I (459) net80211: net80211 rom version: e7ae62f
I (469) wifi:wifi driver task: 3fced4cc, prio:23, stack:6656, core=0
I (469) wifi:wifi firmware version: b37c951
I (469) wifi:wifi certification version: v7.0
I (479) wifi:config NVS flash: enabled
I (479) wifi:config nano formatting: disabled
I (479) wifi:Init data frame dynamic rx buffer num: 32
I (479) wifi:Init static rx mgmt buffer num: 5
I (489) wifi:Init management short buffer num: 32
I (489) wifi:Init dynamic tx buffer num: 32
I (499) wifi:Init static tx FG buffer num: 2
I (499) wifi:Init static rx buffer size: 1600
I (499) wifi:Init static rx buffer num: 10
I (509) wifi:Init dynamic rx buffer num: 32
I (509) wifi_init: rx ba win: 6
I (519) wifi_init: accept mbox: 6
I (519) wifi_init: tcpip mbox: 32
I (519) wifi_init: udp mbox: 6
I (519) wifi_init: tcp mbox: 6
I (529) wifi_init: tcp tx win: 5760
I (529) wifi_init: tcp rx win: 5760
I (529) wifi_init: tcp mss: 1440
I (539) wifi_init: WiFi IRAM OP enabled
I (539) wifi_init: WiFi RX IRAM OP enabled
I (539) phy_init: phy_version 711,97bcf0a2,Aug 25 2025,19:04:10
I (589) wifi:mode : sta (90:70:69:31:a6:8c)
I (599) wifi:enable tsf
I (599) wifi station: wifi initialized. Type 'connect' to join a network (interactive)
I (599) wifi station: [OTA] running partition: ota_1, version 1.3.0
W (599) wifi station: [OTA] new firmware, state PENDING_VERIFY - running self-check...
I (649) wifi station: [OTA] self-check passed, firmware marked VALID
```

**ota broken**

```text
I (103289) wifi station: [OTA] current version: 1.4.0 (partition ota_0)
I (103289) wifi station: [OTA] target partition: ota_1
I (103289) wifi station: [OTA] downloading: https://raw.githubusercontent.com/BohdanHorbanych/esp32-ota-files/main/firmware/broken/station_WiFi.bin
I (103319) wifi:<ba-add>idx:1 (ifx:0, 32:16:9d:25:b8:2e), tid:0, ssn:1, winSize:64
I (103789) esp-x509-crt-bundle: Certificate validated
I (104779) esp_https_ota: Starting OTA...
I (104779) esp_https_ota: Writing to <ota_1> partition at offset 0x100000
I (104789) wifi station: [OTA] new version: 1.9.0-broken
I (107069) wifi station: [OTA] progress: 10% (91136 / 907840 bytes)
I (109379) wifi station: [OTA] progress: 20% (185344 / 907840 bytes)
I (111169) wifi station: [OTA] progress: 30% (275456 / 907840 bytes)
I (113409) wifi station: [OTA] progress: 40% (365568 / 907840 bytes)
I (115259) wifi station: [OTA] progress: 50% (455680 / 907840 bytes)
I (117289) wifi station: [OTA] progress: 60% (545792 / 907840 bytes)
I (119099) wifi station: [OTA] progress: 70% (635904 / 907840 bytes)
I (121159) wifi station: [OTA] progress: 80% (730112 / 907840 bytes)
I (123329) wifi station: [OTA] progress: 90% (820224 / 907840 bytes)
I (125109) wifi station: [OTA] progress: 100% (907840 / 907840 bytes)
I (125109) esp_image: segment 0: paddr=00100020 vaddr=3c0a0020 size=334ach (210092) map
I (125139) esp_image: segment 1: paddr=001334d4 vaddr=3fc97100 size=0506ch ( 20588) 
I (125149) esp_image: segment 2: paddr=00138548 vaddr=40374000 size=07ad0h ( 31440) 
I (125149) esp_image: segment 3: paddr=00140020 vaddr=42000020 size=923bch (598972) map
I (125229) esp_image: segment 4: paddr=001d23e4 vaddr=4037bad0 size=0b604h ( 46596) 
I (125239) esp_image: segment 5: paddr=001dd9f0 vaddr=50000000 size=00024h (    36) 
I (125239) esp_image: segment 0: paddr=00100020 vaddr=3c0a0020 size=334ach (210092) map
I (125269) esp_image: segment 1: paddr=001334d4 vaddr=3fc97100 size=0506ch ( 20588) 
I (125269) esp_image: segment 2: paddr=00138548 vaddr=40374000 size=07ad0h ( 31440) 
I (125279) esp_image: segment 3: paddr=00140020 vaddr=42000020 size=923bch (598972) map
I (125359) esp_image: segment 4: paddr=001d23e4 vaddr=4037bad0 size=0b604h ( 46596) 
I (125369) esp_image: segment 5: paddr=001dd9f0 vaddr=50000000 size=00024h (    36) 
I (125409) wifi station: [OTA] success: 1.4.0 -> 1.9.0-broken in 20 s. Rebooting...
I (125909) wifi:state: run -> init (0x0)
I (125919) wifi:pm stop, total sleep time: 6740206 us / 29510436 us

I (125919) wifi:<ba-del>idx:1, tid:0
I (125919) wifi:<ba-del>idx:0, tid:5
I (125919) wifi:new:<5,0>, old:<5,1>, ap:<255,255>, sta:<5,1>, prof:1, snd_ch_cfg:0x0
I (125929) wifi station: retry to connect to the AP
I (125969) wifi:flush txq
I (125969) wifi:stop sw txq
I (125969) wifi:lmac stop hw txq
␀�ESP-ROM:esp32s3-20210327
Build:Mar 27 2021
rst:0xc (RTC_SW_CPU_RST),boot:0x2b (SPI_FAST_FLASH_BOOT)
Saved PC:0x4037d308
SPIWP:0xee
mode:DIO, clock div:1
load:0x3fce2820,len:0x14f0
load:0x403c8700,len:0xda0
load:0x403cb700,len:0x2fa0
entry 0x403c8908
I (29) boot: ESP-IDF v6.0.1 2nd stage bootloader
I (29) boot: compile time Sep 29 2026 14:16:01
I (29) boot: Multicore bootloader
I (29) boot: chip revision: v0.2
I (32) boot: efuse block revision: v1.4
I (36) boot.esp32s3: Boot SPI Speed : 80MHz
I (40) boot.esp32s3: SPI Mode       : DIO
I (43) boot.esp32s3: SPI Flash Size : 2MB
I (47) boot: Enabling RNG early entropy source...
I (52) boot: Partition Table:
I (54) boot: ## Label            Usage          Type ST Offset   Length
I (61) boot:  0 nvs              WiFi data        01 02 00009000 00004000
I (67) boot:  1 otadata          OTA data         01 00 0000d000 00002000
I (74) boot:  2 ota_0            OTA app          00 10 00010000 000f0000
I (80) boot:  3 ota_1            OTA app          00 11 00100000 000f0000
I (87) boot: End of partition table
I (115) esp_image: segment 0: paddr=00100020 vaddr=3c0a0020 size=334ach (210092) map
I (153) esp_image: segment 1: paddr=001334d4 vaddr=3fc97100 size=0506ch ( 20588) load
I (158) esp_image: segment 2: paddr=00138548 vaddr=40374000 size=07ad0h ( 31440) load
I (165) esp_image: segment 3: paddr=00140020 vaddr=42000020 size=923bch (598972) map
I (273) esp_image: segment 4: paddr=001d23e4 vaddr=4037bad0 size=0b604h ( 46596) load
I (283) esp_image: segment 5: paddr=001dd9f0 vaddr=50000000 size=00024h (    36) load
I (292) boot: Loaded app from partition at offset 0x100000
I (292) boot: Disabling RNG early entropy source...
I (302) cpu_start: Multicore app
I (311) cpu_start: GPIO 44 and 43 are used as console UART I/O pins
I (311) cpu_start: Pro cpu start user code
I (311) cpu_start: cpu freq: 160000000 Hz
I (313) app_init: Application information:
I (317) app_init: Project name:     station_WiFi
I (321) app_init: App version:      1.9.0-broken
I (326) app_init: Compile time:     Sep 29 2026 14:18:27
I (331) app_init: ELF file SHA256:  d47fe8b01...
I (335) app_init: ESP-IDF:          v6.0.1
I (339) efuse_init: Min chip rev:     v0.0
I (343) efuse_init: Max chip rev:     v0.99 
I (347) efuse_init: Chip rev:         v0.2
I (350) heap_init: Initializing. RAM available for dynamic allocation:
I (357) heap_init: At 3FCA0460 len 000492B0 (292 KiB): RAM
I (362) heap_init: At 3FCE9710 len 00005724 (21 KiB): RAM
I (367) heap_init: At 3FCF0000 len 00008000 (32 KiB): DRAM
I (372) heap_init: At 600FE000 len 00001FE8 (7 KiB): RTCRAM
I (378) spi_flash: detected chip: mxic
I (381) spi_flash: flash io: dio
W (384) spi_flash: Detected size(16384k) larger than the size in the binary image header(2048k). Using the size in the binary image header.
I (397) sleep_gpio: Configure to isolate all GPIO pins in sleep state
I (403) sleep_gpio: Enable automatic switching of GPIO sleep configuration
I (410) main_task: Started on CPU0
I (430) main_task: Calling app_main()
I (450) temperature_sensor: Range [-10°C ~ 80°C], error < 1°C
I (450) pp: pp rom version: e7ae62f
I (460) net80211: net80211 rom version: e7ae62f
I (470) wifi:wifi driver task: 3fced4cc, prio:23, stack:6656, core=0
I (470) wifi:wifi firmware version: b37c951
I (470) wifi:wifi certification version: v7.0
I (480) wifi:config NVS flash: enabled
I (480) wifi:config nano formatting: disabled
I (480) wifi:Init data frame dynamic rx buffer num: 32
I (480) wifi:Init static rx mgmt buffer num: 5
I (490) wifi:Init management short buffer num: 32
I (490) wifi:Init dynamic tx buffer num: 32
I (500) wifi:Init static tx FG buffer num: 2
I (500) wifi:Init static rx buffer size: 1600
I (500) wifi:Init static rx buffer num: 10
I (510) wifi:Init dynamic rx buffer num: 32
I (510) wifi_init: rx ba win: 6
I (520) wifi_init: accept mbox: 6
I (520) wifi_init: tcpip mbox: 32
I (520) wifi_init: udp mbox: 6
I (520) wifi_init: tcp mbox: 6
I (530) wifi_init: tcp tx win: 5760
I (530) wifi_init: tcp rx win: 5760
I (530) wifi_init: tcp mss: 1440
I (540) wifi_init: WiFi IRAM OP enabled
I (540) wifi_init: WiFi RX IRAM OP enabled
I (540) phy_init: phy_version 711,97bcf0a2,Aug 25 2025,19:04:10
I (600) wifi:mode : sta (90:70:69:31:a6:8c)
I (600) wifi:enable tsf
I (600) wifi station: wifi initialized. Type 'connect' to join a network (interactive)
I (600) wifi station: [OTA] running partition: ota_1, version 1.9.0-broken
W (610) wifi station: [OTA] new firmware, state PENDING_VERIFY - running self-check...
E (610) wifi station: [OTA] self-check FAILED (this build is intentionally broken)
E (620) wifi station: [OTA] rolling back to previous firmware...
I (1280) esp_ota_ops: Rollback to previously worked partition.
I (1280) wifi:flush txq
I (1280) wifi:stop sw txq
I (1280) wifi:lmac stop hw txq
���ESP-ROM:esp32s3-20210327
Build:Mar 27 2021
rst:0xc (RTC_SW_CPU_RST),boot:0x2b (SPI_FAST_FLASH_BOOT)
Saved PC:0x4037d308
SPIWP:0xee
mode:DIO, clock div:1
load:0x3fce2820,len:0x14f0
load:0x403c8700,len:0xda0
load:0x403cb700,len:0x2fa0
entry 0x403c8908
I (29) boot: ESP-IDF v6.0.1 2nd stage bootloader
I (29) boot: compile time Sep 29 2026 14:16:01
I (29) boot: Multicore bootloader
I (29) boot: chip revision: v0.2
I (32) boot: efuse block revision: v1.4
I (36) boot.esp32s3: Boot SPI Speed : 80MHz
I (40) boot.esp32s3: SPI Mode       : DIO
I (43) boot.esp32s3: SPI Flash Size : 2MB
I (47) boot: Enabling RNG early entropy source...
I (52) boot: Partition Table:
I (54) boot: ## Label            Usage          Type ST Offset   Length
I (61) boot:  0 nvs              WiFi data        01 02 00009000 00004000
I (67) boot:  1 otadata          OTA data         01 00 0000d000 00002000
I (74) boot:  2 ota_0            OTA app          00 10 00010000 000f0000
I (80) boot:  3 ota_1            OTA app          00 11 00100000 000f0000
I (87) boot: End of partition table
I (90) esp_image: segment 0: paddr=00010020 vaddr=3c0a0020 size=3349ch (210076) map
I (135) esp_image: segment 1: paddr=000434c4 vaddr=3fc97100 size=0506ch ( 20588) load
I (140) esp_image: segment 2: paddr=00048538 vaddr=40374000 size=07ae0h ( 31456) load
I (147) esp_image: segment 3: paddr=00050020 vaddr=42000020 size=923ech (599020) map
I (255) esp_image: segment 4: paddr=000e2414 vaddr=4037bae0 size=0b5f4h ( 46580) load
I (265) esp_image: segment 5: paddr=000eda10 vaddr=50000000 size=00024h (    36) load
I (274) boot: Loaded app from partition at offset 0x10000
I (274) boot: Disabling RNG early entropy source...
I (284) cpu_start: Multicore app
I (292) cpu_start: GPIO 44 and 43 are used as console UART I/O pins
I (293) cpu_start: Pro cpu start user code
I (293) cpu_start: cpu freq: 160000000 Hz
I (295) app_init: Application information:
I (299) app_init: Project name:     station_WiFi
I (303) app_init: App version:      1.4.0
I (307) app_init: Compile time:     Sep 29 2026 14:16:45
I (312) app_init: ELF file SHA256:  f7a307237...
I (316) app_init: ESP-IDF:          v6.0.1
I (320) efuse_init: Min chip rev:     v0.0
I (324) efuse_init: Max chip rev:     v0.99 
I (328) efuse_init: Chip rev:         v0.2
I (332) heap_init: Initializing. RAM available for dynamic allocation:
I (338) heap_init: At 3FCA0460 len 000492B0 (292 KiB): RAM
I (343) heap_init: At 3FCE9710 len 00005724 (21 KiB): RAM
I (348) heap_init: At 3FCF0000 len 00008000 (32 KiB): DRAM
I (353) heap_init: At 600FE000 len 00001FE8 (7 KiB): RTCRAM
I (359) spi_flash: detected chip: mxic
I (362) spi_flash: flash io: dio
W (365) spi_flash: Detected size(16384k) larger than the size in the binary image header(2048k). Using the size in the binary image header.
I (378) sleep_gpio: Configure to isolate all GPIO pins in sleep state
I (384) sleep_gpio: Enable automatic switching of GPIO sleep configuration
I (391) main_task: Started on CPU0
I (411) main_task: Calling app_main()
I (431) temperature_sensor: Range [-10°C ~ 80°C], error < 1°C
I (431) pp: pp rom version: e7ae62f
I (441) net80211: net80211 rom version: e7ae62f
I (451) wifi:wifi driver task: 3fced4cc, prio:23, stack:6656, core=0
I (451) wifi:wifi firmware version: b37c951
I (451) wifi:wifi certification version: v7.0
I (461) wifi:config NVS flash: enabled
I (461) wifi:config nano formatting: disabled
I (461) wifi:Init data frame dynamic rx buffer num: 32
I (461) wifi:Init static rx mgmt buffer num: 5
I (471) wifi:Init management short buffer num: 32
I (471) wifi:Init dynamic tx buffer num: 32
I (481) wifi:Init static tx FG buffer num: 2
I (481) wifi:Init static rx buffer size: 1600
I (481) wifi:Init static rx buffer num: 10
I (491) wifi:Init dynamic rx buffer num: 32
I (491) wifi_init: rx ba win: 6
I (501) wifi_init: accept mbox: 6
I (501) wifi_init: tcpip mbox: 32
I (501) wifi_init: udp mbox: 6
I (501) wifi_init: tcp mbox: 6
I (511) wifi_init: tcp tx win: 5760
I (511) wifi_init: tcp rx win: 5760
I (511) wifi_init: tcp mss: 1440
I (521) wifi_init: WiFi IRAM OP enabled
I (521) wifi_init: WiFi RX IRAM OP enabled
I (521) phy_init: phy_version 711,97bcf0a2,Aug 25 2025,19:04:10
I (581) wifi:mode : sta (90:70:69:31:a6:8c)
I (581) wifi:enable tsf
I (581) wifi station: wifi initialized. Type 'connect' to join a network (interactive)
I (581) wifi station: [OTA] running partition: ota_0, version 1.4.0
I (591) wifi station: saved credentials found but auto-connect disabled. Type 'connect' to connect.
I (601) wifi station: station_WiFi fw v1.4.0 ready. Type 'help' for commands
```

**ota https://raw.githubusercontent.com/BohdanHorbanych/esp32-ota-files/main/firmware/v1.5.0/station_WiFi.bin**

```text
I (426031) wifi station: [OTA] current version: 1.4.0 (partition ota_0)
I (426031) wifi station: [OTA] target partition: ota_1
I (426031) wifi station: [OTA] downloading: https://raw.githubusercontent.com/BohdanHorbanych/esp32-ota-files/main/firmware/v1.5.0/station_WiFi.bin
I (426401) esp-x509-crt-bundle: Certificate validated
I (427241) esp_https_ota: Starting OTA...
I (427241) esp_https_ota: Writing to <ota_1> partition at offset 0x100000
I (427241) wifi station: [OTA] new version: 1.5.0
I (429381) wifi station: [OTA] progress: 10% (91136 / 908304 bytes)
I (431401) wifi station: [OTA] progress: 20% (185344 / 908304 bytes)
I (433141) wifi station: [OTA] progress: 30% (275456 / 908304 bytes)
I (434781) wifi station: [OTA] progress: 40% (365568 / 908304 bytes)
I (436421) wifi station: [OTA] progress: 50% (455680 / 908304 bytes)
I (438261) wifi station: [OTA] progress: 60% (545792 / 908304 bytes)
I (439801) wifi station: [OTA] progress: 70% (635904 / 908304 bytes)
I (441591) wifi station: [OTA] progress: 80% (730112 / 908304 bytes)
I (443371) wifi station: [OTA] progress: 90% (820224 / 908304 bytes)
I (444791) wifi station: [OTA] progress: 100% (908304 / 908304 bytes)
I (444791) esp_image: segment 0: paddr=00100020 vaddr=3c0a0020 size=3352ch (210220) map
I (444821) esp_image: segment 1: paddr=00133554 vaddr=3fc97100 size=0506ch ( 20588) 
I (444831) esp_image: segment 2: paddr=001385c8 vaddr=40374000 size=07a50h ( 31312) 
I (444831) esp_image: segment 3: paddr=00140020 vaddr=42000020 size=92508h (599304) map
I (444911) esp_image: segment 4: paddr=001d2530 vaddr=4037ba50 size=0b684h ( 46724) 
I (444921) esp_image: segment 5: paddr=001ddbbc vaddr=50000000 size=00024h (    36) 
I (444921) esp_image: segment 0: paddr=00100020 vaddr=3c0a0020 size=3352ch (210220) map
I (444951) esp_image: segment 1: paddr=00133554 vaddr=3fc97100 size=0506ch ( 20588) 
I (444961) esp_image: segment 2: paddr=001385c8 vaddr=40374000 size=07a50h ( 31312) 
I (444961) esp_image: segment 3: paddr=00140020 vaddr=42000020 size=92508h (599304) map
I (445051) esp_image: segment 4: paddr=001d2530 vaddr=4037ba50 size=0b684h ( 46724) 
I (445051) esp_image: segment 5: paddr=001ddbbc vaddr=50000000 size=00024h (    36) 
I (445091) wifi station: [OTA] success: 1.4.0 -> 1.5.0 in 17 s. Rebooting...
I (445591) wifi:state: run -> init (0x0)
I (445601) wifi:pm stop, total sleep time: 107668450 us / 141448329 us

I (445601) wifi:<ba-del>idx:1, tid:0
I (445601) wifi:<ba-del>idx:0, tid:5
I (445601) wifi:new:<5,0>, old:<5,1>, ap:<255,255>, sta:<5,1>, prof:1, snd_ch_cfg:0x0
I (445611) wifi station: retry to connect to the AP
I (445641) wifi:flush txq
I (445641) wifi:stop sw txq
I (445641) wifi:lmac stop hw txq
␀�ESP-ROM:esp32s3-20210327
Build:Mar 27 2021
rst:0xc (RTC_SW_CPU_RST),boot:0x2b (SPI_FAST_FLASH_BOOT)
Saved PC:0x4037d308
SPIWP:0xee
mode:DIO, clock div:1
load:0x3fce2820,len:0x14f0
load:0x403c8700,len:0xda0
load:0x403cb700,len:0x2fa0
entry 0x403c8908
I (29) boot: ESP-IDF v6.0.1 2nd stage bootloader
I (29) boot: compile time Sep 29 2026 14:16:01
I (29) boot: Multicore bootloader
I (29) boot: chip revision: v0.2
I (32) boot: efuse block revision: v1.4
I (36) boot.esp32s3: Boot SPI Speed : 80MHz
I (40) boot.esp32s3: SPI Mode       : DIO
I (43) boot.esp32s3: SPI Flash Size : 2MB
I (47) boot: Enabling RNG early entropy source...
I (52) boot: Partition Table:
I (54) boot: ## Label            Usage          Type ST Offset   Length
I (61) boot:  0 nvs              WiFi data        01 02 00009000 00004000
I (67) boot:  1 otadata          OTA data         01 00 0000d000 00002000
I (74) boot:  2 ota_0            OTA app          00 10 00010000 000f0000
I (80) boot:  3 ota_1            OTA app          00 11 00100000 000f0000
I (87) boot: End of partition table
I (115) esp_image: segment 0: paddr=00100020 vaddr=3c0a0020 size=3352ch (210220) map
I (153) esp_image: segment 1: paddr=00133554 vaddr=3fc97100 size=0506ch ( 20588) load
I (158) esp_image: segment 2: paddr=001385c8 vaddr=40374000 size=07a50h ( 31312) load
I (165) esp_image: segment 3: paddr=00140020 vaddr=42000020 size=92508h (599304) map
I (273) esp_image: segment 4: paddr=001d2530 vaddr=4037ba50 size=0b684h ( 46724) load
I (283) esp_image: segment 5: paddr=001ddbbc vaddr=50000000 size=00024h (    36) load
I (292) boot: Loaded app from partition at offset 0x100000
I (292) boot: Disabling RNG early entropy source...
I (302) cpu_start: Multicore app
I (311) cpu_start: GPIO 44 and 43 are used as console UART I/O pins
I (311) cpu_start: Pro cpu start user code
I (311) cpu_start: cpu freq: 160000000 Hz
I (313) app_init: Application information:
I (317) app_init: Project name:     station_WiFi
I (321) app_init: App version:      1.5.0
I (325) app_init: Compile time:     Sep 29 2026 14:17:34
I (330) app_init: ELF file SHA256:  486cd296d...
I (334) app_init: ESP-IDF:          v6.0.1
I (338) efuse_init: Min chip rev:     v0.0
I (342) efuse_init: Max chip rev:     v0.99 
I (346) efuse_init: Chip rev:         v0.2
I (350) heap_init: Initializing. RAM available for dynamic allocation:
I (356) heap_init: At 3FCA0460 len 000492B0 (292 KiB): RAM
I (361) heap_init: At 3FCE9710 len 00005724 (21 KiB): RAM
I (366) heap_init: At 3FCF0000 len 00008000 (32 KiB): DRAM
I (372) heap_init: At 600FE000 len 00001FE8 (7 KiB): RTCRAM
I (378) spi_flash: detected chip: mxic
I (380) spi_flash: flash io: dio
W (383) spi_flash: Detected size(16384k) larger than the size in the binary image header(2048k). Using the size in the binary image header.
I (396) sleep_gpio: Configure to isolate all GPIO pins in sleep state
I (402) sleep_gpio: Enable automatic switching of GPIO sleep configuration
I (409) main_task: Started on CPU0
I (429) main_task: Calling app_main()
I (449) temperature_sensor: Range [-10°C ~ 80°C], error < 1°C
I (449) wifi station: [CFG] migrating settings to v2 format...
I (569) wifi station: [CFG] migration done
I (579) pp: pp rom version: e7ae62f
I (579) net80211: net80211 rom version: e7ae62f
I (599) wifi:wifi driver task: 3fceed90, prio:23, stack:6656, core=0
I (599) wifi:wifi firmware version: b37c951
I (599) wifi:wifi certification version: v7.0
I (599) wifi:config NVS flash: enabled
I (599) wifi:config nano formatting: disabled
I (609) wifi:Init data frame dynamic rx buffer num: 32
I (609) wifi:Init static rx mgmt buffer num: 5
I (609) wifi:Init management short buffer num: 32
I (619) wifi:Init dynamic tx buffer num: 32
I (619) wifi:Init static tx FG buffer num: 2
I (629) wifi:Init static rx buffer size: 1600
I (629) wifi:Init static rx buffer num: 10
I (639) wifi:Init dynamic rx buffer num: 32
I (639) wifi_init: rx ba win: 6
I (639) wifi_init: accept mbox: 6
I (639) wifi_init: tcpip mbox: 32
I (649) wifi_init: udp mbox: 6
I (649) wifi_init: tcp mbox: 6
I (649) wifi_init: tcp tx win: 5760
I (659) wifi_init: tcp rx win: 5760
I (659) wifi_init: tcp mss: 1440
I (659) wifi_init: WiFi IRAM OP enabled
I (669) wifi_init: WiFi RX IRAM OP enabled
I (669) phy_init: phy_version 711,97bcf0a2,Aug 25 2025,19:04:10
W (679) phy_init: failed to load RF calibration data (0x1102), falling back to full calibration
I (729) phy_init: Saving new calibration data due to checksum failure or outdated calibration data, mode(2)
I (739) wifi:mode : sta (90:70:69:31:a6:8c)
I (739) wifi:enable tsf
I (739) wifi station: wifi initialized. Type 'connect' to join a network (interactive)
I (739) wifi station: [OTA] running partition: ota_1, version 1.5.0
W (749) wifi station: [OTA] new firmware, state PENDING_VERIFY - running self-check...
I (789) wifi station: [OTA] self-check passed, firmware marked VALID
```

**ota-test-server**

```text
I (87759) wifi station: === OTA Update Started ===
I (87759) wifi station: Checking for updates...
I (89259) wifi station: Found firmware v2.0.1
I (89259) wifi station: Downloading component: distance_sensor v1.3.0
I (89259) wifi station:   [distance_sensor] downloading... 10%
I (89559) wifi station:   [distance_sensor] downloading... 20%
I (89859) wifi station:   [distance_sensor] downloading... 30%
I (90159) wifi station:   [distance_sensor] downloading... 40%
I (90459) wifi station:   [distance_sensor] downloading... 50%
I (90759) wifi station:   [distance_sensor] downloading... 60%
I (91059) wifi station:   [distance_sensor] downloading... 70%
I (91359) wifi station:   [distance_sensor] downloading... 80%
I (91659) wifi station:   [distance_sensor] downloading... 90%
I (91959) wifi station:   [distance_sensor] downloading... 100%
I (92259) wifi station:   [distance_sensor] installing...
I (93059) wifi station:   [distance_sensor] OK
I (93059) wifi station: Downloading component: relay_controller v2.1.0
I (93059) wifi station:   [relay_controller] downloading... 10%
I (93359) wifi station:   [relay_controller] downloading... 20%
I (93659) wifi station:   [relay_controller] downloading... 30%
I (93959) wifi station:   [relay_controller] downloading... 40%
I (94259) wifi station:   [relay_controller] downloading... 50%
I (94559) wifi station:   [relay_controller] downloading... 60%
I (94859) wifi station:   [relay_controller] downloading... 70%
I (95159) wifi station:   [relay_controller] downloading... 80%
I (95459) wifi station:   [relay_controller] downloading... 90%
I (95759) wifi station:   [relay_controller] downloading... 100%
I (96059) wifi station:   [relay_controller] installing...
I (96859) wifi station:   [relay_controller] OK
I (96859) wifi station: Downloading component: wifi_manager v3.0.2
I (96859) wifi station:   [wifi_manager] downloading... 10%
I (97059) wifi station:   [wifi_manager] downloading... 20%
I (97259) wifi station:   [wifi_manager] downloading... 30%
I (97459) wifi station:   [wifi_manager] downloading... 40%
I (97659) wifi station:   [wifi_manager] downloading... 50%
I (97859) wifi station:   [wifi_manager] downloading... 60%
I (98059) wifi station:   [wifi_manager] downloading... 70%
I (98259) wifi station:   [wifi_manager] downloading... 80%
I (98459) wifi station:   [wifi_manager] downloading... 90%
I (98659) wifi station:   [wifi_manager] downloading... 100%
I (98859) wifi station:   [wifi_manager] installing...
I (99459) wifi station:   [wifi_manager] OK
I (99459) wifi station: Verifying firmware integrity...
I (100459) wifi station: === OTA Update Complete. Restarting... ===
I (101459) wifi:state: run -> init (0x0)
I (101469) wifi:pm stop, total sleep time: 21420200 us / 24306382 us

I (101469) wifi:<ba-del>idx:0, tid:5
I (101469) wifi:new:<5,0>, old:<5,1>, ap:<255,255>, sta:<5,1>, prof:1, snd_ch_cfg:0x0
I (101479) wifi station: retry to connect to the AP
I (101519) wifi:flush txq
I (101519) wifi:stop sw txq
I (101519) wifi:lmac stop hw txq
ESP-ROM:esp32s3-20210327
Build:Mar 27 2021
rst:0xc (RTC_SW_CPU_RST),boot:0x2b (SPI_FAST_FLASH_BOOT)
Saved PC:0x4037d308
SPIWP:0xee
mode:DIO, clock div:1
load:0x3fce2820,len:0x14f0
load:0x403c8700,len:0xda0
load:0x403cb700,len:0x2fa0
entry 0x403c8908
I (29) boot: ESP-IDF v6.0.1 2nd stage bootloader
I (29) boot: compile time Sep 29 2026 14:16:01
I (29) boot: Multicore bootloader
I (29) boot: chip revision: v0.2
I (32) boot: efuse block revision: v1.4
I (36) boot.esp32s3: Boot SPI Speed : 80MHz
I (40) boot.esp32s3: SPI Mode       : DIO
I (43) boot.esp32s3: SPI Flash Size : 2MB
I (47) boot: Enabling RNG early entropy source...
I (52) boot: Partition Table:
I (54) boot: ## Label            Usage          Type ST Offset   Length
I (61) boot:  0 nvs              WiFi data        01 02 00009000 00004000
I (67) boot:  1 otadata          OTA data         01 00 0000d000 00002000
I (74) boot:  2 ota_0            OTA app          00 10 00010000 000f0000
I (80) boot:  3 ota_1            OTA app          00 11 00100000 000f0000
I (87) boot: End of partition table
I (90) esp_image: segment 0: paddr=00100020 vaddr=3c0a0020 size=3352ch (210220) map
I (135) esp_image: segment 1: paddr=00133554 vaddr=3fc97100 size=0506ch ( 20588) load
I (140) esp_image: segment 2: paddr=001385c8 vaddr=40374000 size=07a50h ( 31312) load
I (147) esp_image: segment 3: paddr=00140020 vaddr=42000020 size=92508h (599304) map
I (255) esp_image: segment 4: paddr=001d2530 vaddr=4037ba50 size=0b684h ( 46724) load
I (265) esp_image: segment 5: paddr=001ddbbc vaddr=50000000 size=00024h (    36) load
I (274) boot: Loaded app from partition at offset 0x100000
I (274) boot: Disabling RNG early entropy source...
I (284) cpu_start: Multicore app
I (293) cpu_start: GPIO 44 and 43 are used as console UART I/O pins
I (293) cpu_start: Pro cpu start user code
I (293) cpu_start: cpu freq: 160000000 Hz
I (295) app_init: Application information:
I (299) app_init: Project name:     station_WiFi
I (303) app_init: App version:      1.5.0
I (307) app_init: Compile time:     Sep 29 2026 14:17:34
I (312) app_init: ELF file SHA256:  486cd296d...
I (316) app_init: ESP-IDF:          v6.0.1
I (320) efuse_init: Min chip rev:     v0.0
I (324) efuse_init: Max chip rev:     v0.99 
I (328) efuse_init: Chip rev:         v0.2
I (332) heap_init: Initializing. RAM available for dynamic allocation:
I (338) heap_init: At 3FCA0460 len 000492B0 (292 KiB): RAM
I (343) heap_init: At 3FCE9710 len 00005724 (21 KiB): RAM
I (348) heap_init: At 3FCF0000 len 00008000 (32 KiB): DRAM
I (353) heap_init: At 600FE000 len 00001FE8 (7 KiB): RTCRAM
I (360) spi_flash: detected chip: mxic
I (362) spi_flash: flash io: dio
W (365) spi_flash: Detected size(16384k) larger than the size in the binary image header(2048k). Using the size in the binary image header.
I (378) sleep_gpio: Configure to isolate all GPIO pins in sleep state
I (384) sleep_gpio: Enable automatic switching of GPIO sleep configuration
I (391) main_task: Started on CPU0
I (411) main_task: Calling app_main()
I (431) temperature_sensor: Range [-10°C ~ 80°C], error < 1°C
I (441) pp: pp rom version: e7ae62f
I (441) net80211: net80211 rom version: e7ae62f
I (451) wifi:wifi driver task: 3fced4cc, prio:23, stack:6656, core=0
I (451) wifi:wifi firmware version: b37c951
I (451) wifi:wifi certification version: v7.0
I (461) wifi:config NVS flash: enabled
I (461) wifi:config nano formatting: disabled
I (461) wifi:Init data frame dynamic rx buffer num: 32
I (461) wifi:Init static rx mgmt buffer num: 5
I (471) wifi:Init management short buffer num: 32
I (471) wifi:Init dynamic tx buffer num: 32
I (481) wifi:Init static tx FG buffer num: 2
I (481) wifi:Init static rx buffer size: 1600
I (481) wifi:Init static rx buffer num: 10
I (491) wifi:Init dynamic rx buffer num: 32
I (491) wifi_init: rx ba win: 6
I (501) wifi_init: accept mbox: 6
I (501) wifi_init: tcpip mbox: 32
I (501) wifi_init: udp mbox: 6
I (501) wifi_init: tcp mbox: 6
I (511) wifi_init: tcp tx win: 5760
I (511) wifi_init: tcp rx win: 5760
I (511) wifi_init: tcp mss: 1440
I (521) wifi_init: WiFi IRAM OP enabled
I (521) wifi_init: WiFi RX IRAM OP enabled
I (521) phy_init: phy_version 711,97bcf0a2,Aug 25 2025,19:04:10
I (571) wifi:mode : sta (90:70:69:31:a6:8c)
I (581) wifi:enable tsf
I (581) wifi station: wifi initialized. Type 'connect' to join a network (interactive)
I (581) wifi station: [OTA] running partition: ota_1, version 1.5.0
I (581) wifi station: saved credentials found but auto-connect disabled. Type 'connect' to connect.
I (591) wifi station: station_WiFi fw v1.5.0 ready. Type 'help' for commands
```

**ota update** - *wi-fi interrupted during progress 30%*

```text
I (193969) wifi:<ba-add>idx:1 (ifx:0, 32:16:9d:25:b8:2e), tid:0, ssn:1, winSize:64
I (194409) esp-x509-crt-bundle: Certificate validated
I (195279) wifi station: [OTA] stable channel: 1.4.0, current: 1.3.0
I (195279) wifi station: [OTA] current version: 1.3.0 (partition ota_0)
I (195279) wifi station: [OTA] target partition: ota_1
I (195289) wifi station: [OTA] downloading: https://raw.githubusercontent.com/BohdanHorbanych/esp32-ota-files/main/firmware/v1.4.0/station_WiFi.bin
I (195779) esp-x509-crt-bundle: Certificate validated
I (196709) esp_https_ota: Starting OTA...
I (196709) esp_https_ota: Writing to <ota_1> partition at offset 0x100000
I (196739) wifi station: [OTA] new version: 1.4.0
I (200139) wifi station: [OTA] progress: 10% (91136 / 907872 bytes)
I (203429) wifi station: [OTA] progress: 20% (185344 / 907872 bytes)
I (206059) wifi station: [OTA] progress: 30% (275456 / 907872 bytes)
I (209149) wifi station: [OTA] progress: 40% (365568 / 907872 bytes)
I (211599) wifi station: [OTA] progress: 50% (455680 / 907872 bytes)
I (214329) wifi station: [OTA] progress: 60% (545792 / 907872 bytes)
I (217179) wifi station: [OTA] progress: 70% (635904 / 907872 bytes)
I (219949) wifi station: [OTA] progress: 80% (730112 / 907872 bytes)
I (222799) wifi station: [OTA] progress: 90% (820224 / 907872 bytes)
I (224769) wifi station: [OTA] progress: 100% (907872 / 907872 bytes)
I (224769) esp_image: segment 0: paddr=00100020 vaddr=3c0a0020 size=3349ch (210076) map
I (224799) esp_image: segment 1: paddr=001334c4 vaddr=3fc97100 size=0506ch ( 20588) 
I (224809) esp_image: segment 2: paddr=00138538 vaddr=40374000 size=07ae0h ( 31456) 
I (224809) esp_image: segment 3: paddr=00140020 vaddr=42000020 size=923ech (599020) map
I (224889) esp_image: segment 4: paddr=001d2414 vaddr=4037bae0 size=0b5f4h ( 46580) 
I (224899) esp_image: segment 5: paddr=001dda10 vaddr=50000000 size=00024h (    36) 
I (224899) esp_image: segment 0: paddr=00100020 vaddr=3c0a0020 size=3349ch (210076) map
I (224929) esp_image: segment 1: paddr=001334c4 vaddr=3fc97100 size=0506ch ( 20588) 
I (224929) esp_image: segment 2: paddr=00138538 vaddr=40374000 size=07ae0h ( 31456) 
I (224939) esp_image: segment 3: paddr=00140020 vaddr=42000020 size=923ech (599020) map
I (225029) esp_image: segment 4: paddr=001d2414 vaddr=4037bae0 size=0b5f4h ( 46580) 
I (225029) esp_image: segment 5: paddr=001dda10 vaddr=50000000 size=00024h (    36) 
I (225069) wifi station: [OTA] success: 1.3.0 -> 1.4.0 in 28 s. Rebooting...
I (225569) wifi:state: run -> init (0x0)
I (225579) wifi:pm stop, total sleep time: 7704940 us / 40822362 us

I (225579) wifi:<ba-del>idx:1, tid:0
I (225579) wifi:<ba-del>idx:0, tid:5
I (225579) wifi:new:<5,0>, old:<5,1>, ap:<255,255>, sta:<5,1>, prof:1, snd_ch_cfg:0x0
I (225589) wifi station: retry to connect to the AP
I (225619) wifi:flush txq
I (225619) wifi:stop sw txq
I (225619) wifi:lmac stop hw txq
␀�ESP-ROM:esp32s3-20210327
Build:Mar 27 2021
rst:0xc (RTC_SW_CPU_RST),boot:0x2b (SPI_FAST_FLASH_BOOT)
Saved PC:0x4037d308
SPIWP:0xee
mode:DIO, clock div:1
load:0x3fce2820,len:0x14f0
load:0x403c8700,len:0xda0
load:0x403cb700,len:0x2fa0
entry 0x403c8908
I (29) boot: ESP-IDF v6.0.1 2nd stage bootloader
I (29) boot: compile time Sep 29 2026 14:16:01
I (29) boot: Multicore bootloader
I (29) boot: chip revision: v0.2
I (32) boot: efuse block revision: v1.4
I (36) boot.esp32s3: Boot SPI Speed : 80MHz
I (40) boot.esp32s3: SPI Mode       : DIO
I (43) boot.esp32s3: SPI Flash Size : 2MB
I (47) boot: Enabling RNG early entropy source...
I (52) boot: Partition Table:
I (54) boot: ## Label            Usage          Type ST Offset   Length
I (61) boot:  0 nvs              WiFi data        01 02 00009000 00004000
I (67) boot:  1 otadata          OTA data         01 00 0000d000 00002000
I (74) boot:  2 ota_0            OTA app          00 10 00010000 000f0000
I (80) boot:  3 ota_1            OTA app          00 11 00100000 000f0000
I (87) boot: End of partition table
I (115) esp_image: segment 0: paddr=00100020 vaddr=3c0a0020 size=3349ch (210076) map
I (153) esp_image: segment 1: paddr=001334c4 vaddr=3fc97100 size=0506ch ( 20588) load
I (158) esp_image: segment 2: paddr=00138538 vaddr=40374000 size=07ae0h ( 31456) load
I (165) esp_image: segment 3: paddr=00140020 vaddr=42000020 size=923ech (599020) map
I (273) esp_image: segment 4: paddr=001d2414 vaddr=4037bae0 size=0b5f4h ( 46580) load
I (283) esp_image: segment 5: paddr=001dda10 vaddr=50000000 size=00024h (    36) load
I (292) boot: Loaded app from partition at offset 0x100000
I (292) boot: Disabling RNG early entropy source...
I (302) cpu_start: Multicore app
I (311) cpu_start: GPIO 44 and 43 are used as console UART I/O pins
I (311) cpu_start: Pro cpu start user code
I (311) cpu_start: cpu freq: 160000000 Hz
I (313) app_init: Application information:
I (317) app_init: Project name:     station_WiFi
I (321) app_init: App version:      1.4.0
I (325) app_init: Compile time:     Sep 29 2026 14:16:45
I (330) app_init: ELF file SHA256:  f7a307237...
I (334) app_init: ESP-IDF:          v6.0.1
I (338) efuse_init: Min chip rev:     v0.0
I (342) efuse_init: Max chip rev:     v0.99 
I (346) efuse_init: Chip rev:         v0.2
I (350) heap_init: Initializing. RAM available for dynamic allocation:
I (356) heap_init: At 3FCA0460 len 000492B0 (292 KiB): RAM
I (361) heap_init: At 3FCE9710 len 00005724 (21 KiB): RAM
I (366) heap_init: At 3FCF0000 len 00008000 (32 KiB): DRAM
I (372) heap_init: At 600FE000 len 00001FE8 (7 KiB): RTCRAM
I (378) spi_flash: detected chip: mxic
I (380) spi_flash: flash io: dio
W (383) spi_flash: Detected size(16384k) larger than the size in the binary image header(2048k). Using the size in the binary image header.
I (396) sleep_gpio: Configure to isolate all GPIO pins in sleep state
I (402) sleep_gpio: Enable automatic switching of GPIO sleep configuration
I (409) main_task: Started on CPU0
I (429) main_task: Calling app_main()
I (449) temperature_sensor: Range [-10°C ~ 80°C], error < 1°C
I (449) pp: pp rom version: e7ae62f
I (459) net80211: net80211 rom version: e7ae62f
I (469) wifi:wifi driver task: 3fced4cc, prio:23, stack:6656, core=0
I (469) wifi:wifi firmware version: b37c951
I (469) wifi:wifi certification version: v7.0
I (479) wifi:config NVS flash: enabled
I (479) wifi:config nano formatting: disabled
I (479) wifi:Init data frame dynamic rx buffer num: 32
I (479) wifi:Init static rx mgmt buffer num: 5
I (489) wifi:Init management short buffer num: 32
I (489) wifi:Init dynamic tx buffer num: 32
I (499) wifi:Init static tx FG buffer num: 2
I (499) wifi:Init static rx buffer size: 1600
I (499) wifi:Init static rx buffer num: 10
I (509) wifi:Init dynamic rx buffer num: 32
I (509) wifi_init: rx ba win: 6
I (519) wifi_init: accept mbox: 6
I (519) wifi_init: tcpip mbox: 32
I (519) wifi_init: udp mbox: 6
I (519) wifi_init: tcp mbox: 6
I (529) wifi_init: tcp tx win: 5760
I (529) wifi_init: tcp rx win: 5760
I (529) wifi_init: tcp mss: 1440
I (539) wifi_init: WiFi IRAM OP enabled
I (539) wifi_init: WiFi RX IRAM OP enabled
I (539) phy_init: phy_version 711,97bcf0a2,Aug 25 2025,19:04:10
I (599) wifi:mode : sta (90:70:69:31:a6:8c)
I (599) wifi:enable tsf
I (599) wifi station: wifi initialized. Type 'connect' to join a network (interactive)
I (599) wifi station: [OTA] running partition: ota_1, version 1.4.0
W (609) wifi station: [OTA] new firmware, state PENDING_VERIFY - running self-check...
I (649) wifi station: [OTA] self-check passed, firmware marked VALID
```

**ota update beta** - *wi-fi interrupted during progress 20%*

```text
I (272639) esp-x509-crt-bundle: Certificate validated
I (273479) wifi station: [OTA] beta channel: 1.5.0, current: 1.4.0
I (273489) wifi station: [OTA] current version: 1.4.0 (partition ota_1)
I (273489) wifi station: [OTA] target partition: ota_0
I (273489) wifi station: [OTA] downloading: https://raw.githubusercontent.com/BohdanHorbanych/esp32-ota-files/main/firmware/v1.5.0/station_WiFi.bin
I (273869) esp-x509-crt-bundle: Certificate validated
I (274709) esp_https_ota: Starting OTA...
I (274709) esp_https_ota: Writing to <ota_0> partition at offset 0x10000
I (274719) wifi station: [OTA] new version: 1.5.0
I (276639) wifi station: [OTA] progress: 10% (91136 / 908304 bytes)
I (278459) wifi station: [OTA] progress: 20% (185344 / 908304 bytes)
I (280079) wifi station: [OTA] progress: 30% (275456 / 908304 bytes)
I (281849) wifi station: [OTA] progress: 40% (365568 / 908304 bytes)
I (283679) wifi station: [OTA] progress: 50% (455680 / 908304 bytes)
I (285419) wifi station: [OTA] progress: 60% (545792 / 908304 bytes)
I (287189) wifi station: [OTA] progress: 70% (635904 / 908304 bytes)
I (288839) wifi station: [OTA] progress: 80% (730112 / 908304 bytes)
I (290479) wifi station: [OTA] progress: 90% (820224 / 908304 bytes)
I (292079) wifi station: [OTA] progress: 100% (908304 / 908304 bytes)
I (292079) esp_image: segment 0: paddr=00010020 vaddr=3c0a0020 size=3352ch (210220) map
I (292109) esp_image: segment 1: paddr=00043554 vaddr=3fc97100 size=0506ch ( 20588) 
I (292119) esp_image: segment 2: paddr=000485c8 vaddr=40374000 size=07a50h ( 31312) 
I (292119) esp_image: segment 3: paddr=00050020 vaddr=42000020 size=92508h (599304) map
I (292209) esp_image: segment 4: paddr=000e2530 vaddr=4037ba50 size=0b684h ( 46724) 
I (292209) esp_image: segment 5: paddr=000edbbc vaddr=50000000 size=00024h (    36) 
I (292219) esp_image: segment 0: paddr=00010020 vaddr=3c0a0020 size=3352ch (210220) map
I (292239) esp_image: segment 1: paddr=00043554 vaddr=3fc97100 size=0506ch ( 20588) 
I (292249) esp_image: segment 2: paddr=000485c8 vaddr=40374000 size=07a50h ( 31312) 
I (292249) esp_image: segment 3: paddr=00050020 vaddr=42000020 size=92508h (599304) map
I (292339) esp_image: segment 4: paddr=000e2530 vaddr=4037ba50 size=0b684h ( 46724) 
I (292339) esp_image: segment 5: paddr=000edbbc vaddr=50000000 size=00024h (    36) 
I (292379) wifi station: [OTA] success: 1.4.0 -> 1.5.0 in 17 s. Rebooting...
I (292879) wifi:state: run -> init (0x0)
I (292889) wifi:pm stop, total sleep time: 64863907 us / 103147450 us

I (292889) wifi:<ba-del>idx:1, tid:0
I (292889) wifi:<ba-del>idx:0, tid:5
I (292889) wifi:new:<5,0>, old:<5,1>, ap:<255,255>, sta:<5,1>, prof:1, snd_ch_cfg:0x0
I (292899) wifi station: retry to connect to the AP
I (292949) wifi:flush txq
I (292949) wifi:stop sw txq
I (292949) wifi:lmac stop hw txq
␀�ESP-ROM:esp32s3-20210327
Build:Mar 27 2021
rst:0xc (RTC_SW_CPU_RST),boot:0x2b (SPI_FAST_FLASH_BOOT)
Saved PC:0x4037d308
SPIWP:0xee
mode:DIO, clock div:1
load:0x3fce2820,len:0x14f0
load:0x403c8700,len:0xda0
load:0x403cb700,len:0x2fa0
entry 0x403c8908
I (29) boot: ESP-IDF v6.0.1 2nd stage bootloader
I (29) boot: compile time Sep 29 2026 14:16:01
I (29) boot: Multicore bootloader
I (29) boot: chip revision: v0.2
I (32) boot: efuse block revision: v1.4
I (36) boot.esp32s3: Boot SPI Speed : 80MHz
I (40) boot.esp32s3: SPI Mode       : DIO
I (43) boot.esp32s3: SPI Flash Size : 2MB
I (47) boot: Enabling RNG early entropy source...
I (52) boot: Partition Table:
I (54) boot: ## Label            Usage          Type ST Offset   Length
I (61) boot:  0 nvs              WiFi data        01 02 00009000 00004000
I (67) boot:  1 otadata          OTA data         01 00 0000d000 00002000
I (74) boot:  2 ota_0            OTA app          00 10 00010000 000f0000
I (80) boot:  3 ota_1            OTA app          00 11 00100000 000f0000
I (87) boot: End of partition table
I (115) esp_image: segment 0: paddr=00010020 vaddr=3c0a0020 size=3352ch (210220) map
I (153) esp_image: segment 1: paddr=00043554 vaddr=3fc97100 size=0506ch ( 20588) load
I (158) esp_image: segment 2: paddr=000485c8 vaddr=40374000 size=07a50h ( 31312) load
I (165) esp_image: segment 3: paddr=00050020 vaddr=42000020 size=92508h (599304) map
I (273) esp_image: segment 4: paddr=000e2530 vaddr=4037ba50 size=0b684h ( 46724) load
I (283) esp_image: segment 5: paddr=000edbbc vaddr=50000000 size=00024h (    36) load
I (292) boot: Loaded app from partition at offset 0x10000
I (292) boot: Disabling RNG early entropy source...
I (302) cpu_start: Multicore app
I (311) cpu_start: GPIO 44 and 43 are used as console UART I/O pins
I (311) cpu_start: Pro cpu start user code
I (311) cpu_start: cpu freq: 160000000 Hz
I (313) app_init: Application information:
I (317) app_init: Project name:     station_WiFi
I (321) app_init: App version:      1.5.0
I (325) app_init: Compile time:     Sep 29 2026 14:17:34
I (330) app_init: ELF file SHA256:  486cd296d...
I (334) app_init: ESP-IDF:          v6.0.1
I (338) efuse_init: Min chip rev:     v0.0
I (342) efuse_init: Max chip rev:     v0.99 
I (346) efuse_init: Chip rev:         v0.2
I (350) heap_init: Initializing. RAM available for dynamic allocation:
I (356) heap_init: At 3FCA0460 len 000492B0 (292 KiB): RAM
I (361) heap_init: At 3FCE9710 len 00005724 (21 KiB): RAM
I (366) heap_init: At 3FCF0000 len 00008000 (32 KiB): DRAM
I (372) heap_init: At 600FE000 len 00001FE8 (7 KiB): RTCRAM
I (378) spi_flash: detected chip: mxic
I (380) spi_flash: flash io: dio
W (383) spi_flash: Detected size(16384k) larger than the size in the binary image header(2048k). Using the size in the binary image header.
I (396) sleep_gpio: Configure to isolate all GPIO pins in sleep state
I (402) sleep_gpio: Enable automatic switching of GPIO sleep configuration
I (409) main_task: Started on CPU0
I (429) main_task: Calling app_main()
I (449) temperature_sensor: Range [-10°C ~ 80°C], error < 1°C
I (449) wifi station: [CFG] migrating settings to v2 format...
I (569) wifi station: [CFG] migration done
I (579) pp: pp rom version: e7ae62f
I (579) net80211: net80211 rom version: e7ae62f
I (599) wifi:wifi driver task: 3fceed90, prio:23, stack:6656, core=0
I (599) wifi:wifi firmware version: b37c951
I (599) wifi:wifi certification version: v7.0
I (599) wifi:config NVS flash: enabled
I (599) wifi:config nano formatting: disabled
I (609) wifi:Init data frame dynamic rx buffer num: 32
I (609) wifi:Init static rx mgmt buffer num: 5
I (609) wifi:Init management short buffer num: 32
I (619) wifi:Init dynamic tx buffer num: 32
I (619) wifi:Init static tx FG buffer num: 2
I (629) wifi:Init static rx buffer size: 1600
I (629) wifi:Init static rx buffer num: 10
I (639) wifi:Init dynamic rx buffer num: 32
I (639) wifi_init: rx ba win: 6
I (639) wifi_init: accept mbox: 6
I (639) wifi_init: tcpip mbox: 32
I (649) wifi_init: udp mbox: 6
I (649) wifi_init: tcp mbox: 6
I (649) wifi_init: tcp tx win: 5760
I (659) wifi_init: tcp rx win: 5760
I (659) wifi_init: tcp mss: 1440
I (659) wifi_init: WiFi IRAM OP enabled
I (669) wifi_init: WiFi RX IRAM OP enabled
I (669) phy_init: phy_version 711,97bcf0a2,Aug 25 2025,19:04:10
W (679) phy_init: failed to load RF calibration data (0x1102), falling back to full calibration
I (719) phy_init: Saving new calibration data due to checksum failure or outdated calibration data, mode(2)
I (739) wifi:mode : sta (90:70:69:31:a6:8c)
I (739) wifi:enable tsf
I (739) wifi station: wifi initialized. Type 'connect' to join a network (interactive)
I (739) wifi station: [OTA] running partition: ota_0, version 1.5.0
W (739) wifi station: [OTA] new firmware, state PENDING_VERIFY - running self-check...
I (789) wifi station: [OTA] self-check passed, firmware marked VALID
```

**ota install 1.3.0 force** - *wi-fi interrupted before progress*

```text
I (214049) wifi station: [OTA] current version: 1.5.0 (partition ota_0)
I (214049) wifi station: [OTA] target partition: ota_1
I (214049) wifi station: [OTA] downloading: https://raw.githubusercontent.com/BohdanHorbanych/esp32-ota-files/main/firmware/v1.3.0/station_WiFi.bin
I (214079) wifi:<ba-add>idx:1 (ifx:0, 32:16:9d:25:9c:16), tid:0, ssn:1, winSize:64
I (214429) esp-x509-crt-bundle: Certificate validated
I (215219) esp_https_ota: Starting OTA...
I (215219) esp_https_ota: Writing to <ota_1> partition at offset 0x100000
I (215229) wifi station: [OTA] new version: 1.3.0
I (216779) wifi station: [OTA] progress: 10% (91136 / 907616 bytes)
I (218369) wifi station: [OTA] progress: 20% (185344 / 907616 bytes)
I (219849) wifi station: [OTA] progress: 30% (275456 / 907616 bytes)
I (221549) wifi station: [OTA] progress: 40% (365568 / 907616 bytes)
I (223159) wifi station: [OTA] progress: 50% (455680 / 907616 bytes)
I (224759) wifi station: [OTA] progress: 60% (545792 / 907616 bytes)
I (226299) wifi station: [OTA] progress: 70% (635904 / 907616 bytes)
I (227919) wifi station: [OTA] progress: 80% (730112 / 907616 bytes)
I (229439) wifi station: [OTA] progress: 90% (820224 / 907616 bytes)
I (230769) wifi station: [OTA] progress: 100% (907616 / 907616 bytes)
I (230769) esp_image: segment 0: paddr=00100020 vaddr=3c0a0020 size=3341ch (209948) map
I (230799) esp_image: segment 1: paddr=00133444 vaddr=3fc97100 size=0506ch ( 20588) 
I (230799) esp_image: segment 2: paddr=001384b8 vaddr=40374000 size=07b60h ( 31584) 
I (230809) esp_image: segment 3: paddr=00140020 vaddr=42000020 size=92368h (598888) map
I (230889) esp_image: segment 4: paddr=001d2390 vaddr=4037bb60 size=0b574h ( 46452) 
I (230899) esp_image: segment 5: paddr=001dd90c vaddr=50000000 size=00024h (    36) 
I (230899) esp_image: segment 0: paddr=00100020 vaddr=3c0a0020 size=3341ch (209948) map
I (230929) esp_image: segment 1: paddr=00133444 vaddr=3fc97100 size=0506ch ( 20588) 
I (230929) esp_image: segment 2: paddr=001384b8 vaddr=40374000 size=07b60h ( 31584) 
I (230939) esp_image: segment 3: paddr=00140020 vaddr=42000020 size=92368h (598888) map
I (231019) esp_image: segment 4: paddr=001d2390 vaddr=4037bb60 size=0b574h ( 46452) 
I (231029) esp_image: segment 5: paddr=001dd90c vaddr=50000000 size=00024h (    36) 
I (231069) wifi station: [OTA] success: 1.5.0 -> 1.3.0 in 15 s. Rebooting...
I (231569) wifi:state: run -> init (0x0)
I (231579) wifi:pm stop, total sleep time: 20324800 us / 39122398 us

I (231579) wifi:<ba-del>idx:1, tid:0
I (231579) wifi:<ba-del>idx:0, tid:5
I (231579) wifi:new:<5,0>, old:<5,1>, ap:<255,255>, sta:<5,1>, prof:1, snd_ch_cfg:0x0
I (231589) wifi station: retry to connect to the AP
I (231629) wifi:flush txq
I (231629) wifi:stop sw txq
I (231629) wifi:lmac stop hw txq
␀�ESP-ROM:esp32s3-20210327
Build:Mar 27 2021
rst:0xc (RTC_SW_CPU_RST),boot:0x2b (SPI_FAST_FLASH_BOOT)
Saved PC:0x4037d308
SPIWP:0xee
mode:DIO, clock div:1
load:0x3fce2820,len:0x14f0
load:0x403c8700,len:0xda0
load:0x403cb700,len:0x2fa0
entry 0x403c8908
I (29) boot: ESP-IDF v6.0.1 2nd stage bootloader
I (29) boot: compile time Sep 29 2026 14:16:01
I (29) boot: Multicore bootloader
I (29) boot: chip revision: v0.2
I (32) boot: efuse block revision: v1.4
I (36) boot.esp32s3: Boot SPI Speed : 80MHz
I (40) boot.esp32s3: SPI Mode       : DIO
I (43) boot.esp32s3: SPI Flash Size : 2MB
I (47) boot: Enabling RNG early entropy source...
I (52) boot: Partition Table:
I (54) boot: ## Label            Usage          Type ST Offset   Length
I (61) boot:  0 nvs              WiFi data        01 02 00009000 00004000
I (67) boot:  1 otadata          OTA data         01 00 0000d000 00002000
I (74) boot:  2 ota_0            OTA app          00 10 00010000 000f0000
I (80) boot:  3 ota_1            OTA app          00 11 00100000 000f0000
I (87) boot: End of partition table
I (115) esp_image: segment 0: paddr=00100020 vaddr=3c0a0020 size=3341ch (209948) map
I (153) esp_image: segment 1: paddr=00133444 vaddr=3fc97100 size=0506ch ( 20588) load
I (158) esp_image: segment 2: paddr=001384b8 vaddr=40374000 size=07b60h ( 31584) load
I (165) esp_image: segment 3: paddr=00140020 vaddr=42000020 size=92368h (598888) map
I (273) esp_image: segment 4: paddr=001d2390 vaddr=4037bb60 size=0b574h ( 46452) load
I (283) esp_image: segment 5: paddr=001dd90c vaddr=50000000 size=00024h (    36) load
I (292) boot: Loaded app from partition at offset 0x100000
I (292) boot: Disabling RNG early entropy source...
I (302) cpu_start: Multicore app
I (311) cpu_start: GPIO 44 and 43 are used as console UART I/O pins
I (311) cpu_start: Pro cpu start user code
I (311) cpu_start: cpu freq: 160000000 Hz
I (313) app_init: Application information:
I (317) app_init: Project name:     station_WiFi
I (321) app_init: App version:      1.3.0
I (325) app_init: Compile time:     Sep 29 2026 14:15:53
I (330) app_init: ELF file SHA256:  7fc2e6354...
I (334) app_init: ESP-IDF:          v6.0.1
I (338) efuse_init: Min chip rev:     v0.0
I (342) efuse_init: Max chip rev:     v0.99 
I (346) efuse_init: Chip rev:         v0.2
I (350) heap_init: Initializing. RAM available for dynamic allocation:
I (356) heap_init: At 3FCA0460 len 000492B0 (292 KiB): RAM
I (361) heap_init: At 3FCE9710 len 00005724 (21 KiB): RAM
I (366) heap_init: At 3FCF0000 len 00008000 (32 KiB): DRAM
I (372) heap_init: At 600FE000 len 00001FE8 (7 KiB): RTCRAM
I (378) spi_flash: detected chip: mxic
I (380) spi_flash: flash io: dio
W (383) spi_flash: Detected size(16384k) larger than the size in the binary image header(2048k). Using the size in the binary image header.
I (396) sleep_gpio: Configure to isolate all GPIO pins in sleep state
I (402) sleep_gpio: Enable automatic switching of GPIO sleep configuration
I (409) main_task: Started on CPU0
I (429) main_task: Calling app_main()
I (449) temperature_sensor: Range [-10°C ~ 80°C], error < 1°C
I (449) pp: pp rom version: e7ae62f
I (459) net80211: net80211 rom version: e7ae62f
I (469) wifi:wifi driver task: 3fced4cc, prio:23, stack:6656, core=0
I (469) wifi:wifi firmware version: b37c951
I (469) wifi:wifi certification version: v7.0
I (479) wifi:config NVS flash: enabled
I (479) wifi:config nano formatting: disabled
I (479) wifi:Init data frame dynamic rx buffer num: 32
I (479) wifi:Init static rx mgmt buffer num: 5
I (489) wifi:Init management short buffer num: 32
I (489) wifi:Init dynamic tx buffer num: 32
I (499) wifi:Init static tx FG buffer num: 2
I (499) wifi:Init static rx buffer size: 1600
I (499) wifi:Init static rx buffer num: 10
I (509) wifi:Init dynamic rx buffer num: 32
I (509) wifi_init: rx ba win: 6
I (519) wifi_init: accept mbox: 6
I (519) wifi_init: tcpip mbox: 32
I (519) wifi_init: udp mbox: 6
I (519) wifi_init: tcp mbox: 6
I (529) wifi_init: tcp tx win: 5760
I (529) wifi_init: tcp rx win: 5760
I (529) wifi_init: tcp mss: 1440
I (539) wifi_init: WiFi IRAM OP enabled
I (539) wifi_init: WiFi RX IRAM OP enabled
I (539) phy_init: phy_version 711,97bcf0a2,Aug 25 2025,19:04:10
I (589) wifi:mode : sta (90:70:69:31:a6:8c)
I (599) wifi:enable tsf
I (599) wifi station: wifi initialized. Type 'connect' to join a network (interactive)
I (599) wifi station: [OTA] running partition: ota_1, version 1.3.0
W (599) wifi station: [OTA] new firmware, state PENDING_VERIFY - running self-check...
I (649) wifi station: [OTA] self-check passed, firmware marked VALID
```

**ota install 1.4.0** - *wi-fi interrupted before progress*

```text
I (93379) wifi station: [OTA] current version: 1.3.0 (partition ota_1)
I (93379) wifi station: [OTA] target partition: ota_0
I (93379) wifi station: [OTA] downloading: https://raw.githubusercontent.com/BohdanHorbanych/esp32-ota-files/main/firmware/v1.4.0/station_WiFi.bin
I (93409) wifi:<ba-add>idx:1 (ifx:0, 32:16:9d:25:b8:9e), tid:0, ssn:1, winSize:64
I (93789) esp-x509-crt-bundle: Certificate validated
I (94679) esp_https_ota: Starting OTA...
I (94679) esp_https_ota: Writing to <ota_0> partition at offset 0x10000
I (94689) wifi station: [OTA] new version: 1.4.0
I (96409) wifi station: [OTA] progress: 10% (91136 / 907872 bytes)
I (98249) wifi station: [OTA] progress: 20% (185344 / 907872 bytes)
I (99749) wifi station: [OTA] progress: 30% (275456 / 907872 bytes)
I (101409) wifi station: [OTA] progress: 40% (365568 / 907872 bytes)
I (102849) wifi station: [OTA] progress: 50% (455680 / 907872 bytes)
I (104469) wifi station: [OTA] progress: 60% (545792 / 907872 bytes)
I (105949) wifi station: [OTA] progress: 70% (635904 / 907872 bytes)
I (107549) wifi station: [OTA] progress: 80% (730112 / 907872 bytes)
I (109079) wifi station: [OTA] progress: 90% (820224 / 907872 bytes)
I (110499) wifi station: [OTA] progress: 100% (907872 / 907872 bytes)
I (110499) esp_image: segment 0: paddr=00010020 vaddr=3c0a0020 size=3349ch (210076) map
I (110529) esp_image: segment 1: paddr=000434c4 vaddr=3fc97100 size=0506ch ( 20588) 
I (110539) esp_image: segment 2: paddr=00048538 vaddr=40374000 size=07ae0h ( 31456) 
I (110539) esp_image: segment 3: paddr=00050020 vaddr=42000020 size=923ech (599020) map
I (110619) esp_image: segment 4: paddr=000e2414 vaddr=4037bae0 size=0b5f4h ( 46580) 
I (110629) esp_image: segment 5: paddr=000eda10 vaddr=50000000 size=00024h (    36) 
I (110629) esp_image: segment 0: paddr=00010020 vaddr=3c0a0020 size=3349ch (210076) map
I (110659) esp_image: segment 1: paddr=000434c4 vaddr=3fc97100 size=0506ch ( 20588) 
I (110669) esp_image: segment 2: paddr=00048538 vaddr=40374000 size=07ae0h ( 31456) 
I (110669) esp_image: segment 3: paddr=00050020 vaddr=42000020 size=923ech (599020) map
I (110759) esp_image: segment 4: paddr=000e2414 vaddr=4037bae0 size=0b5f4h ( 46580) 
I (110759) esp_image: segment 5: paddr=000eda10 vaddr=50000000 size=00024h (    36) 
I (110799) wifi station: [OTA] success: 1.3.0 -> 1.4.0 in 16 s. Rebooting...
I (111299) wifi:state: run -> init (0x0)
I (111309) wifi:pm stop, total sleep time: 19209776 us / 39815589 us

I (111309) wifi:<ba-del>idx:1, tid:0
I (111309) wifi:<ba-del>idx:0, tid:5
I (111309) wifi:new:<5,0>, old:<5,1>, ap:<255,255>, sta:<5,1>, prof:1, snd_ch_cfg:0x0
I (111319) wifi station: retry to connect to the AP
I (111349) wifi:flush txq
I (111349) wifi:stop sw txq
I (111349) wifi:lmac stop hw txq
␀�ESP-ROM:esp32s3-20210327
Build:Mar 27 2021
rst:0xc (RTC_SW_CPU_RST),boot:0x2b (SPI_FAST_FLASH_BOOT)
Saved PC:0x4037d308
SPIWP:0xee
mode:DIO, clock div:1
load:0x3fce2820,len:0x14f0
load:0x403c8700,len:0xda0
load:0x403cb700,len:0x2fa0
entry 0x403c8908
I (29) boot: ESP-IDF v6.0.1 2nd stage bootloader
I (29) boot: compile time Sep 29 2026 14:16:01
I (29) boot: Multicore bootloader
I (29) boot: chip revision: v0.2
I (32) boot: efuse block revision: v1.4
I (36) boot.esp32s3: Boot SPI Speed : 80MHz
I (40) boot.esp32s3: SPI Mode       : DIO
I (43) boot.esp32s3: SPI Flash Size : 2MB
I (47) boot: Enabling RNG early entropy source...
I (52) boot: Partition Table:
I (54) boot: ## Label            Usage          Type ST Offset   Length
I (61) boot:  0 nvs              WiFi data        01 02 00009000 00004000
I (67) boot:  1 otadata          OTA data         01 00 0000d000 00002000
I (74) boot:  2 ota_0            OTA app          00 10 00010000 000f0000
I (80) boot:  3 ota_1            OTA app          00 11 00100000 000f0000
I (87) boot: End of partition table
I (115) esp_image: segment 0: paddr=00010020 vaddr=3c0a0020 size=3349ch (210076) map
I (153) esp_image: segment 1: paddr=000434c4 vaddr=3fc97100 size=0506ch ( 20588) load
I (158) esp_image: segment 2: paddr=00048538 vaddr=40374000 size=07ae0h ( 31456) load
I (165) esp_image: segment 3: paddr=00050020 vaddr=42000020 size=923ech (599020) map
I (273) esp_image: segment 4: paddr=000e2414 vaddr=4037bae0 size=0b5f4h ( 46580) load
I (283) esp_image: segment 5: paddr=000eda10 vaddr=50000000 size=00024h (    36) load
I (292) boot: Loaded app from partition at offset 0x10000
I (292) boot: Disabling RNG early entropy source...
I (302) cpu_start: Multicore app
I (311) cpu_start: GPIO 44 and 43 are used as console UART I/O pins
I (311) cpu_start: Pro cpu start user code
I (311) cpu_start: cpu freq: 160000000 Hz
I (313) app_init: Application information:
I (317) app_init: Project name:     station_WiFi
I (321) app_init: App version:      1.4.0
I (325) app_init: Compile time:     Sep 29 2026 14:16:45
I (330) app_init: ELF file SHA256:  f7a307237...
I (334) app_init: ESP-IDF:          v6.0.1
I (338) efuse_init: Min chip rev:     v0.0
I (342) efuse_init: Max chip rev:     v0.99 
I (346) efuse_init: Chip rev:         v0.2
I (350) heap_init: Initializing. RAM available for dynamic allocation:
I (356) heap_init: At 3FCA0460 len 000492B0 (292 KiB): RAM
I (361) heap_init: At 3FCE9710 len 00005724 (21 KiB): RAM
I (366) heap_init: At 3FCF0000 len 00008000 (32 KiB): DRAM
I (372) heap_init: At 600FE000 len 00001FE8 (7 KiB): RTCRAM
I (378) spi_flash: detected chip: mxic
I (380) spi_flash: flash io: dio
W (383) spi_flash: Detected size(16384k) larger than the size in the binary image header(2048k). Using the size in the binary image header.
I (396) sleep_gpio: Configure to isolate all GPIO pins in sleep state
I (402) sleep_gpio: Enable automatic switching of GPIO sleep configuration
I (409) main_task: Started on CPU0
I (429) main_task: Calling app_main()
I (449) temperature_sensor: Range [-10°C ~ 80°C], error < 1°C
I (449) pp: pp rom version: e7ae62f
I (459) net80211: net80211 rom version: e7ae62f
I (469) wifi:wifi driver task: 3fced4cc, prio:23, stack:6656, core=0
I (469) wifi:wifi firmware version: b37c951
I (469) wifi:wifi certification version: v7.0
I (479) wifi:config NVS flash: enabled
I (479) wifi:config nano formatting: disabled
I (479) wifi:Init data frame dynamic rx buffer num: 32
I (479) wifi:Init static rx mgmt buffer num: 5
I (489) wifi:Init management short buffer num: 32
I (489) wifi:Init dynamic tx buffer num: 32
I (499) wifi:Init static tx FG buffer num: 2
I (499) wifi:Init static rx buffer size: 1600
I (499) wifi:Init static rx buffer num: 10
I (509) wifi:Init dynamic rx buffer num: 32
I (509) wifi_init: rx ba win: 6
I (519) wifi_init: accept mbox: 6
I (519) wifi_init: tcpip mbox: 32
I (519) wifi_init: udp mbox: 6
I (519) wifi_init: tcp mbox: 6
I (529) wifi_init: tcp tx win: 5760
I (529) wifi_init: tcp rx win: 5760
I (529) wifi_init: tcp mss: 1440
I (539) wifi_init: WiFi IRAM OP enabled
I (539) wifi_init: WiFi RX IRAM OP enabled
I (539) phy_init: phy_version 711,97bcf0a2,Aug 25 2025,19:04:10
I (599) wifi:mode : sta (90:70:69:31:a6:8c)
I (599) wifi:enable tsf
I (599) wifi station: wifi initialized. Type 'connect' to join a network (interactive)
I (599) wifi station: [OTA] running partition: ota_0, version 1.4.0
W (609) wifi station: [OTA] new firmware, state PENDING_VERIFY - running self-check...
I (649) wifi station: [OTA] self-check passed, firmware marked VALID
```