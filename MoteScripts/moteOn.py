import motephat
import time

motephat.configure_channel(1, 16, False)
motephat.configure_channel(2, 16, False)
motephat.configure_channel(3, 16, False)
motephat.configure_channel(4, 16, False)

try:
    while True:
        for channel in range(1, 5):
            for pixel in range(16):
                motephat.set_pixel(channel, pixel, 255, 46, 0,brightness=1)
        motephat.show()
except KeyboardInterrupt:
    motephat.clear()
    motephat.show()
    quit()