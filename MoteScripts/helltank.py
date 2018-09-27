#!/usr/bin/env python
#Based on work from https://github.com/pimoroni/mote

import math
import time
from colorsys import hsv_to_rgb

import motephat

# The hue wheel is 360 degrees around, with;
# 0 = Red
# 40ish = Orange
# 120 = Green
# 180 = Teal
# 240 = Blue
# 300 = Purple

hue_start = 0
hue_range = 30
speed = 0.25

motephat.configure_channel(1, 16, False)
motephat.configure_channel(2, 16, False)
motephat.configure_channel(3, 16, False)
motephat.configure_channel(4, 16, False)

try:
    while True:
        phase = 0
        for channel in [1,2,3,4]:
            for pixel in range(motephat.get_pixel_count(channel)):
                h = (time.time() * speed) + (phase / 10.0)
                h = math.sin(h) * (hue_range/2)
                hue = hue_start + (hue_range/2) + h
                hue %= 360

                r, g, b = [int(c * 255) for c in hsv_to_rgb(hue/360.0, 1.0, 1.0)]
                motephat.set_pixel(channel, pixel, r, g, b)

                phase += 1

        motephat.show()
        time.sleep(0.01)

except KeyboardInterrupt:
    motephat.clear()
    motephat.show()
