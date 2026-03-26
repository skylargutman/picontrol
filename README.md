# picontrol

Raspberry Pi 4B control system for FAU Senior Design Project:  
**Parametric Retrofit of Lab Equipment for Remote Control**  
*Author: Skylar Gutman — March 2026*

---

## Overview

This repository contains the embedded software running on the Raspberry Pi 4B
(`PiControlTest.local`) that interfaces with a MATLAB/Simulink control model,
drives hardware outputs, displays live system state, and publishes telemetry
to a cloud MQTT broker.

---

## Repository Structure
```
picontrol/
├── drivers/
│   ├── st7735_driver.py       # symlink → ST7735_PI4/st7735_driver.py
│   └── ST7735_PI4/            # submodule: ST7735R display driver + docs
├── models/                    # Simulink Coder deployed executables (not tracked)
├── scripts/
│   ├── update_display.py      # display daemon: receives UDP, renders to LCD
│   ├── start.sh               # start pigpiod, display daemon, and model
│   └── stop.sh                # cleanly stop all running components
└── README.md
```

---

## Hardware

| Component | Details |
|---|---|
| Raspberry Pi 4B | Hostname: PiControlTest.local |
| ST7735R LCD | 1.8" 128×160 SPI display, CS on GPIO 23, DC on GPIO 24, RST on GPIO 25 |
| PWM output | GPIO 18 (physical pin 12) — PWM0, 1kHz |
| Motor driver | BTS7960 IBT-2 H-bridge, 24V supply |

---

## Dependencies
```bash
sudo apt install pigpio mosquitto-clients -y
sudo pip3 install lgpio numpy pillow --break-system-packages
```

pigpiod must be running before the Simulink model starts:
```bash
sudo systemctl enable pigpiod
sudo systemctl start pigpiod
```

---

## Model B — Sine Wave PWM + Telemetry

The current deployed model (`model_b.slx`) does the following:

- Generates a 1 Hz sine wave (amplitude 50, bias 50 → range 0–100)
- Drives GPIO 18 PWM at 1kHz with duty cycle following the sine wave
- Publishes JSON telemetry to MQTT broker at 10Hz via UDP to display daemon
- Displays live sine value and duty cycle bar graph on ST7735R LCD

### Data flow
```
Simulink model_b.elf
    ├── PWM block → GPIO 18 (pin 12)
    ├── UDP Send → update_display.py → ST7735R LCD
    └── MQTT Publish → sciencelabtoyou.com:1885
                            topic: picontrol/model_b/sine
                            payload: {"t":%f,"cart":%d,"pendulum":%d,"pwm":%+09.4f}
```

### MQTT payload format
```json
{"t":123.456,"cart":0,"pendulum":0,"pwm":+075.2384}
```

| Field | Type | Description |
|---|---|---|
| t | float | Simulink clock time (seconds) |
| cart | int | Cart encoder position (stub: 0) |
| pendulum | int | Pendulum encoder position (stub: 0) |
| pwm | float | Motor PWM duty cycle (0–100) |

---

## Running
```bash
~/picontrol/scripts/start.sh    # start everything
~/picontrol/scripts/stop.sh     # stop everything
```

---

## Display Driver

The ST7735R driver is maintained as a Git submodule in `drivers/ST7735_PI4/`.
See that repo for full wiring diagrams, troubleshooting, and driver documentation.

Key characteristics:
- Bit-bang SPI for commands (lgpio GPIO bit-bang)
- lgpio spi_write for pixel data burst
- Idempotent `init()` — safe to call multiple times
- `show()` auto-initialises on first call
- ~2 second full-screen refresh (Python bit-bang limitation)

---

## On the Horizon

- Connect cart and pendulum encoder data from ESP32/PCI-1711 pipeline
- Replace MQTT payload stubs with real encoder positions
- Django + MySQL telemetry logging and waveform reconstruction on Oracle Cloud
- Custom PCB revision after component set is finalised
- C display driver for faster refresh rate
