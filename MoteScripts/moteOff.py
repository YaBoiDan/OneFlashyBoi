#!/usr/bin/env python
import motephat
import time

motephat.configure_channel(1, 16, False)
motephat.configure_channel(2, 16, False)
motephat.configure_channel(3, 16, False)
motephat.configure_channel(4, 16, False)

motephat.clear()
motephat.show()
quit()