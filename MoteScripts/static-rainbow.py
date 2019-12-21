#!/usr/bin/env python
#From https://github.com/pimoroni/mote

import time
from colorsys import hsv_to_rgb

import motephat as mote

mote.configure_channel(1, 16, False)
mote.configure_channel(2, 16, False)
mote.configure_channel(3, 16, False)
mote.configure_channel(4, 16, False)

mote.set_clear_on_exit(False)

h = 1

for channel in range(1,5):
    pixel_count = mote.get_pixel_count(channel)
    for pixel in range(pixel_count):
        hue = (h + ((channel-1) * pixel_count * 5) + (pixel * 5)) % 360
        r, g, b = [int(c * 255) for c in hsv_to_rgb(hue/360.0, 1.0, 1.0)]
        mote.set_pixel(channel, pixel, r, g, b)
mote.show()
