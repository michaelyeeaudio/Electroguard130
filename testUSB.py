#!/usr/bin/env python3
import os
import shutil
import subprocess
import json
from tkinter import *
import tkinter as tk
from queue import Queue
from threading import Thread
import time
from datetime import date
from datetime import datetime

def chk_usb():
    # returns 0 to insert, 1 to re-insert, 2 ready to write
#    command = "lsblk -f --json | grep sd"
#    command = "lsblk -f --json"
#    USBcommand = "lsblk -f | grep sda"
#    lsblk_rtn = os.system(command)
#    print("data type = ", lsblk_rtn)
#    print("ls -d = ",lsblk_rtn)
#    USBcommand = "lsblk"
    process = subprocess.run("lsblk --json -o NAME".split(), capture_output=True, text=True)    
    blockdevices = json.loads(process.stdout)
    print(blockdevices)
    str_block = str(blockdevices)
    print("str_block = \n", str_block)
    loc_sd0 = str_block.find("'children': [{'name':")
    print("loc_sd0 = ", loc_sd0)
    SDx = str_block[loc_sd0 + 23 : loc_sd0 + 27]
    print("SDx = ", SDx)
    print("\n")
    print("SDx type =", type(SDx))
    pos = str_block.find("sd") 
    if(str_block.find("sd") == 0):
        return 0                         #no usb
    if(str_block.find("sd") > 0):       #usb is inserted
        if(str_block.find("/media/pi/") > 0):    #usb is mounted
            return 2
        else:
            dest = str(os.listdir("/media/pi/"))
            print("chk usb dest = ", dest)
            print("type of dest = ", type(dest))
            loc1 = dest.find('[')
            loc2 = dest.find(']')
            USBcommand = "ls -d */"
            lsblk_rtn = str(os.system(USBcommand))
            print("ls -d = ",lsblk_rtn)
            b = "sudo mkdir /media/pi/"+ dest[loc1+2:loc2-1]
            print ("b0 = ", b)
            b = 'sudo mount /dev/'+ SDx    # ' /media/pi/'    #+ dest[loc1+2:loc2-1]
            print ("b1 = ", b)
            b = b + ' /media/pi/'
            print ("b3 = ", b)
            b = b + dest[loc1+2:loc2-1]
            print ("b4 = ", b)
#            cmd = '"%s"'% (b)
            cmd = b
            print ("cmd = ", cmd)
            os.system(cmd)
#            os.system("sudo mount /dev/sda1 /media/pi/usb")
            return 2
#         if (len(dest) > 0):             #usb is inserted
#             if(str_block.find("sda") > 1):                 #usb is inserted and mounted
#                 return 2
#         if (len(dest) == 0):             #not mounted
#             cmd = "sudo mkdir /media/pi/ + dest"
#             os.system(cmd)
#             cmd = "sudo mount /dev/sda1 /media/pi/ + dest"
#             os.system(cmd)   
#             return 2
#         else:
#             return 2
    else:
         return 0
    
a = chk_usb()
print("a = ", a)