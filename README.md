# OneFlashyBoi

## Run at startup

Add the below to the end of the /etc/rc.local file:

```bash
python3 /home/pi/OneFlashyBoi/LightStrip/LightsServer.py >/home/pi/OneFlashyBoi/OneFlashyBoi.log 2>&1
```

This must be in place *before* the exit 0.

## Mote Install

I had issues installing using the install commands provided by Pimoroni, commands would run, but lights would not light. I ended up installing older version of the library, got it working and then installed the latest version, it kept working.
