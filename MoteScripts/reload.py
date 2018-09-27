import os
import time
import sys
from subprocess import call

'''
if len(argv) == 2:
    PID = int(argv[1])
    print ("PID:",PID)
    result = None
    while result is None:
        try:
            os.kill(pid, 0)
            result = get_data(...)
        except:
            pass
    
else:
    print ("Not enough arguments!")
    '''
#os.system("pkill python &")
time.sleep(0.1)
#pid=os.fork()
#if pid==0: # new process
print ("Starting PiLights again...")
call(["python", "/home/pi/bin/Python/HTTPServer.py","666",">","/home/pi/bin/Python/Logs/httpserver.log"])
    #os.system("python /home/pi/bin/Python/HTTPServer.py 666 > /home/pi/bin/Python/Logs/httpserver.log")
print ("Started PiLights")
quit()
sys.exit()
    #exit()