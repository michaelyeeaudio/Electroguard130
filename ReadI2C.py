#read I2C
# this script reads the I2C RTC memory
#   - Reads data and time from RTC
#   - Reads calibration constants

from smbus import SMBus
import time
from datetime import date
from datetime import datetime

def Num2BCD(number, num_digits):    #number is the number you want to convert, num_digits is 2 for year, etc
    st_number = str(number)
    numb_cnt = len(st_number)
    if(numb_cnt > 1):
        BCDnumber = int(st_number[numb_cnt - 2 :numb_cnt])
    else:
        BCDnumber = number
    return BCDnumber

def BCD2Num(BCDnumber, num_digits):    #number is the number you want to convert, num_digits is 2 for year, etc
    number = (BCDnumber & 0x0F) + (((BCDnumber & 0xF0) >> 4) * 10)
    return number

bus1 = SMBus(1)
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
print("RTyear = ", RTyear)
print("RTmonth = ", RTmonth)
print("RTdate = ", RTdate)
print("RThours = ", RThour)
print("RTminutes = ", RTminutes)
print("RTSec = ", RTseconds & 0x70)

checksum = bus1.read_byte_data(0x6F, 0x20)
chansel = bus1.read_byte_data(0x6F, 0x21)
ch1offset = bus1.read_byte_data(0x6F, 0x22)
ch2offset = bus1.read_byte_data(0x6F, 0x23)
ch3offset = bus1.read_byte_data(0x6F, 0x24)
ch4offset = bus1.read_byte_data(0x6F, 0x25)
ch1gain = bus1.read_byte_data(0x6F, 0x26)
ch2gain = bus1.read_byte_data(0x6F, 0x27)
ch3gain = bus1.read_byte_data(0x6F, 0x28)
ch4gain = bus1.read_byte_data(0x6F, 0x29)
print("prev ch1gain =", ch1gain)
print("prev ch1offset =", ch1offset)
print("prev ch2gain =", ch2gain)
print("prev ch2offset =", ch2offset)
print("prev ch3gain =", ch3gain)
print("prev ch3offset =", ch3offset)
print("prev ch4gain =", ch4gain)
print("prev ch4offset =", ch4offset)
