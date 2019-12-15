from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import json
import cgi

class Server(BaseHTTPRequestHandler):
# Declare all of the Class Vars here

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
        self.wfile.write(json.dumps({'hello': 'world', 'received': 'ok'}))
        
    # POST echoes the message adding a JSON field
    def do_POST(self):
        print ('>> Posted Data, POST started')
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        
        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return
            
        # read the message and convert it into a python dictionary
        length = int(self.headers.getheader('content-length'))
        message = json.loads(self.rfile.read(length))
        
        # add a property to the object, just to mess with data
        message['Received'] = 'ok'
        
        # send the message back
        self._set_headers()
        self.wfile.write(json.dumps(message))
        
def run(server_class=HTTPServer, handler_class=Server, port=8008):
    try:
		server_address = ('', port)
		httpd = server_class(server_address, handler_class)
		print ('Starting Server...')
		sa = httpd.socket.getsockname()
		print ("Serving on {0}:{1}").format(sa[0],sa[1])
		httpd.serve_forever()
	except KeyboardInterrupt:
		print("Interrupt received, stopping...")
	finally:
		#os.system('clear')
		print ("RIP Pi Lights")
		S.KillLights #Call it from the classhttpserver-on
		quit()
		sys.exit()
    
if __name__ == "__main__":
    from sys import argv
    
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()