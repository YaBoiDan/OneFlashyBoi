#!/usr/bin/env python
import motephat
from sys import argv

if len(argv) != 4: #[Program] [R1] [G1] [B1] [R2] [G2] [B2]
    print ("Not enough Variables")
    quit()

motephat.configure_channel(1, 16, False)
motephat.configure_channel(2, 16, False)
motephat.configure_channel(3, 16, False)
motephat.configure_channel(4, 16, False)
motephat.set_clear_on_exit(False)

for channel in range(1,5):
    for pixel in range(16):
        motephat.set_pixel(channel, pixel, argv[1], argv[2], argv[3],brightness=1)
motephat.show()