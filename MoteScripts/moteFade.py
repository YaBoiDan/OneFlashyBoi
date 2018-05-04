import motephat
import time
from sys import argv

#255, 0, 164 x 0, 139, 255

if len(argv) != 7: #[Program] [R1] [G1] [B1] [R2] [G2] [B2]
    print ("Not enough Variables")
    quit()

motephat.configure_channel(1, 16, False)
motephat.configure_channel(2, 16, False)
motephat.configure_channel(3, 16, False)
motephat.configure_channel(4, 16, False)

try:
    while True:
        for pixel in range(16):
            motephat.set_pixel(2, pixel, argv[1], argv[2], argv[3],brightness=1)
            motephat.set_pixel(3, pixel, argv[1], argv[2], argv[3],brightness=1)
            motephat.set_pixel(1, pixel, argv[4], argv[5], argv[6],brightness=1)
            motephat.set_pixel(4, pixel, argv[4], argv[5], argv[6],brightness=1)
        motephat.show()
except KeyboardInterrupt:
    motephat.clear()
    motephat.show()
    quit()