#TimeSerNum2.py:
#   - looks at current time
#   - Checks to see if date/time is correct
#   - if not, enters date/time, programs date/time

from smbus import SMBus
import time
from datetime import date
from datetime import datetime
from os.path import exists
import os

CalList = ["SerialNumber", "chansel", "SNCheckSum", "CalCheckSum", "ch1offset", "ch1gain","ch2offset", "ch2gain","ch3offset", "ch3gain","ch4offset", "ch4gain"]

file_exists = exists("/home/pi/Documents/ElectroguardPi/eguardsettings.txt")
if(file_exists):
    with open("/home/pi/Documents/ElectroguardPi/eguardsettings.txt", "r") as cal:
        linecnt = 0
        for line in cal:
            linecnt = linecnt + 1
            if line.startswith("SerialNumber"):
                begin = line.find(" ")
                end = len(line)
                sernum = line[begin+1:end]
            if line.startswith("chansel"):
                begin = line.find(" ")
                end = len(line)
                chansel = line[begin+1:end]
            if line.startswith("SNCheckSum"):
                begin = line.find(" ")
                print("begin =", begin)
                end = len(line)
                print("end =", end)
                SNcksum = line[begin+1:end]
            if line.startswith("CalCheckSum"):
                begin = line.find(" ")
                end = len(line)
                CALcksum = line[begin+1:end]
            if line.startswith("ch1offset"):
                begin = line.find(" ")
                end = len(line)
                ch1offset = line[begin+1:end]
            if line.startswith("ch1gain"):
                begin = line.find(" ")
                end = len(line)
                ch1gain = line[begin+1:end]
            if line.startswith("ch2offset"):
                begin = line.find(" ")
                end = len(line)
                ch2offset = line[begin+1:end]
            if line.startswith("ch2gain"):
                begin = line.find(" ")
                end = len(line)
                ch2gain = line[begin+1:end]
            if line.startswith("ch3offset"):
                begin = line.find(" ")
                end = len(line)
                ch3offset = line[begin+1:end]
            if line.startswith("ch3gain"):
                begin = line.find(" ")
                end = len(line)
                ch3gain = line[begin+1:end]
            if line.startswith("ch4offset"):
                begin = line.find(" ")
                end = len(line)
                ch4offset = line[begin+1:end]
            if line.startswith("ch4gain"):
                begin = line.find(" ")
                end = len(line)
                ch4gain = line[begin+1:end]

                
    print("sernum =", sernum)
    print("chansel =", chansel)
    print("SNcksum =", SNcksum)
    print("CALcksum =", CALcksum)
    print("ch1offset =", ch1offset)
    print("ch1gain =", ch1gain)
    print("ch2offset =", ch2offset)
    print("ch2gain =", ch2gain)
    print("ch3offset =", ch3offset)
    print("ch3gain =", ch3gain)
    print("ch4offset =", ch4offset)
    print("ch4gain =", ch4gain)
