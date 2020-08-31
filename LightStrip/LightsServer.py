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
    CurrentState = "Off"

    def KillLights(self):
        global Process
        if Process == "": #Because it is set as a string above to stop NameError (Calling before defined)
            print ("PiLights are not running...")
            return
        else:
            print ("PILights are running... Killing...")
            Process.terminate()
            Process.kill()
            Process = subprocess.call(["python3", "LEDScripts/Off.py"])
            Process = ""
            CurrentState = "Off"
            return

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
            'Received': 'ok',
            'Result': 'This is not the result you were looking for...'
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

        if Mode == "On":
            print (f"DEBUG: We hit {Mode}!")
            self.KillLights()
            Process = subprocess.Popen(["python3", "LEDScripts/On.py"])
            CurrentState = Mode
        elif Mode == "Off":
            print (f"DEBUG: We hit {Mode}!")
            self.KillLights()
        elif Mode == "ClearAnyway":
            Process = subprocess.call(["python3", "LEDScripts/Off.py"])
            Process = ""
            #Reload and clear usually fixes things
            CurrentState = "Off"
            return
        elif Mode == "Rainbow":
            print (f"DEBUG: We hit {Mode}!")
            self.KillLights()
            Process = subprocess.Popen(["python3", "LEDScripts/Rainbow.py"])
            CurrentState = Mode
        elif Mode == "RainbowR":
            print (f"DEBUG: We hit {Mode}!")
            self.KillLights()
            Process = subprocess.Popen(["python3", "LEDScripts/RainbowR.py"])
            CurrentState = Mode
        elif Mode == "Bilge":
            print (f"DEBUG: We hit {Mode}!")
            self.KillLights()
            Process = subprocess.Popen(["python3", "LEDScripts/bilgetank.py"])
            CurrentState = Mode
        elif Mode == "Reload":
            print (f"DEBUG: We hit {Mode}!")
            self.KillLights()
            os.execl(sys.executable, 'python', __file__, *sys.argv[1:])
        elif Mode == "Manual":
            print (f"DEBUG: We hit {Mode}!")
            self.KillLights()
            
            Process = subprocess.Popen([ #Pass args to manual script
                "python3", 
                "LEDScripts/Manual.py",
                ReceivedData["Colour"][0]["R"],
                ReceivedData["Colour"][0]["G"],
                ReceivedData["Colour"][0]["B"],
            ])
            CurrentState = Mode
        elif Mode == "Marquee":
            print (f"DEBUG: We hit {Mode}!")
            self.KillLights()
            
            Process = subprocess.Popen([ #Pass args to manual script
                "python3", 
                "LEDScripts/Marquee.py",
                ReceivedData["Colour"][0]["R"],
                ReceivedData["Colour"][0]["G"],
                ReceivedData["Colour"][0]["B"],
            ])
            CurrentState = Mode

        # send the message back
        self._set_headers()
        #self.wfile.write(json.dumps(ReceivedData).encode()) #Parrot
        self.wfile.write(json.dumps({
            'Received': 'ok',
            'Mode': Mode
            }).encode())
        
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