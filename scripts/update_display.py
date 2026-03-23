import socket
import struct
import time
import sys
import threading
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, '/home/skylar/picontrol/drivers')
import st7735_driver as lcd

UDP_PORT = 25000
latest_val = None
val_lock = threading.Lock()


def make_screen(sine_val: float, duty: float) -> Image.Image:
    img = Image.new('RGB', (lcd.WIDTH, lcd.HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    draw.rectangle((0, 0, lcd.WIDTH, 20), fill=(0, 80, 160))
    draw.text((4, 4), "SINE OUTPUT", font=font, fill=(200, 230, 255))

    draw.text((10, 30), f"{sine_val:+.4f}", font=font, fill=(255, 255, 100))

    draw.text((10, 46), f"duty: {duty:.1f}%", font=font, fill=(180, 220, 255))

    bar_w = int((duty / 100.0) * (lcd.WIDTH - 20))
    draw.rectangle((10, 68, lcd.WIDTH - 10, 84), outline=(60, 60, 60))
    if bar_w > 0:
        draw.rectangle((10, 68, 10 + bar_w, 84), fill=(0, 200, 80))

    draw.rectangle((0, lcd.HEIGHT - 18, lcd.WIDTH, lcd.HEIGHT), fill=(20, 20, 20))
    draw.text((4, lcd.HEIGHT - 14), "PiControlTest", font=font, fill=(100, 100, 120))

    return img

def udp_listener():
    """Continuously drain UDP socket and update latest_val."""
    global latest_val
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', UDP_PORT))
    sock.setblocking(False)
    print(f"Listening on UDP port {UDP_PORT}...")

    while True:
        try:
            while True:
                data, _ = sock.recvfrom(1024)
                val = struct.unpack('d', data[:8])[0]
                with val_lock:
                    latest_val = val
        except BlockingIOError:
            pass
        time.sleep(0.01)


def main():
    listener = threading.Thread(target=udp_listener, daemon=True)
    listener.start()

    print("Main loop started")
    try:
        while True:
            with val_lock:
                val = latest_val

            if val is not None:
                val = max(0.0, min(100.0, val))
                sine_val = (val - 50.0) / 50.0  # convert 0-100 back to -1..+1
                img = make_screen(sine_val, val)
                lcd.show(img)

            else:
                time.sleep(0.05)

    finally:
        lcd.cleanup()

if __name__ == '__main__':
    main()
