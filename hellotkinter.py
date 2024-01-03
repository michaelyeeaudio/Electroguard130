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
from os.path import exists
import zipfile
import spidev
import RPi.GPIO as GPIO

global currentVoltage
global oldVoltage
global newVoltage
global speed_set

#Initial values
speed_set = 1
oldVoltage = 0
newVoltage = 0

#startTime= datetime.now()
win = tk.Tk()
#win.attributes('-fullscreen',True)
win.geometry("800x400+0+0")
win.configure(bg="black")

# We only have SPI bus 0 available to us on the Pi
bus = 0

#Chip select pin. Set to 0 or 1, depending on the connections
ChipSel = 1

# Enable SPI
spi = spidev.SpiDev()

# Open a connection to a specific bus and device (chip select pin)
spi.open(bus, ChipSel)

# Set SPI speed and mode
spi.max_speed_hz = 500000
spi.mode = 0

CE_DAC = 23
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
DAC_CS = 23
GPIO.setup(DAC_CS, GPIO.OUT, initial=GPIO.HIGH)
HEARTBEAT = 21
#global PIN21
PIN21 = 1
GPIO.setup(HEARTBEAT, GPIO.OUT, initial=GPIO.HIGH)

def changeSpeedState(speedsetting):
    global speed_set
    if speedsetting == 0:
        speed_set = 0
    if speedsetting == 1:
        speed_set = 1
    if speedsetting == 2:
        speed_set = 2
        
def greyout():
#     G1voltage1.config(bg="#D0D1AB")
#     G1voltage2.config(bg="#D0D1AB")
#     G1voltage3.config(bg="#D0D1AB")
#     G1voltage4.config(bg="#D0D1AB")
#     G1voltage5.config(bg="#D0D1AB")
#     G2voltage1.config(bg="#D0D1AB")
#     G2voltage2.config(bg="#D0D1AB")
#     G2voltage3.config(bg="#D0D1AB")
#     G2voltage4.config(bg="#D0D1AB")
#     G2voltage5.config(bg="#D0D1AB")
    G3voltage1.config(bg="#D0D1AB")
    G3voltage2.config(bg="#D0D1AB")
    G3voltage3.config(bg="#D0D1AB")
    G3voltage4.config(bg="#D0D1AB")
    G3voltage5.config(bg="#D0D1AB")

        

def DACwriteVoltage(Volts):
    offset = 1.63 + .00657
    gain = .985
    intermediatecode = float(Volts) + offset
    print(intermediatecode)
    code = float((intermediatecode * (65536/3.31)) * gain)
    if code<0:
        code=0
    if code > 65535:
        code=65535
    return int(code)

def DACwriteCode(code):
    #ChipSel = 0
    print("code = " , code)
    GPIO.setup(DAC_CS, GPIO.OUT, initial=GPIO.LOW)
    lwrByte = (code & 0x00FF)
    upprByte = (code & 0xFF00) >> 8
    spi.xfer2([upprByte])
    print(upprByte)
    spi.xfer2([lwrByte])
    print(lwrByte)
    GPIO.setup(DAC_CS, GPIO.OUT, initial=GPIO.HIGH)
    #ChipSel = 1

def colorChange(Volts, Button):
    global currentVoltage
    global oldVoltage
    global newVoltage
    global speed_set
    newVoltage = Volts
    GPIO.output(HEARTBEAT,GPIO.LOW)
    DACwriteCode(DACwriteVoltage(Volts))
#     PIN21 = GPIO.input(HEARTBEAT)
#     if PIN21 > 0:
#         GPIO.output(HEARTBEAT,GPIO.LOW)
#         PIN21 = 0
#     else:
#         GPIO.output(HEARTBEAT,GPIO.HIGH)
#         PIN21 = 1
    greyout()
    while((oldVoltage-newVoltage) != 0):
        global currentVoltage
        Button.config(bg="yellow")
        if ((oldVoltage-newVoltage) > 0):
            currentVoltage += -.001
        elif ((oldVoltage-newVoltage) < 0):
            currentVoltage += .001
        elif (speed_set == 0):
            time.sleep(.016)
        elif (speed_set == 1):
            time.sleep(.004)
        else:
            time.sleep(0)
    Button.config(bg="green")
    oldVoltage = newVoltage


#### Frame that contains labels with decimal value ####
var1 = 3.79
string_variable1=tk.StringVar()
string_variable1.set(var1)
var2 = 12.11
string_variable2=tk.StringVar()
string_variable2.set(var2)
C = Canvas(win, bg="#88A799", height=150, width=300)
C.place(x=40, y=65)
var1_output = Label(win, bg="white", textvariable=string_variable1, relief="sunken", height=2, width=12).place(x=195, y=100)
var2_output = Label(win, bg="white", textvariable=string_variable2, relief="sunken", height=2, width=12).place(x=195, y=150)
Chan1Label = Label(win, text="Channel 1", height=2, width=12).place(x=50, y=100)
Chan2Label = Label(win, text="Channel 2", height=2, width=12).place(x=50, y=150)

##### (+) and (-) buttons with ramp button ######
PlusButton = Button(win, text="+", font=15, width=8, height=1).place(x=40, y= 240)
MinusButton = Button(win, text="-", font=15, width=8, height=1).place(x=40, y= 290)
RampButton = Button(win, text="Ramp", font=15, width=6, height=1).place(x=230, y= 265)
SlowButton = Button(win, text="Slow", width=6, height=1, command=lambda: changeSpeedState(0)).place(x=40, y=350) #20mV/sec -- 740 sec (speed that alex would like)
MedButton = Button(win, text="Medium", width=6, height=1, command=lambda: changeSpeedState(1)).place(x=141, y=350) #40mV/sec -- 30 sec (speed that alex would like)
FastButton = Button(win, text="Fast", width=6, height=1, command=lambda: changeSpeedState(2)).place(x=241, y=350) #80mV/sec -- 9sec (speed that alex would like)

##### Voltage Buttons For Groups #####
voltage1 = "264mV"
stringvar_v1=tk.StringVar()
stringvar_v1.set(voltage1)
voltage2 = "150mV"
stringvar_v2=tk.StringVar()
stringvar_v2.set(voltage2)
voltage3 = "10mV"
stringvar_v3=tk.StringVar()
stringvar_v3.set(voltage3)
voltage4 = "0mV"
stringvar_v4=tk.StringVar()
stringvar_v4.set(voltage4)
voltage5= "-96mV"
stringvar_v5=tk.StringVar()
stringvar_v5.set(voltage5)
GroupLabel1 = Label(win, text="Group 1", width=7, bg="black", fg="white", font=13.5).place(x=390, y=13)
G1voltage1 = Button(win, text="Voltage 1", width=5, padx=20, pady=15, fg="black", bg="#D0D1AB", activebackground="#88A799", command=lambda: colorChange())
G1voltage1.place(x=390, y=65)
G1voltage2 = Button(win, text="Voltage 2", width=5, padx=20, pady=15, fg="black", bg="#D0D1AB", activebackground="#88A799", command=lambda: select(2)).place(x=390, y=125)
G1voltage3 = Button(win, text="Voltage 3", width=5, padx=20, pady=15, fg="black", bg="#D0D1AB", activebackground="#88A799", command=lambda: select(3)).place(x=390, y=185)
G1voltage4 = Button(win, text="Voltage 4", width=5, padx=20, pady=15, fg="black", bg="#D0D1AB", activebackground="#88A799", command=lambda: select(4)).place(x=390, y=245)
G1voltage5= Button(win, text="Voltage 5", width=5, padx=20, pady=15, fg="black", bg="#D0D1AB", activebackground="#88A799", command=lambda: select(6)).place(x=390, y=305)
GroupLabel2 = Label(win, text="Group 2", width=7, bg="black", fg="white", font=13.5).place(x=520, y=13)
G2voltage1 = Button(win, text="Voltage 1", width=5, padx=20, pady=15, fg="black", bg="#D0D1AB", activebackground="#88A799", command=lambda: select(1)).place(x=520, y=65)
G2voltage2 = Button(win, text="Voltage 2", width=5, padx=20, pady=15, fg="black", bg="#D0D1AB", activebackground="#88A799", command=lambda: select(2)).place(x=520, y=125)
G2voltage3 = Button(win, text="Voltage 3", width=5, padx=20, pady=15, fg="black", bg="#D0D1AB", activebackground="#88A799", command=lambda: select(3)).place(x=520, y=185)
G2voltage4 = Button(win, text="Voltage 4", width=5,padx=20, pady=15, fg="black", bg="#D0D1AB", activebackground="#88A799", command=lambda: select(4)).place(x=520, y=245)
G2voltage5= Button(win, text="Voltage 5", width=5, padx=20, pady=15, fg="black", bg="#D0D1AB", activebackground="#88A799", command=lambda: select(6)).place(x=520, y=305)
GroupLabel3 = Label(win, text="Group 3", width=7, bg="black", fg="white", font=13.5).place(x=650, y=13)
G3voltage1 = Button(win, textvariable=stringvar_v1, width=5, padx=20, pady=15, fg="black", bg="#D0D1AB", activebackground="#88A799", command=lambda: colorChange(.264, G3voltage1))
G3voltage1.place(x=650, y=65)
G3voltage2 = Button(win, textvariable=stringvar_v2, width=5,padx=20, pady=15, fg="black", bg="#D0D1AB", activebackground="#88A799", command=lambda: colorChange(.150, G3voltage2))
G3voltage2.place(x=650, y=125)
G3voltage3 = Button(win, textvariable=stringvar_v3, width=5,padx=20, pady=15, fg="black", bg="#D0D1AB", activebackground="#88A799", command=lambda: colorChange(.01, G3voltage3))
G3voltage3.place(x=650, y=185)
G3voltage4 = Button(win, textvariable=stringvar_v4, width=5,padx=20, pady=15, fg="black", bg="#D0D1AB", activebackground="#88A799", command=lambda: colorChange(0, G3voltage4))
G3voltage4.place(x=650, y=245)
G3voltage5= Button(win, textvariable=stringvar_v5, width=5, padx=20, pady=15, fg="black", bg="#D0D1AB", activebackground="#88A799", command=lambda: colorChange(-.096, G3voltage5))
G3voltage5.place(x=650, y=305)

#read_every_second()
# print ("clock: " , datetime.now() - startTime)
GPIO.output(HEARTBEAT,GPIO.HIGH)
mainloop()

