from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import json
import cgi
import subprocess
import sys
import os

global Process
Process = ""

class Server(BaseHTTPRequestHandler):
# Declare all of the Class Vars here

    def KillLights(self):
        global Process
        if Process == "": #Because it is set as a string above to stop NameError (Calling before defined)
            print ("PiLights are not running...")
            return
        else:
            print ("PILights are running... Killing...")
            Process.terminate()
            Process.kill()
            Process = subprocess.call(["python3", "motescripts/moteOff.py"])
            Process = ""
            return

    def hex_to_rgb(self,value):
        value = value.lstrip('#')
        RGB = tuple(int(value[i:i+2], 16) for i in (0, 2, 4))
        return RGB

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
    def do_HEAD(self):
        print ('>> Requested Header')
        self._set_headers()
        
    # GET sends back a Hello world message
    def do_GET(self):
        print ('>> Requested Data, GET started')
        self._set_headers()
        self.wfile.write(json.dumps({
            'hello': 'world',
            'received': 'ok'
            }).encode())
        
    # POST echoes the message adding a JSON field
    def do_POST(self):
        global Process
        print ('>> Posted Data, POST started')
        ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
        
        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return
            
        # read the message and convert it into a python dictionary
        length = int(self.headers['content-length'])
        ReceivedData = json.loads(self.rfile.read(length))
        
        print (f"> Received Data: {ReceivedData}")
        Mode = ReceivedData["Mode"]
        #print (Mode) #Debug

        """
        # add a property to the object, just to mess with data
        ReceivedData['Received'] = 'ok'
        """

        """ 
        [Mode]     :   [On / Off / etc]
        [Sticks]   :   [Container]
            [Stick 1]  :   [RRGGBB / Blank if per LED]
                [LED0] :   [RRGGBB(Brightness 0.1-1)]
                [LED1] :   [RRGGBB(Brightness 0.1-1)]
                [LEDx] :   [RRGGBB(Brightness 0.1-1)]
            [Stick 2]  :   [RRGGBB(Brightness 0.1-1)]
                [LED0] :   [RRGGBB(Brightness 0.1-1)]
                [LED1] :   [RRGGBB(Brightness 0.1-1)]
                [LEDx] :   [RRGGBB(Brightness 0.1-1)]
            [Stick 3]  :   [RRGGBB(Brightness 0.1-1)]
            [Stick 4]  :   [RRGGBB(Brightness 0.1-1)]
        """

        if Mode == "On":
            print (f"DEBUG: We hit {Mode}!")
            self.KillLights()
            Process = subprocess.Popen(["python3", "motescripts/moteOn.py"])
            print (Process)
        elif Mode == "Off":
            print (f"DEBUG: We hit {Mode}!")
            self.KillLights()
        elif Mode == "Rainbow":
            print (f"DEBUG: We hit {Mode}!")
            Process = subprocess.Popen(["python3", "motescripts/rainbow.py"])
            self.KillLights()
        elif Mode == "RainbowStatic":
            print (f"DEBUG: We hit {Mode}!")
            Process = subprocess.Popen(["python3", "motescripts/static-rainbow.py"])
            self.KillLights()
        elif Mode == "Bilge":
            print (f"DEBUG: We hit {Mode}!")
            self.KillLights()
            Process = subprocess.Popen(["python3", "motescripts/bilgetank.py"])
        elif Mode == "Reload":
            print (f"DEBUG: We hit {Mode}!")
            self.KillLights()
            os.execl(sys.executable, 'python', __file__, *sys.argv[1:])
        elif Mode == "Manual":
            print (f"DEBUG: We hit {Mode}!")
            #ReceivedData["Mode"]
            #for Stick in ReceivedData["Sticks"]:
            dicts = {}

            for num, Stick in enumerate (ReceivedData["Sticks"], start=1):
                print (Stick["Colour"])
                RGB = self.hex_to_rgb(Stick["Colour"])
                #print (RGB)
                #print (RGB[0])
                dicts[("R"+str(num))] = str(RGB[0])
                dicts[("G"+str(num))] = str(RGB[1])
                dicts[("B"+str(num))] = str(RGB[2])

            print(dicts["R1"])
            #print (dicts["R1"],dicts["G1"],dicts["B1"],dicts["R2"],dicts["G2"],dicts["B2"])

            Process = subprocess.Popen([
                "python3", 
                "motescripts/moteManual.py",
                dicts["R1"],dicts["G1"],dicts["B1"],
                dicts["R2"],dicts["G2"],dicts["B2"],
                dicts["R3"],dicts["G3"],dicts["B3"],
                dicts["R4"],dicts["G4"],dicts["B4"]
            ])

        # send the message back
        self._set_headers()
        self.wfile.write(json.dumps(ReceivedData).encode())
        
def run(server_class=HTTPServer, handler_class=Server, port=666):
    try:
        server_address = ('', port)
        httpd = server_class(server_address, handler_class)
        print ('Starting Server...')
        sa = httpd.server_address
        print (f"Serving on {sa[0]}:{sa[1]}")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n>> Interrupt received, stopping...")
    finally:
        print ("RIP in pieces Pi Lights")
        Server.KillLights #Call it from the classhttpserver-on
        quit()
        sys.exit()
if __name__ == "__main__":
    from sys import argv
    
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()