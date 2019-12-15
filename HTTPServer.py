#!/usr/bin/env python
"""
Very simple HTTP server in python.
Usage:
	 ./HTTPserver.py [<port>]
Test
"""

if True: #Need a way of checking this...
	RGBW = "" #Makes all files 'FileName'
else:
	RGBW = "W" #Makes all files 'FileNameW'

#Investigate why it tries to kill and once it can't then runs the app, strange...

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import sys
import motephat
import time
import subprocess
import os
import signal
import re

global Dataz,process, MoteApp, MoteAppLoc, R, G, B, R2, G2, B2 #We need to make them global variables so they can be read inside the function.
process = ""
MoteApp = ""
MoteAppLoc = "/home/pi/bin/Python/MoteScripts/"
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
		global process
		if process == "": #Because it is set as a string above to stop NameError (Calling before defined)
			print ("PiLights are not running...")
			return
		else:
			print ("PILights are running... Killing...")
			process.terminate()
			process.kill()
			motephat.clear()
			motephat.show()
			process = subprocess.call(["python3.4", "/home/pi/bin/Python/MoteScripts/moteOff.py"])
			process = ""
			return
	
	def hex_to_rgb(self,value): #This will be handled this side instead going forward
		value = value.lstrip('#')
		length = len(value)
		return tuple(int(value[i:i + length / 3], 16) for i in range(0, length, length / 3))

	def do_GET(self):
		print ("********Start GET********") #Get whole list and filter through on their side or ours?
		self._set_headers()
		print ("Var(s) Requested: ",self.path[1:])
		VarReq = self.path[1:]
		try:
			if self.path == ("/jives.html") or self.path == ("/Jives.html") or self.path == ("/arnold.html") or self.path == ("/Arnold.html"): 
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
					if re.match("On", VarValue) or re.match("On\.\d{0,2}", VarValue):
						print ("PILights ",VarValue)
						#print (x," Matched the regex")
						self.KillLights()
						if (RGBW == "W"):
							Brightness = SepDataz.split(".")
							Brightness = float(Brightness[1])/10 #Receives brightness 1-10
							print ("Brightness: " ,Brightness)
							process = subprocess.call(["python3.4", "/home/pi/bin/Python/MoteScripts/moteOnW.py",str(Brightness)]) #Must be passed as string
							#MoteApp = "'moteOn{0}.py',{1}'".format(RGBW,str(Brightness)) #Brightness Must be passed as string #Test this...
						else:
							#MoteApp = "moteOn{0}.py".format(RGBW)
							process = subprocess.Popen(["python3.4", "/home/pi/bin/Python/MoteScripts/moteOn.py"])
						self.wfile.write(("PiLights ",VarValue)) #Send reply
					elif VarValue == "Off":
						self.KillLights()
					elif VarValue == "Rainbow":
						self.KillLights()
						print ("PILights ",VarValue)
						process = subprocess.Popen(["python3.4", "/home/pi/bin/Python/MoteScripts/rainbow.py"])
						self.wfile.write(("PiLights ",VarValue)) #Send reply
					elif VarValue == "Bilge":
						self.KillLights()
						print ("PILights ",VarValue)
						process = subprocess.Popen(["python3.4", "/home/pi/bin/Python/MoteScripts/bilgetank.py"])
						self.wfile.write(("PiLights ",VarValue)) #Send reply
					elif VarValue == "Hell":
						self.KillLights()
						print ("PILights ",VarValue)
						process = subprocess.Popen(["python3.4", "/home/pi/bin/Python/MoteScripts/helltank.py"])
						self.wfile.write(("PiLights ",VarValue)) #Send reply
					elif VarValue.startswith('ManFade'):
						self.KillLights()
						try:
							Colours = SepDataz.split(".")
							print (Colours)
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
								process = subprocess.Popen(["python3.4", "/home/pi/bin/Python/MoteScripts/moteFade.py",R,G,B,R2,G2,B2])
								self.wfile.write(("PiLights ","Switch ",R2," ",G2," ",B2, " x ", R," ",G," ",B)) #Send reply
							else:
								R = Colours[1]
								G = Colours[2]
								B = Colours[3]
								R2 = Colours[4]
								G2 = Colours[5]
								B2 = Colours[6]
								process = subprocess.Popen(["python3.4", "/home/pi/bin/Python/MoteScripts/moteFade.py",R,G,B,R2,G2,B2])
								self.wfile.write(("PiLights ",VarValue," ",R," ",G," ",B," x ",R2," ",G2," ",B2)) #Send reply
						except:
							print ("RGB Colour error!")
					elif VarValue.startswith('Man'): #Add regex here
						try:
							Colours = SepDataz.split(".")
							print (Colours)
							self.KillLights()
							print ("PILights ",VarValue)
							R = Colours[1]
							G = Colours[2]
							B = Colours[3]
							process = subprocess.Popen(["python3.4", "/home/pi/bin/Python/MoteScripts/manualSet.py",R,G,B])
							self.wfile.write(("PiLights ",VarValue," ",R," ",G," ",B)) #Send reply
						except:
							print ("RGB Colour error!")
					else:
						print ("Command Unknown")
						self.wfile.write(("PiLights Command Unknown!"))
		except IndexError:
			print ("Var does not fit format")
		print ("********End POST********")
		print ("")

def run(server_class=HTTPServer, handler_class=S, port=666):
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
		os.system('clear')
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