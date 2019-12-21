import motephat
from sys import argv
import time

if len(argv) != 193:
	print ("Not enough Variables")
	print (len(argv))
	quit()

motephat.configure_channel(1, 16, False)
motephat.configure_channel(2, 16, False)
motephat.configure_channel(3, 16, False)
motephat.configure_channel(4, 16, False)
motephat.set_clear_on_exit(False)

Plus = 0
AAA = 0
for stick in range (4):
	for pixel in range(16):  
		PixelRArg = (AAA + 1)
		PixelGArg = (AAA + 2)
		PixelBArg = (AAA + 3)
		AAA += 3
		
		print (f"{argv[PixelRArg]}, {argv[PixelGArg]}, {argv[PixelBArg]}")
		motephat.set_pixel (stick, pixel, argv[PixelRArg], argv[PixelGArg], argv[PixelBArg], brightness=0.2)
		# motephat.show()
		# time.sleep (0.25)
motephat.show()