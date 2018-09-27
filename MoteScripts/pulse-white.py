#!/usr/bin/env python
#From https://github.com/pimoroni/mote

import colorsys
import math
import time

import motephat


motephat.set_brightness(1)

offset = 0

while True:
    br = (math.sin(time.time()) + 1) / 2
    br *= 255.0
    br = int(br)

    for channel in range(1,5):
        for pixel in range(16):
            motephat.set_pixel(channel, pixel, br, br, br)

    motephat.show()
