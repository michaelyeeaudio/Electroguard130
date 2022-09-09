#TimeSerNum.py:
#   - looks at current time
#   - Checks to see if date/time is correct
#   - if not, enters date/time, programs date/time

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
RTminutes = bus1.read_byte_data(0x6F, 0x01)
RTminutes = BCD2Num (RTminutes, 2)
RTseconds = bus1.read_byte_data(0x6F, 0x00)
RTseconds = BCD2Num ((RTseconds & 0x7F), 2)
print("RThours = ", RThour)
print("RTminutes = ", RTminutes)
print("RTSec = ", RTseconds & 0x70)

#d = date.today()
t = str(datetime.now())
print(t)
year = int(t[0:4])
month = int(t[5:7])
day = int(t[8:10])
hour = int(t[11:13])
minutes = int(t[14:16])
choice1 = input ("Is this the correct date?")
if ((choice1 == "n") | (choice1 == "N")):
    year = input ("enter the year (2021)")
    BCDyear = Num2BCD(year, 2)
    print("BCD Year", BCDyear)
    month = input ("enter the month (08)")
    BCDmonth = Num2BCD(month, 2)
    day = input ("enter the day (31)")
    BCDday = Num2BCD(day, 2)
    time = input ("enter the hour and minutes (13:59)")
    atpos = time.find(':')
    BCDhour = 0xC0 | Num2BCD(int(time[atpos-2:atpos]), 2)
    BCDminutes = Num2BCD(int(time[atpos+1:atpos+3]), 2)
else :
    year = t[0:4]
    BCDyear = Num2BCD(year, 2)
    month = int(t[5:7])
    print("month =", month)
    BCDmonth = Num2BCD(month, 2)
    day = int(t[8:10])
    print("day =", day)
    BCDday = Num2BCD(day, 2)
    hour = int(t[11:13])
    print("hour =", hour)
    BCDhour = Num2BCD(hour, 2)
    BCDhour = 0x3F & BCDhour 
    minutes = int(t[14:16])
    print("minutes =", minutes)
    BCDminutes = Num2BCD(int(minutes), 2)
    
print("year =",BCDyear)
print("month =",BCDmonth)
print("day =",BCDday)
print("hour =", BCDhour)
print("minutes =", BCDminutes)
    
#     #get the right bits
wait = input("stopped, y to continue")
bus1.write_byte_data(0x6F, 0x06, BCDyear)
bus1.write_byte_data(0x6F, 0x05, BCDmonth)
bus1.write_byte_data(0x6F, 0x04, BCDday)
bus1.write_byte_data(0x6F, 0x02, BCDhour)
bus1.write_byte_data(0x6F, 0x01, BCDminutes)
bus1.write_byte_data(0x6F, 0x00, 0x80)   #Start Oscillator
bus1.write_byte_data(0x6F, 0x03, 0x08)   #Turn on battery

#input("{} is this the correct date? (Y/n)" .format.year .format.month)


