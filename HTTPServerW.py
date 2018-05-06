#!/usr/bin/env python
"""
Very simple HTTP server in python.
Usage:
	 ./HTTPserver.py [<port>]
"""

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import sys
import motephat
import time
import subprocess
import os
import signal

global Dataz,process, R, G, B, R2, G2, B2 #We need to make them global variables so they can be read inside the function.
process = ""
Dataz = "Nil"
dict = {}
R = 0 #We need these otherwise it flags as accessing a variable before it is defined (See the layout of 'Switch')
G = 0
B = 0
R2 = 0
G2 = 0
B2 = 0

class S(BaseHTTPRequestHandler):
	def _set_headers(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

	def KillLights(self):
		process.poll
		print ("PILights are already on... Killing...")
		process.terminate()
		process.returncode()
		motephat.clear()
		motephat.show()

	def do_GET(self):
		print ("********Start GET********") #Get whole list and filter through on their side or ours?
		self._set_headers()
		print ("Var(s) Requested: ",self.path[1:])
		VarReq = self.path[1:]
		try:
			if self.path == ("/Jives.html"):
					f = open("/home/pi/bin/Python/ControlPanel/" + self.path)
					self.wfile.write(f.read())
					f.close()
					return
			if self.path == ("/Arnold.html"):
					f = open("/home/pi/bin/Python/ControlPanel/" + self.path)
					self.wfile.write(f.read())
					f.close()
					return
		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)
		if VarReq == "AllDict": #No path / arg will send whole table
			self.wfile.write(dict)
		else:
			AllVars = VarReq.split(";")
			dicVarReq = ""
			for i in AllVars:
				print ("Var: ",i)
				try:
					dicVarReq = dicVarReq + i + "=" + dict[i] +";"
				except KeyError: #Not hitting
					self.wfile.write("Var '"+i+"' Not Found...")
					dicVarReq = " " #Put this here otherwise it prints next var
					break
			dicVarReq = dicVarReq[:-1]
			self.wfile.write(dicVarReq)
		print ("********End GET********")
		print ("")

	def do_HEAD(self):
		print ("********Header Request********")
		self._set_headers()
  
	def do_POST(self):
		global process
		print ("********Start POST********")
		print >>sys.stderr,"Header: ", self._set_headers()
		#self.wfile.write("You did a POST!") #Send reply
		print >>sys.stderr,"From: ", self. client_address
		length = int(self.headers['Content-Length'])
		Dataz = self.rfile.read(length)
		print >>sys.stderr,"Data Length: ",length
		print ("======Start All Data======")
		print (Dataz)
		print ("======End All Data======")
		print ("")
		
		MadData = Dataz.split(";") #Multiple Vars are separated with this
		print ("====== String Split Start ======")
		try:
			for SepDataz in MadData: #Split into pairs
				print (SepDataz)
				print ("=== Split Again Start ===")
				MoreData = SepDataz.split("=") #Split individually
				print >>sys.stderr,"!!!Var Set: ",MoreData[0] #Expect 2 vars x=y
				VarName=MoreData[0]
				VarValue=MoreData[1]
				dict[VarName] = VarValue # Add new entry, can't use above with array though...
				#print ("dict:Test: ", dict["Test"]) #Print certain key
				print >>sys.stderr,"Whole Dict: ", str(dict) #Print whole list
				# Make it so everytime a var changes, it saves to file
				print ("=== Split Again End ===")
				print ("====== String Split End ======")
				if VarName == "PiLights":
					if VarValue.startswith("On") and len(VarValue) < 6: #Change to Regex (re.match(pattern, string, flags=0)) Patter is
						try:
							self.KillLights()
						except:
							Brightness = SepDataz.split(".")
							Brightness = float(Brightness[1])/10 #Receives brightness 1-10
							print ("Brightness: " ,Brightness)
							print ("PILights ",VarValue)
							process = subprocess.Popen(["python3.4", "/home/pi/bin/Python/MoteScripts/moteOnW.py",str(Brightness)]) #Must be passed as string
							self.wfile.write(("PiLights ",VarValue)) #Send reply
					elif VarValue == "Off":
						try:
							print ("PILights ",VarValue)
							process.poll
							print ("PILights are on... Killing...")
							process.terminate()
							motephat.clear()
							motephat.show()
							self.wfile.write(("PiLights ",VarValue)) #Send reply
						except:
							print ("PILights Not Started")
							self.wfile.write("PiLights Not Started") #Send reply
					elif VarValue == "Rainbow":
						try:
							self.KillLights()
						except:
							print ("PILights ",VarValue)
							process = subprocess.Popen(["python3.4", "/home/pi/bin/Python/MoteScripts/rainbowW.py"])
							self.wfile.write(("PiLights ",VarValue)) #Send reply
					elif VarValue == "Bilge":
						try:
							self.KillLights()
						except:
							print ("PILights ",VarValue)
							process = subprocess.Popen(["python3.4", "/home/pi/bin/Python/MoteScripts/bilgetankW.py"])
							self.wfile.write(("PiLights ",VarValue)) #Send reply
					elif VarValue == "Hell":
						try:
							self.KillLights()
						except:
							print ("PILights ",VarValue)
							process = subprocess.Popen(["python3.4", "/home/pi/bin/Python/MoteScripts/helltankW.py"])
							self.wfile.write(("PiLights ",VarValue)) #Send reply
					elif VarValue.startswith('ManFade'):
						try:
							Colours = SepDataz.split(".")
							print (Colours)
							try:
								self.KillLights()
							except:
								print ("PILights ",VarValue)
								global  R, G, B, R2, G2, B2
								TmpR = R
								TmpG = G
								TmpB = B
								R = R2
								G = G2
								B = B2
								R2 = TmpR
								G2 = TmpG
								B2 = TmpB
								if VarValue == "ManFade.Switch":
									process = subprocess.Popen(["python3.4", "/home/pi/bin/Python/MoteScripts/moteFadeW.py",R,G,B,R2,G2,B2])
									self.wfile.write(("PiLights ","Switch ",R2," ",G2," ",B2, " x ", R," ",G," ",B)) #Send reply
								else:
									R = Colours[1]
									G = Colours[2]
									B = Colours[3]
									R2 = Colours[4]
									G2 = Colours[5]
									B2 = Colours[6]
									process = subprocess.Popen(["python3.4", "/home/pi/bin/Python/MoteScripts/moteFadeW.py",R,G,B,R2,G2,B2])
									self.wfile.write(("PiLights ",VarValue," ",R," ",G," ",B," x ",R2," ",G2," ",B2)) #Send reply
						except:
							print ("RGB Colour error!")
					elif VarValue.startswith('Man'):
						try:
							Colours = SepDataz.split(".")
							print (Colours)
							try:
								self.KillLights()
							except:
								print ("PILights ",VarValue)
								R = Colours[1]
								G = Colours[2]
								B = Colours[3]
								process = subprocess.Popen(["python3.4", "/home/pi/bin/Python/MoteScripts/manualSetW.py",R,G,B])
								self.wfile.write(("PiLights ",VarValue," ",R," ",G," ",B)) #Send reply
						except:
							print ("RGB Colour error!")
					else:
						try:
							self.KillLights()
						except:
							print ("No task running")
		except IndexError:
			print ("Var does not fit format")
		
		print ("********End POST********")
		print ("")

def run(server_class=HTTPServer, handler_class=S, port=666):
	global process
	try:
		server_address = ('', port)
		httpd = server_class(server_address, handler_class)
		print ('Starting Server...')
		httpd.serve_forever()
	except KeyboardInterrupt:
		print("Interrupt received, stopping...")
	finally:
		#os.kill(process.pid, signal.SIGINT)
		os.system('clear')
		print ("RIP Pi Lights")
		try:
			self.KillLights()
		except:
			print ("Failed to kill standard way btw...")
			motephat.clear()
			motephat.show()
		quit()
		sys.exit()

if __name__ == "__main__":
	 from sys import argv

	 if len(argv) == 2:
		  run(port=int(argv[1]))
	 else:
		  run()