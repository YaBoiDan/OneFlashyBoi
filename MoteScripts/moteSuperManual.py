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

""" for values in argv:
	print (values)

time.sleep(10) """

print ("It worked!")
try:
	while True:
		Plus = 0
		AAA = 0
		for stick in range (1,5): #Add one as not starting at 0
			for pixel in range(1,17):  #Add one as not starting at 0
				# pixelRArg = (stick * pixel + Plus)
				# PixelGArg = (stick * pixel + Plus + 1)
				# PixelBArg = (stick * pixel + Plus + 2)
				pixelRArg = (AAA + 1)
				PixelGArg = (AAA + 2)
				PixelBArg = (AAA + 3)
				AAA += 3
				#print (f"Set Stick {stick}, Pixels {pixel}: {pixelRArg}, {PixelGArg}, {PixelBArg}")
				
				motephat.set_pixel(stick, pixel, argv[pixelRArg], argv[PixelGArg], argv[PixelBArg],brightness=0.2)
				motephat.set_pixel(stick, pixel, pixelRArg, PixelGArg, PixelBArg,brightness=0.2)
				#Plus = Plus + 2 #Plus 2 as it's + 1 from stick increment + 2
				#print (Plus)
			#Plus = Plus + 15 #Add 14 as it is missing 14 when it starts on the next stick
		motephat.show()
except KeyboardInterrupt:
	motephat.clear()
	motephat.show()
	quit()