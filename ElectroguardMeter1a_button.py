# invalid checksums for gain and configuration
# make sure configurations work
# 6 time EGuard button for system functions
# filenames from non-vol
# addition functions, clear
# make zip files
# what clock is used when
# check Flash drive mounted

#!/usr/bin/env python3
import os
import shutil
import subprocess
import json
from tkinter import *
import tkinter as tk
from queue import Queue
from threading import Thread
#from tkinter.font import Font
#from tkinter import messagebox
#import random
import gaugelib
import time
from datetime import date
from datetime import datetime
import spidev
import RPi.GPIO as GPIO
from smbus import SMBus
from os.path import exists
import zipfile

#global str SerNumber
bus1 = SMBus(1)
previousMin = 0
previousHours = 0
previousDay = 0
bus = 0
device = 0
spi = spidev.SpiDev()
spi.open(bus, device)
spi.max_speed_hz = 500000
spi.mode = 0
CE_ADC = 23
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
ADC_CS = 23
GPIO.setup(ADC_CS, GPIO.OUT, initial=GPIO.HIGH)
HEARTBEAT = 21
#global PIN21
PIN21 = 1
GPIO.setup(HEARTBEAT, GPIO.OUT, initial=GPIO.HIGH)
Avg_Cnt = 1
Avg_CH0 = 0
Avg_CH1 = 0
Avg_CH2 = 0
Avg_CH3 = 0
Max_CH0 = 0
Max_CH1 = 0
Max_CH2 = 0
Max_CH3 = 0
Min_CH0 = 5
Min_CH1 = 5
Min_CH2 = 5
Min_CH3 = 5
CH0_SafeCNT = 0
CH1_SafeCNT = 0
CH2_SafeCNT = 0
CH3_SafeCNT = 0
Max_mv2500 = 0
Min_mv2500 = 5
Max_V5REF = 0
Min_V5REF = 5
Max_M5VREF = -10
Min_M5VREF = 10
RmvUSB = 0
insert_usb = 0
repeat5 = 0

#various constants
ButtCol1 = "white"
ButtCol2 = "white"
ButtCol3 = "white"
ButtCol4 = "white"
choice = 1
MetalGroup = 2        #group 1
RedYell = -.050
YellGrn1 = 0
GrnRed2 = .25

label_vis = 0

win = tk.Tk()
#win.attributes('-fullscreen',True)
win.geometry("800x400+0+0")

def show_xtra_but():
    InitBut.config(text="ClearFile", padx=20, pady=15, fg="black", bg="#D0D1AB", activebackground="#D0D1AB", command=lambda: select(7))
    InitBut.place(x=690, y=15)
#     SerNumBut.config(text="SerNumb", padx=20, pady=15, fg="black", bg="#D0D1AB", activebackground="#D0D1AB", command=lambda: select(8))
    SerNumBut.config(text="SerNumb", padx=20, pady=15, fg="black", bg="#D0D1AB", activebackground="#D0D1AB", command=lambda: select(8))
    SerNumBut.place(x=690, y=75)

def clr_xtra_but():
    InitBut.config(text="", padx=0, pady=0, fg="black", bg="black", activebackground="black")
    InitBut.place(x=800, y=15)
    SerNumBut.config(text="", padx=0, pady=0, fg="black", bg="black", activebackground="black")
    SerNumBut.place(x=800, y=75)

def chk_usb():
    global mounted
    global childrn_str
    global sda_name
    # returns 0 to insert, 1 inserted not mounted, 2 ready to write
    USBcommand = "lsblk"
    lsblk_rtn = str(os.system(USBcommand))
    process = subprocess.run("lsblk --json -o NAME,MOUNTPOINT".split(), capture_output=True, text=True)    
    blockdevices = json.loads(process.stdout)
    blocknames = (blockdevices['blockdevices'])
    childrn = blocknames[0]['children']
    mounted = str((childrn[0]['mountpoint']))
    childrn_str = str(childrn)
    
    if(mounted == "/boot"):
        return 0                         #no usb
    if(mounted == "None"):       #usb is inserted and not mounted
        return 1
    else:       #usb is inserted and mounted
        childrn_str = str(childrn)                       #convert list to str
        loc1 = childrn_str.find("sda")                   #find sda1 or sda2
        sda_name = childrn_str[loc1:loc1+4]
        return 2


def bcd2bin(x):
  return (((x) & 0x0f) + ((x) >> 4) * 10)

def Num2BCD(number):    #number is the number you want to convert, num_digits is 2 for year, etc
    strNum = str(number)
    numb_cnt = len(strNum)
    if(numb_cnt > 1):
        BCDnumber = (int(strNum[0])*16)+int(strNum[1])
    else:
        BCDnumber = number
    return BCDnumber

def getRTCtime():
    RTCyear = bcd2bin(bus1.read_byte_data(0x6F, 0x06))
    RTCmonth = bcd2bin(bus1.read_byte_data(0x6F, 0x05) & 0x1F)
    RTCdate = bcd2bin(bus1.read_byte_data(0x6F, 0x04) & 0x3F)
    RTChour = bcd2bin(bus1.read_byte_data(0x6F, 0x02) & 0x3F)
    RTCminutes = bcd2bin (bus1.read_byte_data(0x6F, 0x01) & 0x7F)
#    print ("%02d:%02d:%02d:%02d:%02d" % (RTCyear, RTCmonth, RTCdate, RTChour, RTCminutes))
    if (len (str(RTCmonth)) == 1):
        RTCmonthB = "0"+str(RTCmonth)
    else:
        RTCmonthB = str(RTCmonth)
    if (len (str(RTCdate)) == 1):
        RTCdateB = "0"+str(RTCdate)
    else:
        RTCdateB = str(RTCdate)
    if (len (str(RTChour)) == 1):
        RTChourB = "0"+str(RTChour)
    else:
        RTChourB = str(RTChour)
    if (len (str(RTCminutes)) == 1):
        RTCminutesB = "0"+str(RTCminutes)
    else:
        RTCminutesB = str(RTCminutes)
    DateTime = "20"+(str(RTCyear)) + "-" + (str(RTCmonthB)) + "-" + (str(RTCdateB)) + " " + (str(RTChourB)) + ":" + (str(RTCminutesB)) 
    return DateTime

def BCD2Num(BCDnumber, num_digits):    #number is the number you want to convert, num_digits is 2 for year, etc
    print("BCD2Num BCD = ", BCDnumber)
    units = (BCDnumber & 0x000F)
    tens = (((BCDnumber & 0x00F0) >> 4) * 10)
    print("BCD2Num TENS = ", tens)
    print("BCD2Num units =", units)
    number = tens + units
    return number

def read_nvram():
    global ch1gain
    global ch2gain
    global ch3gain
    global ch4gain
    global ch1offset
    global ch2offset
    global ch3offset
    global ch4offset
    global sernum
    global chansel
    NVSerNum = ""
    
    #############Reading the file#########################
    file_exists = exists("/home/pi/Documents/ElectroguardPi/eguardsettings.txt")
    if(file_exists):
        with open("/home/pi/Documents/ElectroguardPi/eguardsettings.txt", "r") as cal:
            linecnt = 0
            for line in cal:
                linecnt = linecnt + 1
                if line.startswith("SerialNumber"):
                    begin = line.find(" ")
                    end = len(line)
                    sernum = line[begin+1:end-2]
                if line.startswith("chansel"):
                    begin = line.find(" ")
                    end = len(line)
                    chansel = int(line[begin+1:end])
                if line.startswith("SNCheckSum"):
                    begin = line.find(" ")
                    print("begin =", begin)
                    end = len(line)
                    print("end =", end)
                    SNcksum = int(line[begin+1:end])
                if line.startswith("CalCheckSum"):
                    begin = line.find(" ")
                    end = len(line)
                    CALcksum = int(line[begin+1:end])
                if line.startswith("ch1offset"):
                    begin = line.find(" ")
                    end = len(line)
                    ch1offset = int(line[begin+1:end])
                if line.startswith("ch1gain"):
                    begin = line.find(" ")
                    end = len(line)
                    ch1gain = int(line[begin+1:end])
                if line.startswith("ch2offset"):
                    begin = line.find(" ")
                    end = len(line)
                    ch2offset = int(line[begin+1:end])
                if line.startswith("ch2gain"):
                    begin = line.find(" ")
                    end = len(line)
                    ch2gain = int(line[begin+1:end])
                if line.startswith("ch3offset"):
                    begin = line.find(" ")
                    end = len(line)
                    ch3offset = int(line[begin+1:end])
                if line.startswith("ch3gain"):
                    begin = line.find(" ")
                    end = len(line)
                    ch3gain = int(line[begin+1:end])
                if line.startswith("ch4offset"):
                    begin = line.find(" ")
                    end = len(line)
                    ch4offset = int(line[begin+1:end])
                if line.startswith("ch4gain"):
                    begin = line.find(" ")
                    end = len(line)
                    ch4gain = int(line[begin+1:end])
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
    
    ################Reading RTC Clock###########################
    RTStatus = bus1.read_byte_data(0x6F, 0x03)
#    if((RTStatus & 0x20) == 0x20) && ((RTStatus & 0x08) == 0x08):
#        print("oscillator is running AND battery is enabled")
#    else:
#        print("RTC is disabled")
    RTyear = bus1.read_byte_data(0x6F, 0x06)
    RTmonth = bus1.read_byte_data(0x6F, 0x05)
    RTmonth = BCD2Num (RTmonth, 2)
    RTdate = bus1.read_byte_data(0x6F, 0x04)
    RTdate = BCD2Num (RTdate, 2)
    RThour = bus1.read_byte_data(0x6F, 0x02)
    RThour = BCD2Num ((RThour & 0x3F), 2)
    RTminutes = bus1.read_byte_data(0x6F, 0x01)
    RTminutes = BCD2Num (RTminutes, 2)
    RTseconds = bus1.read_byte_data(0x6F, 0x00)
    RTseconds = BCD2Num ((RTseconds & 0x7F), 2)

    print("ser_num = ", (NVSerNum))
    print("RTyear = ", RTyear)
    print("RTmonth = ", RTmonth)
    print("RTdate = ", RTdate)
    print("RThours = ", RThour)
    print("RTminutes = ", RTminutes)
    print("RTSec = ", RTseconds & 0x70)
    
###########Calibration Constants and Configuration##########
    RTchecksum = bus1.read_byte_data(0x6F, 0x20)
    RTchansel = bus1.read_byte_data(0x6F, 0x21)
    RTch1offset = bus1.read_byte_data(0x6F, 0x22)
    RTch2offset = bus1.read_byte_data(0x6F, 0x23)
    RTch3offset = bus1.read_byte_data(0x6F, 0x24)
    RTch4offset = bus1.read_byte_data(0x6F, 0x25)
    RTch1gain = bus1.read_byte_data(0x6F, 0x26)
    RTch2gain = bus1.read_byte_data(0x6F, 0x27)
    RTch3gain = bus1.read_byte_data(0x6F, 0x28)
    RTch4gain = bus1.read_byte_data(0x6F, 0x29)
    if(RTchecksum == ((RTchansel + RTch1offset + RTch2offset + RTch3offset + RTch4offset + RTch1gain + RTch2gain + RTch3gain + RTch4gain) & 0x00FF)):
#        file_exists = exists("/home/pi/Documents/ElectroguardPi/eguardsettings.txt")
#        if(file_exists):
#            with open("/home/pi/Documents/ElectroguardPi/eguardsettings.txt", "r") as cal:
        chansel = RTchansel
        ch1offset = RTch1offset
        ch1gain = RTch1gain
        ch2offset = RTch2offset
        ch2gain = RTch2gain
        ch3offset = RTch3offset
        ch3gain = RTch3gain
        ch4offset = RTch4offset
        ch4gain = RTch4gain
        
    ser_num_len = bus1.read_byte_data(0x6F, 0x30)
    if (ser_num_len > 12):
        ser_num_len = 12
    checksum2 = bus1.read_byte_data(0x6F, 0x31)
    sernumb_chksum = ser_num_len
    for x in range(0, ser_num_len):
        j = bus1.read_byte_data(0x6F, 0x32 + x)
#        print("j = ", chr(j))
        sernumb_chksum = j + sernumb_chksum
        NVSerNum = NVSerNum + chr(j)
    if (checksum2 == (sernumb_chksum & 0xFF)):
        sernumb = NVSerNum
    
#     if (checksum != (chansel+ch1offset+ch2offset+ch3offset+ch4offset+ch1gain+ch2gain+ch3gain+ch4gain) & 0x000000FF):
#         print("defaults")
#         ch1offset = 128
#         ch2offset = 128
#         ch3offset = 128
#         ch4offset = 128
#         ch1gain = 128
#         ch2gain = 128
#         ch3gain = 128
#         ch4gain = 128

def select(number):
    global choice
    global SelChan1
    global SelChan2
    global SelChan3
    global SelChan4
    prev_choice = choice
    prev_numb = number
    choice = number
    global label_vis
    global RmvUSB
    global repeat5
    global insert_usb
    
    print("prev_numb = ", prev_numb)
    print("number = ", number)
    if ((prev_numb == 5) and (number == 5)):
        repeat5 = repeat5 + 1
        print("repeat5 = ", repeat5)
    if ((prev_numb == 5) and (number == 5) and (repeat5 == 6)):
        show_xtra_but()
        
    if (repeat5 > 6):
        repeat5 = 0
        clr_xtra_but()
    
    if number == 1:
        SelChan1.config(bg="#00A0E3", activebackground="#00A0E3")
        SelChan2.config(bg="#D0D1AB", activebackground="#D0D1AB")
        SelChan3.config(bg="#D0D1AB", activebackground="#D0D1AB")
        SelChan4.config(bg="#D0D1AB", activebackground="#D0D1AB")
        return
        
    elif number == 2:
        SelChan2.config(bg="#00A0E3", activebackground="#00A0E3")
        SelChan1.config(bg="#D0D1AB", activebackground="#D0D1AB")
        SelChan3.config(bg="#D0D1AB", activebackground="#D0D1AB")
        SelChan4.config(bg="#D0D1AB", activebackground="#D0D1AB")
        return

    elif number == 3:
        SelChan3.config(bg="#00A0E3", activebackground="#00A0E3")
        SelChan2.config(bg="#D0D1AB", activebackground="#D0D1AB")
        SelChan1.config(bg="#D0D1AB", activebackground="#D0D1AB")
        SelChan4.config(bg="#D0D1AB", activebackground="#D0D1AB")
        return
        
    elif number == 4:
        SelChan4.config(bg="#00A0E3", activebackground="#00A0E3")
        SelChan2.config(bg="#D0D1AB", activebackground="#D0D1AB")
        SelChan3.config(bg="#D0D1AB", activebackground="#D0D1AB")
        SelChan1.config(bg="#D0D1AB", activebackground="#D0D1AB")
        return
        
    elif number == 5:
        RTCTime = getRTCtime()
        choice = prev_choice
        if(label_vis == 0):
            label_vis = 1
            label_2 = Label(win, text = "SerNum = " + SerNum + ", Time = " + RTCTime + ", Gain1 = "+ str(ch1gain) + ", Offset1 = " + str(ch1offset), font="Times 12", fg="white", bg = "black")
            label_1 = Label(win, text = "Electroguard Inc. 317 Deetz Rd #D, Mt Shasta, CA 96067, ph:530 926 4800 email:info@boatcorrosion.com", font="Times 12", fg="white", bg = "black")
        else:
       #     label_1.destroy()
            label_2 = Label(win, text = "SerNum = " + SerNum + ", Time = " + RTCTime + ", Gain1 = "+ str(ch1gain) + ", Offset1 = " + str(ch1offset), font="Times 12", fg="black", bg = "black")
            label_1 = Label(win, text = "Electroguard Inc. 317 Deetz Rd #D, Mt Shasta, CA 96067, ph:530 926 4800 email:info@boatcorrosion.com", font="Times 12", fg="black", bg = "black")
            label_vis = 0
        label_1.place(x=20, y=370)
        label_2.place(x=20, y=350)
        return

#        print("I'm at 5")
    elif number == 6:
        choice = prev_choice
        usbinserted = chk_usb()     #check to see if there is a usb inserted
        print("usbinserted = \n", usbinserted)
        
        dest = os.listdir("/media/pi/")
        print("listdir1 = ", dest)    
            
        if (usbinserted == 0):             #no usb is mounted
            insert_usb = 1
            SelSaveData.config(bg="yellow", padx=19, activebackground="yellow",  text="(re)Insert USB")

        if (usbinserted == 1):             #usb inserted, not mounted
            loc1 = childrn_str.find("sda")                   #find sda1 or sda2
            if (loc1 > 0):
                sda_name = childrn_str[loc1:loc1+4]
                cmd = "sudo mount /dev/" + sda_name + " /media/pi/" + dest[0]
                os.system(cmd)
                cmd = "sudo mkdir /media/pi/" + dest[0]
                os.system(cmd)
                usbinserted = 2           #if usbinserted==1 but no location

        if (usbinserted == 2):
            
            dest = os.listdir("/media/pi/")
            print("listdir3 = ", dest)
#            newname = str(SerNum)
            newname = str(sernum)
            Type = type(newname)
            print ("Serial Numb = ", newname)
            print("Type = ",Type)            
#first the big data file            
#            source = "/home/pi/Documents/ElectroguardPi/Electroguard.txt"
#            destination = "/home/pi/Documents/"
#            shutil.copy(source, destination)            #copy Electroguard.txt into /Documents
#            shutil.os.system('sudo cp "{}" "{}"'.format(source,destination))
#            destination = "/media/pi/dest"
            
#            print("dest", dest[loc1+1:loc2])
#           shutil.copy(source, destination)            #copy Electroguard.txt into /media/pi/+dest[0]
            
            RTCTime = getRTCtime()
            NewFileName =newname +"_" + RTCTime[0:10]
            NewFileNameZip = NewFileName + ".zip"
            shutil.copyfile("Electroguard.txt", NewFileName + ".txt")
            with zipfile.ZipFile(NewFileNameZip, "w", compression=zipfile.ZIP_DEFLATED) as newzip:
                newzip.write(NewFileName + ".txt")
            
#            os.rename("/home/pi/Documents/ElectroguardPi/Electroguard.zip", newname +"_" + RTCTime[0:10] +".zip")
#            os.rename("/home/pi/Documents/ElectroguardPi/Electroguard.zip", newname +"_" + RTCTime[0:10] +".zip")
#            os.rename("/home/pi/Documents/ElectroguardPi/Electroguard.txt", "/home/pi/Documents/test1.txt")
            source = "/home/pi/Documents/ElectroguardPi/" + NewFileNameZip
            destination = "/media/pi/" + dest[0]
            print("1 destination =", destination)
            print("1 source =", source)
            try:
                shutil.copy(source, destination)              #writes to Flash Memory
            except PermissionError:
                shutil.os.system('sudo cp "{}" "{}"'.format(source,destination))
            
#second the small data file
#            p = str(os.listdir('/home/pi/Documents/ElectroguardPi'))
            file_exists = exists('diags.txt')
            if (file_exists == True):
#            if (p.find('/home/pi/Documents/ElectroguardPi/diags.txt')>0):
#               source = "diags.txt"
#               destination = "/home/pi/Documents/"
#               shutil.copy(source, destination)            #copy Electroguard.txt into /Document
               with zipfile.ZipFile(NewFileName + "diags.zip", "w", compression=zipfile.ZIP_DEFLATED) as newzip:
                  newzip.write("diags.txt")
#               os.rename("/home/pi/Documents/diags.txt", "/home/pi/Documents/" + newname +"_diags_" + RTCTime[0:10] +".zip")
#               source = "/home/pi/Documents/"+ newname +"_diags_" + RTCTime[0:10] +".zip"
#               destination = "/media/pi/" + dest[0]
               SelSaveData.config(bg="orange", activebackground="orange",  text="Writing")
#               try:
#                   shutil.copy(source, destination)              #writes to Flash Memory
#               except PermissionError:
#                   shutil.os.system('sudo cp "{}" "{}"'.format(source,destination))
            
            os.system("sync")
            time.sleep(1)
#            SelSaveData.delete()
            SelSaveData.config(bg="yellow", padx = 19, activebackground="yellow",  text="Saving Data")
            loc1 = childrn_str.find("sda")                   #find sda1 or sda2
            sda_name = childrn_str[loc1:loc1+4]
            print("sda_name =  ", sda_name)    
            cmd = "sudo umount /dev/" + sda_name
            os.system(cmd)
            SelSaveData.config(bg="green", padx=19, activebackground="green",  text="Remove USB")
            RmvUSB = 1

    elif number == 7:
        choice = prev_choice
        p = str(os.listdir('/home/pi/Documents/ElectroguardPi'))
        print("listdir = ",p)
        if (p.find('Electroguard.txt')>0):
            os.remove("/home/pi/Documents/ElectroguardPi/Electroguard.txt")
        if (p.find('diags.txt')>0):
            os.remove("/home/pi/Documents/ElectroguardPi/diags.txt")
        repeat5 = 0
        clr_xtra_but()
        return
    
    elif number == 8:
        choice = prev_choice
        p = str(os.listdir('/home/pi/Documents/ElectroguardPi'))
        print("listdir = ",p)
        if (p.find('Electroguard.txt')>0):
            os.remove("/home/pi/Documents/ElectroguardPi/Electroguard.txt")
        repeat5 = 0
        clr_xtra_but()
        return
    else :
#        SelChan1.config(bg="green")
#        SelChan2.config(bg="white")
#        SelChan3.config(bg="white")
#        SelChan4.config(bg="white")
#        number = 1
        return


RTCTime = getRTCtime()
#os.system('sudo hwclock --set --date 2022-02-28')

#GET SERIALNUMBER FROM RTC
SerNumLen = int(bus1.read_byte_data(0x6F, 0x30))
if (SerNumLen >12):
    SerNumLen = 12
#SerNumber = ReadSerNum(SerNumLen)
checksum2 = int(bus1.read_byte_data(0x6F, 0x31))
checksum3 = SerNumLen
SerialNum = ""
for x in range (0, SerNumLen):
    a = (bus1.read_byte_data(0x6F, 0x32 + x))
    SerialNum = SerialNum + chr(a)
    checksum3 = checksum3 + a
if(checksum2 == (checksum3 & 0x00ff)):
    SerNum = SerialNum
else:
    SerNum = "00000000"
    BadCheckSum = 1
#print(SerialNum)
#print("SerNumber = ", SerNum)
# else:
#     SerNum = "NoSerNum"
# print("SerNumber = ", SerNum)
# CHECK FOR "/media/pi/flashdrive")
#dirdest = os.listdir("/media/pi/")
# if(dirdest.find("flashdrive") < 0):
#     cmd = "sudo mkdir /media/pi/flashdrive"
#     os.system(cmd)


#image
img2 = PhotoImage(file = "/home/pi/Documents/ElectroguardPi/EGuardLogoSm.PNG")
# win.create_image(550,300, anchor=NW, image=img2)


#button_0 = Button(win, text="Chan1", padx=40, pady=20, command=button_add)
#CH0Label.grid(row=0, column=0)
StatBut1 = Button(win, text="", padx=5, pady=1, fg="#00A0E3", bg="#00A0E3", activebackground="green")
StatBut1.place(x=550, y=29)
SelChan1 = Button(win, text="Channel 1", padx=20, pady=15, fg="black", bg="#00A0E3", activebackground="#00A0E3", command=lambda: select(1))
SelChan1.place(x=575, y=15)
StatBut2 = Button(win, text="", padx=5, pady=1, fg="black", bg="#00A0E3", activebackground="#00A0E3")
StatBut2.place(x=550, y=89)
SelChan2 = Button(win, text="Channel 2", padx=20, pady=15, fg="black", bg="#D0D1AB", activebackground="#D0D1AB", command=lambda: select(2))
SelChan2.place(x=575, y=75)
StatBut3 = Button(win, text="", padx=5, pady=1, fg="green", bg="green", activebackground="green")
StatBut3.place(x=550, y=149)
SelChan3 = Button(win, text="Channel 3", padx=20, pady=15, fg="black", bg="#D0D1AB", activebackground="#D0D1AB", command=lambda: select(3))
SelChan3.place(x=575, y=135)
StatBut4 = Button(win, text="", padx=5, pady=1, fg="green", bg="green", activebackground="green")
StatBut4.place(x=550, y=209)
SelChan4 = Button(win, text="Channel 4", padx=20, pady=15, fg="black", bg="#D0D1AB", activebackground="#D0D1AB", command=lambda: select(4))
SelChan4.place(x=575, y=195)
SelSaveData= Button(win, text="Save Data", padx=19, pady=15, fg="black", bg="#D0D1AB", activebackground="#D0D1AB", command=lambda: select(6))
SelSaveData.place(x=575, y=255)
SelEGuardButt = Button(win, image = img2, padx=15, pady=15, command=lambda: select(5))
SelEGuardButt.place(x=573, y=315)

InitBut = Button(win, text="", padx=0, pady=0, fg="black", bg="black", activebackground="black")  #, command=lambda: select(7))
InitBut.place(x=800, y=358)
SerNumBut = Button(win, text="", padx=0, pady=0, fg="black", bg="black", activebackground="black")  #, command=lambda: select(7))
SerNumBut.place(x=800, y=258)

a5 = PhotoImage(file="/home/pi/Documents/ElectroguardPi/g2.png")
win.tk.call('wm', 'iconphoto', win._w, a5)
win.title("Electroguard Raspberry Pi Version 2.0")
#win.geometry('zoomed')    #("800x400+0+0")
#win.resizable(width=True, height=True)
win.configure(bg='black')

#g_value=0
x=0

def get_adcs():
    global CH0
    global CH1
    global CH2
    global CH3
    global mv2500
    global V5REF
    global M5VREF
    global ButtCol1
    global ButtCol2
    global ButtCol3
    global ButtCol4
    global RmvUSB
    global insert_usb
    
    # CE goes low, conversion of CH0
    GPIO.output(ADC_CS,GPIO.LOW)
    msg = [0x06]
    msg.append(0x00)
    msg.append(0x00)
    CH0_raw = spi.xfer2(msg)
    GPIO.output(ADC_CS,GPIO.HIGH)
    time.sleep(0.001)
    CH0 = ((float)((((((CH0_raw[1] & 0x0F)<<8) + CH0_raw[2]) + (ch1offset - 128)) - 1365) * 7.5 / 4096))
    CH0 = CH0 * (ch1gain / 128)
    if (CH0 < RedYell):
        ButtCol1 = "red"
    elif ((CH0 >= RedYell) & (CH0 < YellGrn1)):
        ButtCol1 = "yellow"
    elif ((CH0 >= YellGrn1) & (CH0 < GrnRed2)):
        ButtCol1 = "green"
    elif (CH0 >= GrnRed2):
        ButtCol1 = "red"
    else:
        ButtCol1 = "green"
#    else:
#        ButtCol1 = "#00A0E3"
    StatBut1.config(bg=ButtCol1, activebackground=ButtCol1)
#    print("CH0 =", CH0)

# conversion of CH1
    GPIO.output(ADC_CS,GPIO.LOW)
    msg = [0x06]
    msg.append(0x40)
    msg.append(0x00)
    CH1_raw = spi.xfer2(msg)
    CH1 = ((float)((((((CH1_raw[1] & 0x0F)<<8) + CH1_raw[2]) + (ch2offset - 128)) - 1365) * 7.5 / 4096))
    #CH1 = ((float)((((CH1_raw[1] & 0x0F)<<8) + CH1_raw[2] - 1365) * 7.5 / 4096))
    CH1 = CH1 * ch2gain/128
    GPIO.output(ADC_CS,GPIO.HIGH)
#    if choice != 2:
    if (CH1 < RedYell):
        ButtCol2 = "red"
    elif ((CH1 >= RedYell) & (CH1 < YellGrn1)):
        ButtCol2 = "yellow"
    elif ((CH1 >= YellGrn1) & (CH1 < GrnRed2)):
        ButtCol2 = "green"
    elif (CH1 >= GrnRed2):
            ButtCol2 = "red"
    else:
        ButtCol2 = "#00A0E3"
    StatBut2.config(bg=ButtCol2, activebackground=ButtCol2)
    time.sleep(0.001)

# conversion of CH2
    GPIO.output(ADC_CS,GPIO.LOW)
    msg = [0x06]
    msg.append(0x80)
    msg.append(0x00)
    CH2_raw = spi.xfer2(msg)
    GPIO.output(ADC_CS,GPIO.HIGH)
    CH2 = ((float)((((((CH2_raw[1] & 0x0F)<<8) + CH2_raw[2]) + (ch3offset - 128)) - 1365) * 7.5 / 4096))
    CH2 = CH2 * (ch3gain / 128)
    if (CH2 < RedYell):
        ButtCol3 = "red"
    elif ((CH2 >= RedYell) & (CH2 < YellGrn1)):
        ButtCol3 = "yellow"
    elif ((CH2 >= YellGrn1) & (CH2 < GrnRed2)):
        ButtCol3 = "green"
    elif (CH2 >= GrnRed2):
            ButtCol3 = "red"
    else:
        ButtCol3 = "green"
#    else:
#       ButtCol3 = "#00A0E3"
    StatBut3.config(bg=ButtCol3, activebackground=ButtCol3)
    time.sleep(0.001)

# conversion of CH3
    GPIO.output(ADC_CS,GPIO.LOW)
    msg = [0x06]
    msg.append(0xC0)
    msg.append(0x00)
    CH3_raw = spi.xfer2(msg)
    GPIO.output(ADC_CS,GPIO.HIGH)
    CH3 = ((float)((((((CH3_raw[1] & 0x0F)<<8) + CH3_raw[2]) + (ch4offset - 128)) - 1365) * 7.5 / 4096))
    CH3 = CH3 * (ch4gain / 128)
    if (CH3 < RedYell):
        ButtCol4 = "red"
    elif ((CH3 >= RedYell) & (CH3 < YellGrn1)):
        ButtCol4 = "yellow"
    elif ((CH3 >= YellGrn1) & (CH3 < GrnRed2)):
        ButtCol4 = "green"
    elif (CH2 >= GrnRed2):
        ButtCol4 = "red"
    else:
        ButtCol4 = "green"
#    else:
#        ButtCol4 = "#00A0E3"
    
    StatBut4.config(bg=ButtCol4, activebackground=ButtCol4)
    time.sleep(0.001)
    

# conversion of 2.5V Ref
    GPIO.output(ADC_CS,GPIO.LOW)
    msg = [0x07]
    msg.append(0x00)
    msg.append(0x00)
    mv2500 = spi.xfer2(msg)
    GPIO.output(ADC_CS,GPIO.HIGH)
    mv2500 = ((float)((((mv2500[1] & 0x0F)<<8) + mv2500[2]) * 5 / 4096))
    time.sleep(0.001)

# conversion of +5V Ref / 2
    GPIO.output(ADC_CS,GPIO.LOW)
    msg = [0x07]
    msg.append(0x40)
    msg.append(0x00)
    V5_raw = spi.xfer2(msg)
    GPIO.output(ADC_CS,GPIO.HIGH)
    time.sleep(0.001)
    V5REF = ((float)((((V5_raw[1] & 0x0F)<<8) + V5_raw[2]) * 10 / 4096))
    
# conversion of -5V Ref
    GPIO.output(ADC_CS,GPIO.LOW)
    msg = [0x07]
    msg.append(0x80)
    msg.append(0x00)
    M5V_raw = spi.xfer2(msg)
    GPIO.output(ADC_CS,GPIO.HIGH)
    time.sleep(0.001)
    M5VREF = ((float)((((M5V_raw[1] & 0x0F)<<8) + M5V_raw[2] - 1365) * 7.5 / 4096))

# change color of RmvUSB button
    DEV_PRES = chk_usb()    
    if(DEV_PRES == 0):
       if (RmvUSB == 1):
           RmvUSB = 0
           print("change button color \n")
           SelSaveData.config(fg="black", bg="#D0D1AB", padx=19, activebackground="#D0D1AB",  text="Save Data")
    if((DEV_PRES == 1) and (insert_usb == 1)):
        insert_usb = 0;
        select(6)
    
#print("+5Vraw = ", (((V5_raw[1] & 0x0F)<<8) + V5_raw[2]))
#    print("CH0 = %3.3f, CH1 = %3.3f,  CH2 = %3.3f, CH3 = %3.3f, +5V = %3.3f,   2.5V = %3.3f   " % (CH0, CH1, CH2, CH3, V5REF, mv2500))
    time.sleep(1)

def read_every_second():
    global x
    global SigIN
    global previousMin
    global previousDay
    global RTCTime
    global previousHours
    global Avg_Cnt
    global Avg_CH0
    global Avg_CH1
    global Avg_CH2
    global Avg_CH3
    global Max_CH0
    global Max_CH1
    global Max_CH2
    global Max_CH3
    global Min_CH0
    global Min_CH1
    global Min_CH2
    global Min_CH3
    global CH0_SafeCNT
    global CH1_SafeCNT
    global CH2_SafeCNT
    global CH3_SafeCNT
    global Max_mv2500
    global Min_mv2500
    global Max_V5REF
    global Min_V5REF
    global Max_M5VREF
    global Min_M5VREF
    
    
    get_adcs()
    if choice == 1:
        SigIN = CH0
    elif choice == 2:
        SigIN = CH1
    elif choice == 3:
        SigIN = CH2
    elif choice == 4:
        SigIN = CH3
    else:
        SigIN = CH3
    p1.set_value(int(SigIN * 1000))   #SigIN is the selected signal to the meter
#    p1.set_value(int(SigIN))   #SigIN is the selected signal to the meter
    
    t = str(datetime.now())           #read the time
#    print('t = ', t)
    
    minutes = int(t[14:16])
    hours = int(t[11:13])
    day = hours
    
#    day = int(t[8:9])
    if (previousDay != day) :
        previousDay = day
        print("logging diags")
        fout = open('/home/pi/Documents/ElectroguardPi/diags.txt', 'a')
        fout.write(RTCTime + ","+ str(Avg_CH0/Avg_Cnt)[0:6] + "," + str(Avg_CH1/Avg_Cnt)[0:6] + "," + str(Avg_CH2/Avg_Cnt)[0:6] + "," + str(Avg_CH3/Avg_Cnt)[0:6] + ","\
            + str(Max_CH0)[0:6] + "," + str(Max_CH1)[0:6] + "," + str(Max_CH2)[0:6] + ","  + str(Max_CH3)[0:6] + ","\
            + str(Min_CH0)[0:6] + "," + str(Min_CH1)[0:6] + "," + str(Min_CH2)[0:6] + ","  + str(Min_CH3)[0:6] + ","\
            + str(CH0_SafeCNT/Avg_Cnt)[0:6]  +"," + str(CH1_SafeCNT/Avg_Cnt)[0:6]  + "," + str(CH2_SafeCNT/Avg_Cnt)[0:6]  + "," + str(CH3_SafeCNT/Avg_Cnt)[0:6] + ","\
            + str(Max_mv2500)[0:6] + "," + str(Min_mv2500)[0:6] + "," + str(Max_V5REF)[0:6] + "," + str(Min_V5REF)[0:6] + ","\
            + str(Max_M5VREF)[0:6] + "," + str(Min_M5VREF)[0:6] +"\n")
        fout.close()
        Avg_Cnt = 0
        Avg_CH0 = 0
        Avg_CH1 = 0
        Avg_CH2 = 0
        Avg_CH3 = 0
        Max_CH0 = 0
        Max_CH1 = 0
        Max_CH2 = 0
        Max_CH3 = 0
        Min_CH0 = 5
        Min_CH1 = 5
        Min_CH2 = 5
        Min_CH3 = 5
        CH0_SafeCNT = 0
        CH1_SafeCNT = 0
        CH2_SafeCNT = 0
        CH3_SafeCNT = 0
        
        Max_mv2500 = 0
        Min_mv2500 = 5
        Max_V5REF = 0
        Min_V5REF = 5
        Max_M5VREF = -10
        Min_M5VREF = +10
        
        
    if (previousMin != minutes) :
        previousMin = minutes
        RTCTime = getRTCtime()
        Avg_Cnt = Avg_Cnt + 1
        Avg_CH0 = Avg_CH0 + CH0
        Avg_CH1 = Avg_CH1 + CH1
        Avg_CH2 = Avg_CH2 + CH2
        Avg_CH3 = Avg_CH3 + CH3
        if(Max_CH0 < CH0):
            Max_CH0 = CH0
        print("CH0= ", CH0)
        print("Max_CH0= ", Max_CH0)
        if(Max_CH1 < CH1):
            Max_CH1 = CH1
        if(Max_CH2 < CH2):
            Max_CH2 = CH2
        if(Max_CH3 < CH3):
            Max_CH3 = CH3
        if(Min_CH0 > CH0):
            Min_CH0 = CH0
        if(Min_CH1 > CH1):
            Min_CH1 = CH1
        if(Min_CH2 > CH2):
            Min_CH2 = CH2
        if(Min_CH3 > CH3):
            Min_CH3 = CH3
        if(Max_mv2500 < mv2500):
            Max_mv2500 = mv2500
        if(Min_mv2500 > mv2500):
            Min_mv2500 = mv2500
        if(Max_V5REF < V5REF):
            Max_V5REF = V5REF
        if(Min_V5REF > V5REF):
            Min_V5REF = V5REF
        if(Max_M5VREF < M5VREF):
            Max_M5VREF = M5VREF
        if(Min_M5VREF> M5VREF):
            Min_M5VREF = M5VREF
        
        if(ButtCol1 == "green"):
            CH0_SafeCNT = CH0_SafeCNT +1
        if(ButtCol2 == "green"):
            CH1_SafeCNT = CH1_SafeCNT +1
        if(ButtCol3 == "green"):
            CH2_SafeCNT = CH2_SafeCNT +1   
        if(ButtCol4 == "green"):
            CH3_SafeCNT = CH3_SafeCNT +1           
            
        print("day = ",day)
        print("Prev day = ",previousDay)
        print("Avg_Cnt = ",Avg_Cnt)
        print("Avg_CH0 = ",Avg_CH0)
        print("Max_CH0 = ",Max_CH0)
        print("Min_CH0 = ",Min_CH0)
            
#        print (RTCTime)
        print("logging")
        fout = open('/home/pi/Documents/ElectroguardPi/Electroguard.txt', 'a')
        if ((chansel & 0x0F) == 0x01):
            fout.write(RTCTime + ","+ str(CH0)[0:6] + "\n")
        elif ((chansel & 0x0F) == 0x02):
            fout.write(RTCTime + ","+ str(CH1)[0:6] + "\n")
        elif ((chansel & 0x0F) == 0x03):
            fout.write(RTCTime + "," + str(CH0)[0:6] + "," + str(CH1)[0:6] + "\n")
        elif ((chansel & 0x0F) == 0x04):
            fout.write(RTCTime + ","+ str(CH2)[0:6] + "\n")
        elif ((chansel & 0x0F) == 0x05):
            fout.write(RTCTime + "," + str(CH0)[0:6] + "," + str(CH2)[0:6] + "\n")
        elif ((chansel & 0x0F) == 0x06):
            fout.write(RTCTime + "," + str(CH1)[0:6] + "," + str(CH2)[0:6] + "\n")
        elif ((chansel & 0x0F) == 0x07):
            fout.write(RTCTime + "," + str(CH0)[0:6] + "," + str(CH1)[0:6] + "," + str(CH2)[0:6] + "\n")
        elif ((chansel & 0x0F) == 0x08):
            fout.write(RTCTime + ","+ str(CH4)[0:6] + "\n")
        elif ((chansel & 0x0F) == 0x09):
            fout.write(RTCTime + "," + str(CH0)[0:6] + "," + str(CH3)[0:6] + "\n") 
        elif ((chansel & 0x0F) == 0x0A):
            fout.write(RTCTime + "," + str(CH1)[0:6] + "," + str(CH3)[0:6] + "\n")
        elif ((chansel & 0x0F) == 0x0B):
            fout.write(RTCTime + "," + str(CH0)[0:6] + "," + str(CH1)[0:6] + "," + str(CH3)[0:6] + "\n")
        elif ((chansel & 0x0F) == 0x0C):
            fout.write(RTCTime + "," + str(CH2)[0:6] + "," + str(CH3)[0:6] + "\n")
        elif ((chansel & 0x0F) == 0x0D):
            fout.write(RTCTime + "," + str(CH0)[0:6] + "," + str(CH2)[0:6] + "," + str(CH3)[0:6] + "\n")
        elif ((chansel & 0x0F) == 0x0E):
            fout.write(RTCTime + "," + str(CH0)[0:6] + "," + str(CH2)[0:6] + "," + str(CH3)[0:6] + "\n")        
        elif ((chansel & 0x0F) == 0x0F):
            fout.write(RTCTime + ","+ str(CH0)[0:6] + "," + str(CH1)[0:6] + "," + str(CH2)[0:6] + "," + str(CH3)[0:6] + "\n")
        else:
            fout.write(RTCTime + ","+ str(CH0)[0:6] + "\n")
        print("CH0 = %3.3f, CH1 = %3.3f,  CH2 = %3.3f, CH3 = %3.3f" % (CH0, CH1, CH2, CH3))
        fout.close()
    
    PIN21 = GPIO.input(HEARTBEAT)
    if PIN21 > 0:
        GPIO.output(HEARTBEAT,GPIO.LOW)
        PIN21 = 0
    else:
        GPIO.output(HEARTBEAT,GPIO.HIGH)
        PIN21 = 1

    win.after(400, read_every_second)
    
read_nvram()
p1 = gaugelib.DrawGauge2(
    win,
    max_value=425.0,     #myee
    min_value=-147.0,    #myee
    size=500,
    bg_col='black',
    unit = "Volts",bg_sel = 2)
p1.place(x=40, y=25)
#p1.pack(side=RIGHT)

read_every_second()
mainloop()