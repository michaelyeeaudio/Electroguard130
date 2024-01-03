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

#global str SerNumber
bus1 = SMBus(1)
previousMin = 0
previousHours = 0
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

#various constants
ButtCol1 = "white"
ButtCol2 = "white"
ButtCol3 = "white"
ButtCol4 = "white"
choice = 1
MetalGroup = 1        #group 1
RedYell1 = 0
YellGrn1 = .4
GrnYell2 = .55
YellRed2 = .55
label_vis = 0

win = tk.Tk()
#win.attributes('-fullscreen',True)
win.geometry("800x400+0+0")

def chk_usb():
    USBcommand = "lsblk"
    process = subprocess.run("lsblk --json -o NAME".split(), capture_output=True, text=True)    
    blockdevices = json.loads(process.stdout)
    str_block = str(blockdevices)
    print("str_block = \n", str_block)
    if(str_block.find("sda") > 0):
        dest = os.listdir("/media/pi/")
        print("chk usb dest = \n", dest)
        if (len(dest) == 0):             #no usb is mounted
#             cmd = "sudo mkdir /media/pi/usb"
#             os.system(cmd)
#             cmd = "sudo mount /dev/sda1 /media/pi/usb"
#             os.system(cmd)   
            return 1
    else:
        return 0

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

def read_nvram():
    global ch1gain
    global ch2gain
    global ch3gain
    global ch4gain
    global ch1offset
    global ch2offset
    global ch3offset
    global ch4offset
    checksum = bus1.read_byte_data(0x6F, 0x20)
    chansel = bus1.read_byte_data(0x6F, 0x21)
    ch1offset = bus1.read_byte_data(0x6F, 0x22)
    ch2offset = bus1.read_byte_data(0x6F, 0x23)
    print("prev ch2offset =", ch2offset)
    ch3offset = bus1.read_byte_data(0x6F, 0x24)
    ch4offset = bus1.read_byte_data(0x6F, 0x25)
    ch1gain = bus1.read_byte_data(0x6F, 0x26)
    ch2gain = bus1.read_byte_data(0x6F, 0x27)
    print("prev ch2gain =", ch2gain)
    ch3gain = bus1.read_byte_data(0x6F, 0x28)
    ch4gain = bus1.read_byte_data(0x6F, 0x29)
    if (checksum != (chansel+ch1offset+ch2offset+ch3offset+ch4offset+ch1gain+ch2gain+ch3gain+ch4gain) & 0x000000FF):
        print("defaults")
        ch1offset = 128
        ch2offset = 128
        ch3offset = 128
        ch4offset = 128
        ch1gain = 128
        ch2gain = 128
        ch3gain = 128
        ch4gain = 128

def select(number):
    global choice
    global SelChan1
    global SelChan2
    global SelChan3
    global SelChan4
    choice = number
    global label_vis
    
    if number == 1:
        SelChan1.config(bg="#D9D9D6", activebackground="#D9D9D6")
        SelChan2.config(bg="#D9D9D6", activebackground="#D9D9D6")
        SelChan3.config(bg="#D9D9D6", activebackground="#D9D9D6")
        SelChan4.config(bg="#D9D9D6", activebackground="#D9D9D6")
        return
        
    elif number == 2:
        SelChan2.config(bg="#D9D9D6", activebackground="#D9D9D6")
        SelChan1.config(bg="#D9D9D6", activebackground="#D9D9D6")
        SelChan3.config(bg="#D9D9D6", activebackground="#D9D9D6")
        SelChan4.config(bg="#D9D9D6", activebackground="#D9D9D6")
        return

    elif number == 3:
        SelChan3.config(bg="#D9D9D6", activebackground="#D9D9D6")
        SelChan2.config(bg="#D9D9D6", activebackground="#D9D9D6")
        SelChan1.config(bg="#D9D9D6", activebackground="#D9D9D6")
        SelChan4.config(bg="#D9D9D6", activebackground="#D9D9D6")
        return
        
    elif number == 4:
        SelChan4.config(bg="#D9D9D6", activebackground="#D9D9D6")
        SelChan2.config(bg="#D9D9D6", activebackground="#D9D9D6")
        SelChan3.config(bg="#D9D9D6", activebackground="#D9D9D6")
        SelChan1.config(bg="#D9D9D6", activebackground="#D9D9D6")
        return
        
    elif number == 5:
        if(label_vis == 0):
            label_vis = 1
            label_1 = Label(win, text = "Electroguard Inc. 317 Deetz Rd #D, Mt Shasta, CA 96067, ph:530 926 4800 email:info@boatcorrosion.com", font="Times 12", fg="white", bg = "black")
        else:
       #     label_1.destroy()
            label_1 = Label(win, text = "Electroguard Inc. 317 Deetz Rd #D, Mt Shasta, CA 96067, ph:530 926 4800 email:info@boatcorrosion.com", font="Times 12", fg="black", bg = "black")
            label_vis = 0
        label_1.place(x=20, y=370)
        return

#        print("I'm at 5")
    elif number == 6:
        source = "/home/pi/Documents/ElectroguardPi/Electroguard.txt"
        destination = "/home/pi/Documents/"         
    #    destination = "/media/pi/"+dest[1]
        shutil.copy(source, destination)            #copy Electroguard.txt into /Documents
   #    usbinserted = chk_usb()     #check to see if there is a usb inserted
   #     print("usbinserted = \n", usbinserted) 
   
   #if (usbinserted == 0):
        dest = os.listdir("/media/pi/")
        if (len(dest) == 0):             #no usb is mounted
            print("no usb mounted")
            print("re-insert usb")
            SelSaveData.config(bg="yellow", activebackground="yellow",  text="(re)Insert USB")
        else:      
            dest = str(os.listdir("/media/pi/"))
            loc1 = dest.find('[')
            loc2 = dest.find(']')
            print("loc1 = ", loc1)
            print("loc2 = ", loc2)
            newname = SerNum
            
            source = "/home/pi/Documents/ElectroguardPi/Electroguard.txt"
            destination = "/home/pi/Documents/"
            shutil.copy(source, destination)            #copy Electroguard.txt into /Documents
#            destination = "/media/pi/dest"
            
            print("dest", dest[loc1+1:loc2])
#           shutil.copy(source, destination)            #copy Electroguard.txt into /media/pi/+dest[0]
            RTCTime = getRTCtime()
            os.rename("/home/pi/Documents/Electroguard.txt", "/home/pi/Documents/" + newname +"_" + RTCTime[0:10] +".txt")
            source = "/home/pi/Documents/"+ newname +"_" + RTCTime[0:10] +".txt"
            destination = "/media/pi/" + dest[loc1+2:loc2-1]
            print("1 destination =", destination)
            print("1 source =", source)
            SelSaveData.config(bg="orange", activebackground="orange",  text="Writing")
#            shutil.copy(source, destination)              #writes to Flash Memory
#            os.system("cp /home/pi/Documents/ElectroguardPi/Electroguard.txt /home/pi/dest")
#            os.system("cp source /media/pi/dest")
            shutil.copy(source, destination)              #writes to Flash Memory
            os.system("sync")
            time.sleep(5)
            SelSaveData.config(bg="yellow", activebackground="yellow",  text="Saving Data")
                
            cmd = "sudo umount /dev/sda1"
            os.system(cmd)
            SelSaveData.config(bg="green", padx=15, activebackground="green",  text="Remove USB")
                 
    else :
#        SelChan1.config(bg="green")
#        SelChan2.config(bg="white")
#        SelChan3.config(bg="white")
#        SelChan4.config(bg="white")
#        number = 1
        return

# def ReadSerNum(SerNumLen):
#     SerNum
#     SerialNum
#     checksum2 = int(bus1.read_byte_data(0x6F, 0x31))
#     checksum3 = 0
#     for x in range (0, SerNumLen):
#         a = (bus1.read_byte_data(0x6F, 0x31 + x))
#         SerialNum[x] = str(a)
#         checksum3 = checksum3 + a
#     if(checksum2 == checksum3):
#         SerNum = SerialNum
#     else:
#         SerNum = "NoSerNum"
#     return SerNum
# get and set the Pi clock
RTCTime = getRTCtime()
#os.system('sudo hwclock --set --date 2022-02-28')

#GET SERIALNUMBER FROM RTC
SerNumLen = int(bus1.read_byte_data(0x6F, 0x30))
#SerNumber = ReadSerNum(SerNumLen)
checksum2 = int(bus1.read_byte_data(0x6F, 0x31))
checksum3 = 0
SerialNum = ""
for x in range (0, SerNumLen):
    a = (bus1.read_byte_data(0x6F, 0x32 + x))
    SerialNum = SerialNum + chr(a)
    checksum3 = checksum3 + a
if(checksum2 == (checksum3 & 0x00ff)):
    SerNum = SerialNum
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
StatBut1 = Button(win, text="", padx=5, pady=1, fg="light blue", bg="light blue", activebackground="green")
StatBut1.place(x=600, y=29)
SelChan1 = Button(win, text="Channel 1", padx=20, pady=15, fg="black", bg="#D9D9D6", activebackground="#D9D9D6", command=lambda: select(1))
SelChan1.place(x=625, y=15)
StatBut2 = Button(win, text="", padx=5, pady=1, fg="green", bg="green", activebackground="green")
StatBut2.place(x=600, y=89)
SelChan2 = Button(win, text="Channel 2", padx=20, pady=15, fg="black", bg="#D9D9D6", activebackground="#D9D9D6", command=lambda: select(2))
SelChan2.place(x=625, y=75)
StatBut3 = Button(win, text="", padx=5, pady=1, fg="green", bg="green", activebackground="green")
StatBut3.place(x=600, y=149)
SelChan3 = Button(win, text="Channel 3", padx=20, pady=15, fg="black", bg="#D9D9D6", activebackground="#D9D9D6", command=lambda: select(3))
SelChan3.place(x=625, y=135)
StatBut4 = Button(win, text="", padx=5, pady=1, fg="green", bg="green", activebackground="green")
StatBut4.place(x=600, y=209)
SelChan4 = Button(win, text="Channel 4", padx=20, pady=15, fg="black", bg="#D9D9D6", activebackground="#D9D9D6", command=lambda: select(4))
SelChan4.place(x=625, y=195)
SelSaveData= Button(win, text="Save Data", padx=19, pady=15, fg="black", bg="#D9D9D6", activebackground="#D9D9D6", command=lambda: select(6))
SelSaveData.place(x=625, y=255)
SelEGuardButt = Button(win, image = img2, padx=15, pady=15, command=lambda: select(5))
SelEGuardButt.place(x=618, y=315)


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

    # CE goes low, conversion of CH0
    GPIO.output(ADC_CS,GPIO.LOW)
    msg = [0x06]
    msg.append(0x00)
    msg.append(0x00)
    CH0_raw = spi.xfer2(msg)
    GPIO.output(ADC_CS,GPIO.HIGH)
    time.sleep(0.001)
    CH0 = ((float)((((CH0_raw[1] & 0x0F)<<8) + CH0_raw[2] - 1365) * 7.5 / 4096))
    if choice != 1:
        if ((CH0 < RedYell1) | (CH0 >= YellRed2)):
            ButtCol1 = "red"
        elif ((CH0 >= RedYell1) & (CH0 < YellGrn1)):
            ButtCol1 = "yellow"
        elif ((CH0 >= GrnYell2) & (CH0 < YellRed2)):
            ButtCol1 = "yellow"
        else:
            ButtCol1 = "green"
    else:
        ButtCol1 = "light blue"
    StatBut1.config(bg=ButtCol1, activebackground=ButtCol1)
#    print("CH0 =", CH0)

# conversion of CH1
    GPIO.output(ADC_CS,GPIO.LOW)
    msg = [0x06]
    msg.append(0x40)
    msg.append(0x00)
    CH1_raw = spi.xfer2(msg)
    CH1 = ((float)((((CH1_raw[1] & 0x0F)<<8) + CH1_raw[2] - 1365) * 7.5 / 4096))
    GPIO.output(ADC_CS,GPIO.HIGH)
    if choice != 2:
        if ((CH1 < RedYell1) | (CH1 >= YellRed2)):
            ButtCol2 = "red"
        elif ((CH1 >= RedYell1) & (CH1 < YellGrn1)):
            ButtCol2 = "yellow"
        elif ((CH1 >= GrnYell2) & (CH1 < YellRed2)):
            ButtCol2 = "yellow"
        else:
            ButtCol2 = "green"
    else:
        ButtCol2 = "light blue"
    StatBut2.config(bg=ButtCol2, activebackground=ButtCol2)
    time.sleep(0.001)


# conversion of CH2
    GPIO.output(ADC_CS,GPIO.LOW)
    msg = [0x06]
    msg.append(0x80)
    msg.append(0x00)
    CH2_raw = spi.xfer2(msg)
    GPIO.output(ADC_CS,GPIO.HIGH)
    CH2 = ((float)((((CH2_raw[1] & 0x0F)<<8) + CH2_raw[2] - 1365) * 7.5 / 4096))
    if choice != 3:
        if ((CH2 < RedYell1) | (CH2 >= YellRed2)):
            ButtCol3 = "red"
        elif ((CH2 >= RedYell1) & (CH2 < YellGrn1)):
            ButtCol3 = "yellow"
        elif ((CH2 >= GrnYell2) & (CH2 < YellRed2)):
            ButtCol3 = "yellow"
        else:
            ButtCol3 = "green"
    else:
        ButtCol3 = "light blue"
    StatBut3.config(bg=ButtCol3, activebackground=ButtCol3)
    time.sleep(0.001)

# conversion of CH3
    GPIO.output(ADC_CS,GPIO.LOW)
    msg = [0x06]
    msg.append(0xC0)
    msg.append(0x00)
    CH3_raw = spi.xfer2(msg)
    GPIO.output(ADC_CS,GPIO.HIGH)
    CH3 = ((float)((((CH3_raw[1] & 0x0F)<<8) + CH3_raw[2] - 1365) * 7.5 / 4096))
    if choice != 4:
        if ((CH3 < RedYell1) | (CH3 >= YellRed2)):
            ButtCol4 = "red"
        elif ((CH3 >= RedYell1) & (CH3 < YellGrn1)):
            ButtCol4 = "yellow"
        elif ((CH3 >= GrnYell2) & (CH3 < YellRed2)):
            ButtCol4 = "yellow"
        else:
            ButtCol4 = "green"
    else:
        ButtCol4 = "light blue"
    
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

#print("+5Vraw = ", (((V5_raw[1] & 0x0F)<<8) + V5_raw[2]))
#    print("CH0 = %3.3f, CH1 = %3.3f,  CH2 = %3.3f, CH3 = %3.3f, +5V = %3.3f,   2.5V = %3.3f   " % (CH0, CH1, CH2, CH3, V5REF, mv2500))
    time.sleep(1)

def read_every_second():
    global x
    global SigIN
    global previousMin
    global RTCTime
    global previousHours
    
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
        SigIN = CH0
    p1.set_value(int(SigIN * 1000))   #SigIN is the selected signal to the meter
#    p1.set_value(int(SigIN))   #SigIN is the selected signal to the meter
    
    t = str(datetime.now())           #read the time
#    print('t = ', t)
    minutes = int(t[14:16])
    hours = int(t[11:13])
    if (previousHours != hours) :
        previousHours = hours
        print("logging diags")
        fout = open('/home/pi/Documents/ElectroguardPi/diags.txt', 'a')
        fout.write(RTCTime + ","+ str(mv2500)[0:6] + "," + str(V5REF)[0:6] + "," + str(M5VREF)[0:6] + "\n")
        fout.close()
        
    if (previousMin != minutes) :
        previousMin = minutes
        RTCTime = getRTCtime()

#        print (RTCTime)
        print("logging")
        fout = open('/home/pi/Documents/ElectroguardPi/Electroguard.txt', 'a')
        fout.write(RTCTime + ","+ str(CH0)[0:6] + "," + str(CH1)[0:6] + "," + str(CH2)[0:6] + "," + str(CH3)[0:6] + "\n")
#        fout.write(t[2:16] + ","+ str(CH0)[0:5] + "," + str(CH1)[0:5] + "," + str(CH2)[0:5] + "," + str(CH3)[0:5] + "\n")
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

p1 = gaugelib.DrawGauge2(
    win,
    max_value=1200,
    min_value=-300,
    size=400,
    bg_col='black',
    unit = "Volts",bg_sel = 2)
p1.place(x=40, y=25)
#p1.pack(side=RIGHT)

read_every_second()

#tk.update_idletasks()
#tk.update()
mainloop()