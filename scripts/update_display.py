import sys
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, '/home/skylar/picontrol/drivers')
import st7735_driver as lcd

def make_screen(value: float) -> Image.Image:
    img = Image.new('RGB', (lcd.WIDTH, lcd.HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    # header
    draw.rectangle((0, 0, lcd.WIDTH, 20), fill=(0, 80, 160))
    draw.text((4, 4), "SINE OUTPUT", font=font, fill=(200, 230, 255))

    # numeric value
    draw.text((10, 30), f"{value:+.4f}", font=font, fill=(255, 255, 100))

    # duty cycle
    duty = 50 + value * 50
    draw.text((10, 46), f"duty: {duty:.1f}%", font=font, fill=(180, 220, 255))

    # bar graph
    bar_w = int((value + 1) / 2 * (lcd.WIDTH - 20))
    draw.rectangle((10, 68, lcd.WIDTH - 10, 84), outline=(60, 60, 60))
    if bar_w > 0:
        draw.rectangle((10, 68, 10 + bar_w, 84), fill=(0, 200, 80))

    # footer
    draw.rectangle((0, lcd.HEIGHT - 18, lcd.WIDTH, lcd.HEIGHT), fill=(20, 20, 20))
    draw.text((4, lcd.HEIGHT - 14), "PiControlTest", font=font, fill=(100, 100, 120))

    return img

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: update_display.py <value>")
        sys.exit(1)

    value = float(sys.argv[1])
    value = max(-1.0, min(1.0, value))  # clamp to sine range

    try:
        img = make_screen(value)
        lcd.show(img)
    finally:
        lcd.cleanup()
