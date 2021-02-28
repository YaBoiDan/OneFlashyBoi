# OneFlashyBoi

## Run at startup

Add the below to the end of the /etc/rc.local file:

```bash
python3 /home/pi/OneFlashyBoi/LightStrip/LightsServer.py >/home/pi/OneFlashyBoi/OneFlashyBoi.log 2>&1
```

This must be in place *before* the exit 0.
