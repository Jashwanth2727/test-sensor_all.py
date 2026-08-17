#!/usr/bin/env python3
import time
from rpi_ws281x import PixelStrip, ws

GREEN = (0 << 16) | (51 << 8) | 0

print("init GPIO 18...")
s18 = PixelStrip(6, 18, 800000, 5, False, 255, 0, ws.WS2811_STRIP_GRB)
s18.begin()
print("init GPIO 12...")
s12 = PixelStrip(6, 12, 800000, 6, False, 255, 0, ws.WS2811_STRIP_GRB)
s12.begin()
print("ready")

def set_all(color):
    for s in (s18, s12):
        for i in range(s.numPixels()):
            s.setPixelColor(i, color)
        s.show()
        time.sleep(0.01)

set_all(0)
time.sleep(1)
print("blinking — Ctrl+C to stop")

try:
    while True:
        print("ON")
        set_all(GREEN)
        time.sleep(2)
        print("OFF")
        set_all(0)
        time.sleep(2)
except KeyboardInterrupt:
    set_all(0)
    print("Off.")
