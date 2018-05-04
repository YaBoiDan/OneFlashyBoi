import motephat
import time
from sys import argv

if len(argv) != 4:
    print ("Not enough Variables")

motephat.configure_channel(1, 16, False)
motephat.configure_channel(2, 16, False)
motephat.configure_channel(3, 16, False)
motephat.configure_channel(4, 16, False)

try:
    while True:
        for channel in range(1, 5):
            for pixel in range(16):
                motephat.set_pixel(channel, pixel, argv[1], argv[2], argv[3])
        motephat.show()
except KeyboardInterrupt:
    motephat.clear()
    motephat.show()
    quit()