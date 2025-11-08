# WAPE32 — Wi‑Fi Attacks Framework for ESP32

WAPE32 is an extensible framework for implementing and running Wi‑Fi reconnaissance and attack techniques from an ESP32 microcontroller. The project provides common low‑level and helper functionality used by Wi‑Fi tools (packet capture, injection, parsing, formatting, and attack orchestration) so new attacks and utilities can be developed quickly on low‑cost hardware.

Note: WAPE32 is NOT a password cracking tool. The ESP32 is used for capture and targeted attacks; heavy cryptographic cracking must be performed on proper hardware off‑device.

Contents
- Features
- Supported hardware
- Quickstart (build, flash, run)
- Usage (web UI and network)
- Output formats and interoperability
- Extending the framework
- Security, ethics, and license
- Further reading and acknowledgements

## Features
- PMKID capture (802.11i)
- WPA/WPA2 handshake capture and parsing
- Passive handshake sniffing
- Deauthentication attacks (multiple methods)
- Denial of Service (DoS) attack utilities
- Packet capture export in PCAP format
- Handshake export in HCCAPX format (Hashcat compatible)
- Modular, easily extensible attack framework
- Built‑in ESP32_tools web configuration interface for on‑device control
- Prebuilt binaries available for quick flashing (see build/)

## Supported hardware
Tested primarily on:
- ESP32‑DEVKITC‑32E
Compatible with ESP32 modules based on ESP32‑WROOM‑32.

Other ESP32 variants may work but functionality depends on Wi‑Fi driver support available in the ESP‑IDF version used.

## Quickstart

Prerequisites
- ESP32 toolchain and ESP‑IDF (recommended) — see Espressif docs: https://docs.espressif.com
- Python3 and esptool.py (if flashing prebuilt binaries)
- USB cable and access to the device serial port

Build and flash (ESP‑IDF)
1. Clone and set up ESP‑IDF (follow Espressif instructions).
2. Configure the project:
   - idf.py menuconfig
3. Build and flash:
   ```
   idf.py build
   idf.py -p /dev/ttyUSB0 flash
   ```
   Replace /dev/ttyUSB0 with your serial device.

Flash prebuilt binaries (no ESP‑IDF)
- Prebuilt images are available in `build/`. Use esptool.py:
  ```
  esptool.py -p /dev/ttyUSB0 -b 115200 --after hard_reset write_flash \
    --flash_mode dio --flash_freq 40m --flash_size detect \
    0x8000 build/partition_table/partition-table.bin \
    0x1000 build/bootloader/bootloader.bin \
    0x10000 build/<project>.bin
  ```
  Adjust paths and filenames for the build artifacts present in the `build/` directory.

On Windows, you can use Espressif's Flash Download Tool.

## Running and usage

1. Power the ESP32 after flashing.
2. The device starts the ESP32_tools access point automatically after boot.

Default AP (configurable in menuconfig or web UI)
- SSID: `ESP32_tools`
- Password: `xnBD2k25`
- Web UI IP: `192.168.4.1`

3. Connect a phone or laptop to the ESP32_tools AP and open a browser to:
   ```
   http://192.168.4.1
   ```
   The web UI allows:
   - Selecting target SSIDs / BSSIDs and channels
   - Starting/stopping sniffing and attacks (deauth, DoS, etc.)
   - Viewing and downloading captured PCAP and HCCAPX files
   - Configuring attack parameters and saving settings

See the web UI for live status and logs.

## Output formats and interoperability
- PCAP: Capture standard 802.11 frames in PCAP format for analysis in Wireshark or other tools.
- HCCAPX: Handshakes can be exported to HCCAPX format so Hashcat or other cracking tools can be used off‑device.
- Logs and CSV: Basic logs and metadata for captured sessions.

Limitations
- The ESP32 is not suitable for brute force or GPU cracking. Use HCCAPX exports with Hashcat on appropriate hardware.
- Some capture/injection features depend on the ESP‑IDF Wi‑Fi driver and may vary between chip revisions and SDK versions.

## Extending the framework
WAPE32 is designed to be modular:
- Attack modules are implemented as separate components that hook into the common capture/injection API.
- New modules should:
  - Use the provided capture and injection abstractions
  - Register UI endpoints (if applicable) for web control
  - Produce/consume standard output formats (PCAP, HCCAPX) when relevant

When contributing modules, follow the existing code structure and add documentation and tests where possible.

## Security, Ethics, and Responsible Use
WAPE32 demonstrates weaknesses in 802.11 and is intended for:
- Research and education
- Network auditing where explicit permission has been granted
- Testing and defending your own networks

Do NOT use WAPE32 on networks you do not own or have explicit authorization to test. Unauthorized interception, interference, or disruption of networks is illegal in many jurisdictions.

If you discover vulnerabilities in third‑party systems, follow responsible disclosure practices.

## License
This project is released under the MIT License. See the LICENSE file for full terms.

Being open source does not remove responsibility: please use this project ethically and share improvements back to the community.

## Further reading
- Academic paper about this project (PDF): https://excel.fit.vutbr.cz/submissions/2021/048/48.pdf
- Related projects and references:
  - GANESH-ICMC/esp32-deauther — https://github.com/GANESH-ICMC/esp32-deauther
  - SpacehuhnTech/esp8266_deauther — https://github.com/SpacehuhnTech/esp8266_deauther
  - justcallmekoko/ESP32Marauder — https://github.com/justcallmekoko/ESP32Marauder
  - Jeija/esp32free80211 — https://github.com/Jeija/esp32free80211

## Contributing
Contributions, issues and feature requests are welcome. Please open issues for bugs or enhancements and submit pull requests for fixes and new modules. Include test steps and describe the environment (ESP32 variant, ESP‑IDF version) used for development and testing.

## Contact / Maintainer
Maintainer: Cypher-Z
(Use GitHub issues or pull requests for project communications.)

Acknowledgements
Thanks to the community projects and researchers whose work provided inspiration and reference implementations for this project.
