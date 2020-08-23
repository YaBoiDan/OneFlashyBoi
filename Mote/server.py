from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import json
import cgi
import subprocess
import sys
import os

#Scripts have been appended to not clear after launch where possible, this negates the requirement to keep them in loops unless they need to change dynamically. Optionally you can also remove the 'Process' from these, although you will need to run clear by default save getting caught with colour mixing. Additionally, this should mean that if you somehow manage to launch two processes, they won't overwrite as they aren't both still running in loops.

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
        elif Mode == "Off":
            print (f"DEBUG: We hit {Mode}!")
            self.KillLights()
        elif Mode == "ClearAnyway":
            Process = subprocess.call(["python3", "motescripts/moteOff.py"])
            Process = ""
            #Reload and clear usually fixes things
            return
        #elif Mode == "ClearAnyway+Force":
            #Run clear, this is for when a process isn't running but you wanna clear. Also task kill anything under the 'motescript' directory for sure.
        elif Mode == "Rainbow":
            print (f"DEBUG: We hit {Mode}!")
            self.KillLights()
            Process = subprocess.Popen(["python3", "motescripts/rainbow.py"])
        elif Mode == "RainbowStatic":
            print (f"DEBUG: We hit {Mode}!")
            self.KillLights()
            Process = subprocess.Popen(["python3", "motescripts/static-rainbow.py"])
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
            dicts = {}
            self.KillLights()

            if "Colour" in ReceivedData["Sticks"][0]: #If stick one has a colour defined rather than per pixel defined.
                for num, Stick in enumerate (ReceivedData["Sticks"], start=1): #Enumerate and build dictionary of values.
                    print (Stick["Colour"])
                    RGB = self.hex_to_rgb(Stick["Colour"]) #Convert to RGB from Hex
                    #print (RGB)
                    dicts[("R"+str(num))] = str(RGB[0])
                    dicts[("G"+str(num))] = str(RGB[1])
                    dicts[("B"+str(num))] = str(RGB[2])
                
                Process = subprocess.Popen([ #Pass args to manual mote script
                    "python3", 
                    "motescripts/moteManual.py",
                    dicts["R1"],dicts["G1"],dicts["B1"],
                    dicts["R2"],dicts["G2"],dicts["B2"],
                    dicts["R3"],dicts["G3"],dicts["B3"],
                    dicts["R4"],dicts["G4"],dicts["B4"]
                ])

            else: #If no colour per stick is set, assume pixels
                if "Colour" in ReceivedData["Sticks"][0]["Pixels"][0]: #Check first pixel for colour, basic test but happens before per pixel enumeration.
                    print (">>>Hit Super Manual")
                    for num, Stick in enumerate (ReceivedData["Sticks"], start=1):
                        for PNum, Pixel in enumerate (Stick["Pixels"], start=1):
                            RGB = self.hex_to_rgb(Pixel["Colour"])
                            #print (RGB)
                            dicts[("R"+str(num)+"-"+str(PNum))] = str(RGB[0])
                            dicts[("G"+str(num)+"-"+str(PNum))] = str(RGB[1])
                            dicts[("B"+str(num)+"-"+str(PNum))] = str(RGB[2])
                    #Try itterating through, if value not defined, return malformed request. Try triggering this by not setting a single pixel value per stick?
                    #print (dicts)
                    #Not sure I like passing 193 args to a script...
                    Process = subprocess.Popen([ #Pass args to manual mote script
                    "python3", 
                    "motescripts/moteSuperManual.py",
                    dicts["R1-1"], dicts["G1-1"], dicts["B1-1"],
                    dicts["R1-2"], dicts["G1-2"], dicts["B1-2"],
                    dicts["R1-3"], dicts["G1-3"], dicts["B1-3"],
                    dicts["R1-4"], dicts["G1-4"], dicts["B1-4"],
                    dicts["R1-5"], dicts["G1-5"], dicts["B1-5"],
                    dicts["R1-6"], dicts["G1-6"], dicts["B1-6"],
                    dicts["R1-7"], dicts["G1-7"], dicts["B1-7"],
                    dicts["R1-8"], dicts["G1-8"], dicts["B1-8"],
                    dicts["R1-9"], dicts["G1-9"], dicts["B1-9"],
                    dicts["R1-10"], dicts["G1-10"], dicts["B1-10"],
                    dicts["R1-11"], dicts["G1-11"], dicts["B1-11"],
                    dicts["R1-12"], dicts["G1-12"], dicts["B1-12"],
                    dicts["R1-13"], dicts["G1-13"], dicts["B1-13"],
                    dicts["R1-14"], dicts["G1-14"], dicts["B1-14"],
                    dicts["R1-15"], dicts["G1-15"], dicts["B1-15"],
                    dicts["R1-16"], dicts["G1-16"], dicts["B1-16"],
                    dicts["R2-1"], dicts["G2-1"], dicts["B2-1"],
                    dicts["R2-2"], dicts["G2-2"], dicts["B2-2"],
                    dicts["R2-3"], dicts["G2-3"], dicts["B2-3"],
                    dicts["R2-4"], dicts["G2-4"], dicts["B2-4"],
                    dicts["R2-5"], dicts["G2-5"], dicts["B2-5"],
                    dicts["R2-6"], dicts["G2-6"], dicts["B2-6"],
                    dicts["R2-7"], dicts["G2-7"], dicts["B2-7"],
                    dicts["R2-8"], dicts["G2-8"], dicts["B2-8"],
                    dicts["R2-9"], dicts["G2-9"], dicts["B2-9"],
                    dicts["R2-10"], dicts["G2-10"], dicts["B2-10"],
                    dicts["R2-11"], dicts["G2-11"], dicts["B2-11"],
                    dicts["R2-12"], dicts["G2-12"], dicts["B2-12"],
                    dicts["R2-13"], dicts["G2-13"], dicts["B2-13"],
                    dicts["R2-14"], dicts["G2-14"], dicts["B2-14"],
                    dicts["R2-15"], dicts["G2-15"], dicts["B2-15"],
                    dicts["R2-16"], dicts["G2-16"], dicts["B2-16"],
                    dicts["R3-1"], dicts["G3-1"], dicts["B3-1"],
                    dicts["R3-2"], dicts["G3-2"], dicts["B3-2"],
                    dicts["R3-3"], dicts["G3-3"], dicts["B3-3"],
                    dicts["R3-4"], dicts["G3-4"], dicts["B3-4"],
                    dicts["R3-5"], dicts["G3-5"], dicts["B3-5"],
                    dicts["R3-6"], dicts["G3-6"], dicts["B3-6"],
                    dicts["R3-7"], dicts["G3-7"], dicts["B3-7"],
                    dicts["R3-8"], dicts["G3-8"], dicts["B3-8"],
                    dicts["R3-9"], dicts["G3-9"], dicts["B3-9"],
                    dicts["R3-10"], dicts["G3-10"], dicts["B3-10"],
                    dicts["R3-11"], dicts["G3-11"], dicts["B3-11"],
                    dicts["R3-12"], dicts["G3-12"], dicts["B3-12"],
                    dicts["R3-13"], dicts["G3-13"], dicts["B3-13"],
                    dicts["R3-14"], dicts["G3-14"], dicts["B3-14"],
                    dicts["R3-15"], dicts["G3-15"], dicts["B3-15"],
                    dicts["R3-16"], dicts["G3-16"], dicts["B3-16"],
                    dicts["R4-1"], dicts["G4-1"], dicts["B4-1"],
                    dicts["R4-2"], dicts["G4-2"], dicts["B4-2"],
                    dicts["R4-3"], dicts["G4-3"], dicts["B4-3"],
                    dicts["R4-4"], dicts["G4-4"], dicts["B4-4"],
                    dicts["R4-5"], dicts["G4-5"], dicts["B4-5"],
                    dicts["R4-6"], dicts["G4-6"], dicts["B4-6"],
                    dicts["R4-7"], dicts["G4-7"], dicts["B4-7"],
                    dicts["R4-8"], dicts["G4-8"], dicts["B4-8"],
                    dicts["R4-9"], dicts["G4-9"], dicts["B4-9"],
                    dicts["R4-10"], dicts["G4-10"], dicts["B4-10"],
                    dicts["R4-11"], dicts["G4-11"], dicts["B4-11"],
                    dicts["R4-12"], dicts["G4-12"], dicts["B4-12"],
                    dicts["R4-13"], dicts["G4-13"], dicts["B4-13"],
                    dicts["R4-14"], dicts["G4-14"], dicts["B4-14"],
                    dicts["R4-15"], dicts["G4-15"], dicts["B4-15"],
                    dicts["R4-16"], dicts["G4-16"], dicts["B4-16"]
                ])
                else:
                    print (">>>Malformed manual request")
                    raise Exception("Malformed manual request, check JSON")

            #print (dicts)

        # send the message back
        self._set_headers()
        self.wfile.write(json.dumps(ReceivedData).encode()) #Parrot
        
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