from smbus import SMBus
import time
import os
from os.path import exists

SerialNumber = "123ewq"
chansel = 0x2F
SNCheckSum = 0x33
CalCheckSum = 0x65
ch1offset = 128
ch1gain = 126
ch2offset = 128
ch2gain = 126
ch3offset = 128
ch3gain = 126
ch4offset = 128
ch4gain =126

CalList = ["SerialNumber", "chansel", "SNCheckSum", "CalCheckSum", "ch1offset", "ch1gain","ch2offset", "ch2gain","ch3offset", "ch3gain","ch4offset", "ch4gain"]
file_exists = exists("/home/pi/Documents/ElectroguardPi/eguardsettings.txt")
if(file_exists):
    os.remove("/home/pi/Documents/ElectroguardPi/eguardsettings.txt")
#with open("/home/pi/Documents/ElectroguardPi/eguardsettings.txt", "a") as input:
with open("/home/pi/Documents/ElectroguardPi/eguardsettings_b.txt", "w") as output:
    print("SerialNumber \n", SerialNumber)
    output.write("SerialNumber " + SerialNumber + "\n")
    print("chansel \n", chansel)
    output.write("chansel " + str(chansel) + "\n")
    print("SNCheckSum \n", SNCheckSum)
    output.write("SNCheckSum " + str(SNCheckSum) + "\n")
    print("CalCheckSum \n", CalCheckSum)
    output.write("CalCheckSum " + str(CalCheckSum) + "\n")
    print("ch1offset \n", ch1offset)
    output.write("ch1offset " + str(ch1offset) + "\n")
    print("ch1gain \n", ch1gain)
    output.write("ch1gain " + str(ch1gain) + "\n")
    print("ch2offset \n", ch2offset)
    output.write("ch2offset " + str(ch2offset) + "\n")
    print("ch2gain \n", ch2gain)
    output.write("ch2gain " + str(ch2gain) + "\n")
    print("ch3offset \n", ch3offset)
    output.write("ch3offset " + str(ch3offset) + "\n")
    print("ch3gain \n", ch3gain)
    output.write("ch3gain " + str(ch3gain) + "\n")
    print("ch4offset \n", ch4offset)
    output.write("ch4offset " + str(ch4offset) + "\n")
    print("ch4gain \n", ch4gain)
    output.write("ch4gain " + str(ch4gain) + "\n")
    

os.replace('/home/pi/Documents/ElectroguardPi/eguardsettings_b.txt', '/home/pi/Documents/ElectroguardPi/eguardsettings.txt')
#input.close()
output.close()