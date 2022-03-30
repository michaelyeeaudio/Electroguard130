#CheckUSB.py:
#   - looks for USB drive

import os
import subprocess
d = os.listdir("/home/pi/Documents")
#print(d)
rpistr = "ls /media/pi > usbs.txt"
p=subprocess.Popen(rpistr,shell=True, preexec_fn=os.setsid)
#print(rpistr)
USBdir = open('usbs.txt', 'r')
print(str(USBdir))