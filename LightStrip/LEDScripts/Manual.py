#!/usr/bin/env python
from sys import argv
from rpi_ws281x import *

# LED strip configuration:
LED_COUNT      = 89     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

if len(argv) != 4: #[Program] [R1] [G1] [B1], starts at 0
    print ("Wrong number of Variables")
    quit()

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ,LED_DMA,LED_INVERT,LED_BRIGHTNESS,LED_CHANNEL)
strip.begin()

for pixel in range(0,LED_COUNT):
    strip.setPixelColor(pixel,Color(int(argv[1]), int(argv[2]), int(argv[3])))

strip.show()