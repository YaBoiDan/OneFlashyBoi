from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import json
import cgi
import subprocess
import sys
import os

# Scripts have been appended to not clear after launch where possible, this negates the requirement to keep them in loops unless they need to change dynamically. Optionally you can also remove the 'Process' from these, although you will need to run clear by default save getting caught with colour mixing. Additionally, this should mean that if you somehow manage to launch two processes, they won't overwrite as they aren't both still running in loops.

global Process
global ConfigData
Process = ""
ConfigData = json.loads('{"Mode":"Off"}')


def KillLights():
    global Process
    global ConfigData
    # Because it is set as a string above to stop NameError (Calling before defined)
    if Process == "":
        print("PiLights are not running...")
        return
    else:
        print("PILights are running... Killing...")
        Process.terminate()
        Process.kill()
        Process = subprocess.call(["python3",  os.path.dirname(
            os.path.abspath(__file__)) + "/LEDScripts/moteOff.py"])
        Process = ""
        ConfigData = json.loads('{"Mode":"Off"}')
        return


class Server(BaseHTTPRequestHandler):
    # Declare all of the Class Vars here

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_HEAD(self):
        print('>> Requested Header')
        self._set_headers()

    # GET sends back the current state as defined by correctly formatted JSON.
    def do_GET(self):
        global ConfigData
        print('>> Requested Data, GET started')
        #print(ConfigData)
        #print(json.dumps(ConfigData).encode())
        self._set_headers()
        self.wfile.write(json.dumps(ConfigData).encode())

    def do_POST(self):
        global Process
        global ConfigData
        print('>> Posted Data, POST started')
        ctype, pdict = cgi.parse_header(self.headers['Content-Type'])

        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return

        length = int(self.headers['content-length'])
        #ReceivedDataDebug = self.rfile.read(length)  # DEBUG
        #print(ReceivedDataDebug)
        ReceivedData = json.loads(self.rfile.read(length))

        print(f"> Received Data: {ReceivedData}")
        Mode = ReceivedData["Mode"]
        # print (Mode) #Debug

        """ Pro tips!
        # add a property to the object, just to mess with data
        ReceivedData['Received'] = 'ok'
        """

        if Mode == "On":
            print(f"DEBUG: We hit {Mode}!")
            KillLights()
            Process = subprocess.Popen(["python3",  os.path.dirname(
                os.path.abspath(__file__)) + "/LEDScripts/moteOn.py"])
        elif Mode == "Off":
            print(f"DEBUG: We hit {Mode}!")
            KillLights()
        elif Mode == "ClearAnyway":
            Process = subprocess.call(["python3",  os.path.dirname(
                os.path.abspath(__file__)) + "/LEDScripts/moteOff.py"])
            Process = ""
            # Reload and clear usually fixes things
            return
        elif Mode == "Rainbow":
            print(f"DEBUG: We hit {Mode}!")
            KillLights()
            Process = subprocess.Popen(["python3",  os.path.dirname(
                os.path.abspath(__file__)) + "/LEDScripts/Rainbow.py"])
        elif Mode == "RainbowStatic":
            print(f"DEBUG: We hit {Mode}!")
            KillLights()
            Process = subprocess.Popen(["python3",  os.path.dirname(
                os.path.abspath(__file__)) + "/LEDScripts/RainbowStatic.py"])
        elif Mode == "Bilgetank":
            print(f"DEBUG: We hit {Mode}!")
            KillLights()
            Process = subprocess.Popen(["python3",  os.path.dirname(
                os.path.abspath(__file__)) + "/LEDScripts/bilgetank.py"])
        elif Mode == "Helltank":
            print(f"DEBUG: We hit {Mode}!")
            KillLights()
            Process = subprocess.Popen(["python3",  os.path.dirname(
                os.path.abspath(__file__)) + "/LEDScripts/helltank.py"])
        elif Mode == "Reload":
            print(f"DEBUG: We hit {Mode}!")
            KillLights()
            os.execl(sys.executable, 'python', __file__, *sys.argv[1:])
        elif Mode == "Manual":
            print(f"DEBUG: We hit {Mode}!")
            KillLights()
            # print(type(ReceivedData["Colour"][0]["R"]))
            Process = subprocess.Popen([  # Pass args to manual script
                "python3",
                os.path.dirname(os.path.abspath(__file__)) + \
                "/LEDScripts/moteManual.py",
                # Home Assistant (YAML) makes these integers, PoSh and everything else is generally a string, as it should be.
                str(ReceivedData["Colour"][0]["R"]),
                str(ReceivedData["Colour"][0]["G"]),
                str(ReceivedData["Colour"][0]["B"]),
            ])
        elif Mode == "ManualDetailed":
            print(f"DEBUG: We hit {Mode}!")
            KillLights()
            # print(type(ReceivedData["Colour"][0]["R"]))
            Process = subprocess.Popen([  # Pass args to manual script
                "python3",
                os.path.dirname(os.path.abspath(__file__)) + \
                "/LEDScripts/moteManualDetailed.py",
                # Home Assistant (YAML) makes these integers, PoSh and everything else is generally a string, as it should be.
                str(ReceivedData["Channel1"][0]["Colour"][0]["R"]),
                str(ReceivedData["Channel1"][0]["Colour"][0]["G"]),
                str(ReceivedData["Channel1"][0]["Colour"][0]["B"]),
                str(ReceivedData["Channel2"][0]["Colour"][0]["R"]),
                str(ReceivedData["Channel2"][0]["Colour"][0]["G"]),
                str(ReceivedData["Channel2"][0]["Colour"][0]["B"]),
                str(ReceivedData["Channel3"][0]["Colour"][0]["R"]),
                str(ReceivedData["Channel3"][0]["Colour"][0]["G"]),
                str(ReceivedData["Channel3"][0]["Colour"][0]["B"]),
                str(ReceivedData["Channel4"][0]["Colour"][0]["R"]),
                str(ReceivedData["Channel4"][0]["Colour"][0]["G"]),
                str(ReceivedData["Channel4"][0]["Colour"][0]["B"]),
            ])
        # I need to find a way to do this without grabbing 192 values
        # elif Mode == "ManualSuperDetailed":
        #     print(f"DEBUG: We hit {Mode}!")
        #     KillLights()
        #     # print(type(ReceivedData["Colour"][0]["R"]))
        #     Process = subprocess.Popen([  # Pass args to manual script
        #         "python3",
        #         os.path.dirname(os.path.abspath(__file__)) + \
        #         "/LEDScripts/moteManualSuperDetailed.py",
        #         # Home Assistant (YAML) makes these integers, PoSh and everything else is generally a string, as it should be.
        #         str(ReceivedData["Channel1"][0]["Pixel1"][0]["Colour"][0]["R"]),
        #         str(ReceivedData["Channel1"][0]["Pixel1"]["Colour"][0]["G"]),
        #         str(ReceivedData["Channel1"][0]["Pixel1"]["Colour"][0]["B"]),
        #         str(ReceivedData["Channel2"][0]["Pixel1"]["Colour"][0]["R"]),
        #         str(ReceivedData["Channel2"][0]["Pixel1"]["Colour"][0]["G"]),
        #         str(ReceivedData["Channel2"][0]["Pixel1"]["Colour"][0]["B"]),
        #         str(ReceivedData["Channel3"][0]["Pixel1"]["Colour"][0]["R"]),
        #         str(ReceivedData["Channel3"][0]["Pixel1"]["Colour"][0]["G"]),
        #         str(ReceivedData["Channel3"][0]["Pixel1"]["Colour"][0]["B"]),
        #         str(ReceivedData["Channel4"][0]["Pixel1"]["Colour"][0]["R"]),
        #         str(ReceivedData["Channel4"][0]["Pixel1"]["Colour"][0]["G"]),
        #         str(ReceivedData["Channel4"][0]["Pixel1"]["Colour"][0]["B"]),
        #     ])
        else:
            self._set_headers()
            self.wfile.write(json.loads(
                '{"Result":"This is not the result you were looking for..."}'))
            return

        # This is defined as changing Received Data for reporting current state on GET would break as KillLights() would set this, then it's referenced by the modes that pass args, expecting more than just "Mode:Off".
        ConfigData = ReceivedData
        #print ("DEBUG: Should only see in valid request!!!")
        self._set_headers()
        self.wfile.write(json.dumps(ConfigData).encode())


def run(server_class=HTTPServer, handler_class=Server, port=666):
    try:
        server_address = ('', port)
        httpd = server_class(server_address, handler_class)
        print('Starting Server...')
        sa = httpd.server_address
        print(f"Serving on {sa[0]}:{sa[1]}")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n>> Interrupt received, stopping.")
    except Exception as e:
        print(str(e))
    finally:
        print("Killing Pi Lights.")
        KillLights()
        print("Done, exiting.")
        quit()
        sys.exit()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
