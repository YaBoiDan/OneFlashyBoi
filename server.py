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
        print (ReceivedData["Mode"]) #Debug

        """
        # add a property to the object, just to mess with data
        ReceivedData['Received'] = 'ok'
        """

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