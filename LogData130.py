#this reads calibration, logs calibrated data
#   - programs serial number
#   - reads things from Non-Vol (calibration data) 
#   - reads ADCs
#   - Does not use Calibration

import time
import spidev
import threading
import os
from smbus import SMBus
import RPi.GPIO as GPIO
text1 = "starting"
bus = 0
bus1 = SMBus(1)
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
        
def I2C_init():
    bus = SMBus(1)
    time.sleep(.001)
    bus.write_byte_data(0x6F, 3, 0x28)
    time.sleep(.001)
    bus.write_byte_data(0x6F, 0x20, 0x28)
    time.sleep(.001)

def get_adcs():
    global CH0
    global CH1
    global CH2
    global CH3
    global count

    while(True):
    
        # CE goes low, conversion of CH0
        GPIO.output(ADC_CS,GPIO.LOW)
        msg = [0x06]
        msg.append(0x00)
        msg.append(0x00)
        CH0_raw = spi.xfer2(msg)
        GPIO.output(ADC_CS,GPIO.HIGH)
        time.sleep(0.001)
        CH0 = round(((((CH0_raw[1] & 0x0F)<<8) + CH0_raw[2] - 1365) * 7.5 / 4096),3)
        CH0 = round((CH0 * ch1gain/128) + ((ch1offset-128)/1000),3)

# conversion of CH1
        GPIO.output(ADC_CS,GPIO.LOW)
        msg = [0x06]
        msg.append(0x40)
        msg.append(0x00)
        CH1_raw = spi.xfer2(msg)
        CH1 = round(((((CH1_raw[1] & 0x0F)<<8) + CH1_raw[2] - 1365) * 7.5 / 4096),3)        
        CH1 = round((CH1 * ch2gain/128) + ((ch2offset-128)/1000),3)
        GPIO.output(ADC_CS,GPIO.HIGH)
        time.sleep(0.001)

# conversion of CH2
        GPIO.output(ADC_CS,GPIO.LOW)
        msg = [0x06]
        msg.append(0x80)
        msg.append(0x00)
        CH2_raw = spi.xfer2(msg)
        GPIO.output(ADC_CS,GPIO.HIGH)
        CH2 = round(((((CH2_raw[1] & 0x0F)<<8) + CH2_raw[2] - 1365) * 7.5 / 4096),3)
        CH2 = round((CH2 * ch3gain/128) + ((ch3offset-128)/1000),3)
        time.sleep(0.001)

# conversion of CH3
        GPIO.output(ADC_CS,GPIO.LOW)
        msg = [0x06]
        msg.append(0xC0)
        msg.append(0x00)
        CH3_raw = spi.xfer2(msg)
        GPIO.output(ADC_CS,GPIO.HIGH)
        CH3 = round(((((CH3_raw[1] & 0x0F)<<8) + CH3_raw[2] - 1365) * 7.5 / 4096),3)
        CH3 = round((CH3 * ch4gain/128) + ((ch4offset-128)/1000),3)
        time.sleep(.001)
        count = count +1
        if (count >= 29):
            count = 0
            fout = open('output.txt', 'a')
            fout.write(str(CH0) + ',' + str(CH1) + ',' + str(CH2) + ',' + str(CH3) + ',' + "\n")
            fout.close()
            print("logged")
    
        print("CH1 =", CH0)
        print("CH2 =", CH1)
        print("CH3 =", CH2)
        print("CH4 =", CH3)
#        print(text1)
        print("")
#        os.system('clear')
        time.sleep(2)

def Calibration():
    text1 = "put 0V on Channel 1, enter Reading"
    txt_zero_0 = input()
    fl_zero_0 = float(txt_zero_0)
    text1 = "put 1V on Channel 1, enter Reading"
    txt_one_0 = input()
    fl_one_0 = float(txt_one_0)



# Initialize I2C (SMBus)
bus = SMBus(1)
read_nvram()

#main
count = 0
fout = open('output.txt', 'w')
SerialNum = str(input("enter SerialNum (8digits)"))
chansel = str(bus1.read_byte_data(0x6F, 0x21))
fout.write(SerialNum + "," + chansel + "\n")
fout.close()
t1 = threading.Thread(target = get_adcs)
t1.start()

