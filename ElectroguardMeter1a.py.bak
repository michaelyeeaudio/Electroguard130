#!/usr/bin/env python3
from tkinter import *
import tkinter as tk
from tkinter.font import Font
from tkinter import messagebox
import random
import gaugelib
import time
import spidev
import RPi.GPIO as GPIO
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

win = tk.Tk()
#button_0 = Button(win, text="Chan1", padx=40, pady=20, command=button_add)
#CH0Label.grid(row=0, column=0)
a5 = PhotoImage(file="g1.png")
win.tk.call('wm', 'iconphoto', win._w, a5)
win.title("Electroguard Raspberry Pi Version 2.0")
win.geometry("600x300+0+0")
win.resizable(width=True, height=True)
win.configure(bg='black')

g_value=0
x=0

def get_adcs():
    global CH0
    global CH1
    global CH2
    global CH3

    # CE goes low, conversion of CH0
    GPIO.output(ADC_CS,GPIO.LOW)
    msg = [0x06]
    msg.append(0x00)
    msg.append(0x00)
    CH0_raw = spi.xfer2(msg)
    GPIO.output(ADC_CS,GPIO.HIGH)
    time.sleep(0.001)
    CH0 = ((float)((((CH0_raw[1] & 0x0F)<<8) + CH0_raw[2] - 1365) * 7.5 / 4096))
#    print("CH0 =", CH0)

# conversion of CH1
    GPIO.output(ADC_CS,GPIO.LOW)
    msg = [0x06]
    msg.append(0x40)
    msg.append(0x00)
    CH1_raw = spi.xfer2(msg)
    CH1 = ((float)((((CH1_raw[1] & 0x0F)<<8) + CH1_raw[2] - 1365) * 7.5 / 4096))
    GPIO.output(ADC_CS,GPIO.HIGH)
    time.sleep(0.001)


# conversion of CH2
    GPIO.output(ADC_CS,GPIO.LOW)
    msg = [0x06]
    msg.append(0x80)
    msg.append(0x00)
    CH2_raw = spi.xfer2(msg)
    GPIO.output(ADC_CS,GPIO.HIGH)
    CH2 = ((float)((((CH2_raw[1] & 0x0F)<<8) + CH2_raw[2] - 1365) * 7.5 / 4096))
    time.sleep(0.001)

# conversion of CH3
    GPIO.output(ADC_CS,GPIO.LOW)
    msg = [0x06]
    msg.append(0xC0)
    msg.append(0x00)
    CH3_raw = spi.xfer2(msg)
    GPIO.output(ADC_CS,GPIO.HIGH)
    CH3 = ((float)((((CH3_raw[1] & 0x0F)<<8) + CH3_raw[2] - 1365) * 7.5 / 4096))
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
    
#print("+5Vraw = ", (((V5_raw[1] & 0x0F)<<8) + V5_raw[2]))
    print("CH0 = %3.3f, CH1 = %3.3f,  CH2 = %3.3f, CH3 = %3.3f, +5V = %3.3f,   2.5V = %3.3f   " % (CH0, CH1, CH2, CH3, V5REF, mv2500))


def read_every_second():
    global x
    get_adcs()
    #g_value=random.randint(-30,700)
    p1.set_value(int(CH0 * 1000))
    #print("CH0_raw =", CH0)
    g_value=random.randint(0,100)
    x+=1    
    if x>100:
#        graph1.draw_axes()
        x=0
    win.after(400, read_every_second)

p1 = gaugelib.DrawGauge2(
    win,
    max_value=1200,
    min_value=-300,
    size=200,
    bg_col='black',
    unit = "Voltage mV",bg_sel = 2)
p1.pack()

read_every_second()
if PIN21 > 0:
    GPIO.output(HEARTBEAT,GPIO.LOW)
    PIN21 = 0
    print("off")
else:
    GPIO.output(HEARTBEAT,GPIO.HIGH)
    PIN21 = 1
    print("on")
mainloop()