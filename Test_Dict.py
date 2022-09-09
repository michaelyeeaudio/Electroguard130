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


#a = os.path.isdir("/media/pi")
#print(a)
process = subprocess.run("lsblk --json -o NAME,MOUNTPOINT".split(), capture_output=True, text=True)    
blockdevices = json.loads(process.stdout)
#sda_dict = {'blockdevices': [{'name': 'sda', 'children': [{'name': 'sda1'}]}, {'name': 'mmcblk0', 'children': [{'name': 'mmcblk0p1'}, {'name': 'mmcblk0p2'}]}]}
print(blockdevices)
print(type(blockdevices))
name_blockdevices = blockdevices['blockdevices']
print(name_blockdevices)
print(blockdevices['children'][0])


list_blkdev = blockdevices['blockdevices']
#print(type(list_blkdev))
#print(list_blkdev)
for query_names in list_blkdev:
    print(query_names)
#dict_sda = list_blkdev['name']
print(type(query_names))


#print(sda_dict['blockdevices'][0])
#print(sda_dict['blockdevices'][0]['name'])