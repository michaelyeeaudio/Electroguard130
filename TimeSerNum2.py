#TimeSerNum2.py:
#   - looks at current time
#   - Checks to see if date/time is correct
#   - if not, enters date/time, programs date/time

from smbus import SMBus
import time
from datetime import date
from datetime import datetime

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

# def BCD2Num(BCDnumber, num_digits):    #number is the number you want to convert, num_digits is 2 for year, etc
#     print("BCD2Num BCD = ", BCDnumber)
#     units = (BCDnumber & 0x000F)
#     tens = (((BCDnumber & 0x00F0) >> 4) * 10)
#     print("BCD2Num TENS = ", tens)
#     print("BCD2Num units =", units)
#     number = tens + units
#     return number

bus1 = SMBus(1)
RTCyear = bcd2bin(bus1.read_byte_data(0x6F, 0x06))
print ("year =", RTCyear)
print(type(RTCyear))
RTCmonth = bcd2bin(bus1.read_byte_data(0x6F, 0x05) & 0x1F)
RTCdate = bcd2bin(bus1.read_byte_data(0x6F, 0x04) & 0x3F)
RTChour = bcd2bin(bus1.read_byte_data(0x6F, 0x02) & 0x3F)
RTCminutes = bcd2bin (bus1.read_byte_data(0x6F, 0x01) & 0x7F)
status = bus1.read_byte_data(0x6F, 0x00)
print("status = ", status)

print ("RTC= %02d:%02d:%02d:%02d:%02d" % (RTCyear, RTCmonth, RTCdate, RTChour, RTCminutes))
#d = date.today()
t = str(datetime.now())
print("PiTime = ", t)
year = int(t[0:4])
month = int(t[5:7])
day = int(t[8:10])
hour = int(t[11:13])
minutes = int(t[14:16])
choice1 = input ("Is this the correct date?")
if ((choice1 == "n") | (choice1 == "N")):
    year = input ("enter the year (2021)")
    BCDyear = Num2BCD(year)
    print("BCD Year", BCDyear)
    month = input ("enter the month (08)")
    BCDmonth = Num2BCD(month)
    day = input ("enter the day (31)")
    BCDday = Num2BCD(day)
    time = input ("enter the hour and minutes (13:59)")
    atpos = time.find(':')
    BCDhour = 0xC0 | Num2BCD(int(time[atpos-2:atpos]), 2)
    BCDminutes = Num2BCD(int(time[atpos+1:atpos+3]), 2)
else :
    year = t[2:4]
    BCDyear = Num2BCD(year)
    print("BCDyear =", BCDyear)
    month = int(t[5:7])
    print("BCDmonth =", month)
    BCDmonth = Num2BCD(month)
    day = int(t[8:10])
    print("BCDday =", day)
    BCDday = Num2BCD(day)
    hour = int(t[11:13])
    print("BCDhour =", hour)
    BCDhour = Num2BCD(hour)
    BCDhour = 0x3F & BCDhour 
    minutes = int(t[14:16])
    print("BCDminutes =", minutes)
    BCDminutes = Num2BCD(int(minutes))
    
#print("write year =",BCDyear)
#print("month =",BCDmonth)
print("write day =",BCDday)
print("write hour =", BCDhour)
print("write minutes =", BCDminutes)
    
#     #get the right bits

wait = input("stopped, y to continue")
bus1.write_byte_data(0x6F, 0x00, 0x80)   #Start Oscillator
bus1.write_byte_data(0x6F, 0x06, BCDyear)
bus1.write_byte_data(0x6F, 0x05, BCDmonth)
bus1.write_byte_data(0x6F, 0x04, BCDday)
bus1.write_byte_data(0x6F, 0x02, BCDhour)
bus1.write_byte_data(0x6F, 0x01, BCDminutes)
bus1.write_byte_data(0x6F, 0x03, 0x08)   #Turn on battery
checksum3 = ((BCDyear + BCDmonth + BCDday + BCDhour + BCDminutes) & 0x00FF)
bus1.write_byte_data(0x6F, 0x2A, BCDminutes)

RTCyear = bcd2bin(bus1.read_byte_data(0x6F, 0x06))
RTCmonth = bcd2bin(bus1.read_byte_data(0x6F, 0x05) & 0x1F)
RTCdate = bcd2bin(bus1.read_byte_data(0x6F, 0x04) & 0x3F)
RTChour = bcd2bin(bus1.read_byte_data(0x6F, 0x02) & 0x3F)
RTCminutes = bcd2bin (bus1.read_byte_data(0x6F, 0x01) & 0x7F)
print ("%02d:%02d:%02d:%02d:%02d" % (RTCyear, RTCmonth, RTCdate, RTChour, RTCminutes))
#input("{} is this the correct date? (Y/n)" .format.year .format.month)

# Store max 12 digits of serial number / name
ser_num = input ("enter the serial number")
ser_num_len = len(ser_num)
if (ser_num_len) > 12:
    ser_num_len = 12
RTCsernum = str(ser_num[0:ser_num_len])
print("ser_num = %s" % (RTCsernum))
bus1.write_byte_data(0x6F, 0x30, ser_num_len)     #this is the sernum length
checksum2 = 0
for x in range (0, ser_num_len):
    print(RTCsernum[x])
    bus1.write_byte_data(0x6F, 0x32 + x, ord(RTCsernum[x]))
    checksum2 = checksum2 + ord(RTCsernum[x])
checksum2 = checksum2 + ser_num_len
bus1.write_byte_data(0x6F, 0x31, checksum2 & 0x000000ff)