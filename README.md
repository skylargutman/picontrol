# picontrol

Raspberry Pi 4B control system for FAU Senior Design Project:
**Parametric Retrofit of Lab Equipment for Remote Control**

## Structure

- `drivers/` — hardware drivers; ST7735R display driver documented in [ST7735_PI4](drivers/ST7735_PI4/)
- `models/` — Simulink Coder deployed executables
- `scripts/` — runtime scripts called by Simulink models (e.g. display update)

## Hardware

- Raspberry Pi 4B (`PiControlTest.local`)
- ST7735R 1.8" 128×160 SPI display
- GPIO 18 (pin 12) — PWM0 output

## Dependencies
```bash
sudo pip3 install lgpio pillow --break-system-packages
```
