# Prayer Time Music Muter

## Overview

The **Prayer Time Music Muter** is an IoT project designed to address the issue of music being played during Islamic prayer times at NYU Abu Dhabi's dining hall (D2). This system automatically mutes the music during prayer times, promoting inclusivity and respect for cultural and religious practices.

---

## Features

- **Automated Volume Control**: Mutes music during prayer times and restores it after five minutes.
- **Python-Based Solution**: Utilizes a script to compare the current time with predefined prayer times.
- **High-Quality Audio Handling**: Integrates **Raspberry Pi 3 Model B** with **HiFiBerry DAC+ ADC** for seamless audio input/output.
- **Flexible Networking**: Operates with an independent router setup to bypass network restrictions.

---

## Hardware Requirements

- Raspberry Pi 3 Model B
- HiFiBerry DAC+ ADC
- HDMI Cable
- Keyboard and Mouse
- Power Cable
- RCA Cables and AUX Cable
- Router for independent network setup

---

## Software Requirements

- Raspberry Pi OS (32-bit)
- Python 3.x
- `praytimes` Python library
- Audio control via `amixer`

---

## Steps to Execute the Code

### 1. Hardware Setup
1. Solder an audio jack onto the HiFiBerry DAC+ ADC for testing purposes.
2. Connect the HiFiBerry DAC+ ADC to the Raspberry Pi via the 40-pin GPIO header.
3. Secure the setup inside a custom-designed casing.

### 2. Router Configuration
1. Configure a separate router to connect the Raspberry Pi to the internet.
2. Use Eduroam as the main network source to simplify the setup process.

### 3. Software Installation
1. Install Raspberry Pi OS onto a microSD card using the Raspberry Pi Imager.
2. Boot the Raspberry Pi and ensure it is connected to the internet.
3. Open a terminal and update the package manager:
   ```bash
   sudo apt-get update

### 4. Run the py file
Go to terminal

Install the praytimes library by running the command “pip3 install praytimes”

Create a new Python file by running the command “mute_prayer_time.py”

Run the script by entering python3 mute_prayer_time.py.

The script will run in the background, muting the sound at the specified prayer times and unmuting it after 5 minutes.
