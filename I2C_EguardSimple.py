from smbus import SMBus
import time

bus1 = SMBus(1)
time.sleep(.001)
#bus1.write_byte_data(0x6F, 3, 0x28)
time.sleep(.001)
#bus1.write_byte_data(0x6F, 0x20, 0x28)
time.sleep(.001)
#bus1.write_byte_data(0x6F, 0x21, 0x45)
time.sleep(.001)

checksum = bus1.read_byte_data(0x6F, 0x20)
print("prev checksum =", checksum)
chansel = bus1.read_byte_data(0x6F, 0x21)
print("prev chansel =", chansel)
ch1offset = bus1.read_byte_data(0x6F, 0x22)
ch2offset = bus1.read_byte_data(0x6F, 0x23)
ch3offset = bus1.read_byte_data(0x6F, 0x24)
ch4offset = bus1.read_byte_data(0x6F, 0x25)
ch1gain = bus1.read_byte_data(0x6F, 0x26)
ch2gain = bus1.read_byte_data(0x6F, 0x27)
ch3gain = bus1.read_byte_data(0x6F, 0x28)
ch4gain = bus1.read_byte_data(0x6F, 0x29)
if (checksum == (chansel+ch1offset+ch2offset+ch3offset+ch4offset+ch1gain+ch2gain+ch3gain+ch4gain) & 0x000000FF):
    print("checksum good")
print("prev ch1offset =", ch1offset)
print("prev ch1gain =", ch1gain) 
    
time.sleep(.001)
#CH1
chansel = int(input("enter chansel (15)"))
ch1offset = int(input("enter ch1offset (0 (mV))"))
ch1gain = int(input("enter ch1gain (1000 (mV))"))
ch1gain = int(float(128/((ch1gain-ch1offset)/1000)))
ch1offset = -ch1offset + 128
print("ch1offset = ",ch1offset)
print("ch1gain = ",ch1gain)

#Ch2
ch2offset = int(input("enter ch2offset (0 (mV))"))
ch2gain = int(input("enter ch2gain (1000 (mV))"))
ch2gain = round(128*(1000/(ch2gain-ch2offset)))
ch2offset = -ch2offset + 128
print("ch2gain = ", ch2gain)
# 
#Ch3
ch3offset = int(input("enter ch3offset (0 (mV))"))
ch3gain = int(input("enter ch3gain (1000 (mV))"))
ch3gain = int(float(128/((ch3gain-ch3offset)/1000)))
ch3offset = -ch3offset + 128
# 
#Ch4
ch4offset = int(input("enter ch4offset (0 (mV))"))
ch4gain = int(input("enter ch4gain (1000 (mV))"))
ch4gain = int(float(128/((ch4gain-ch4offset)/1000)))
ch4offset = -ch4offset + 128

checksum = ((chansel+ch1offset+ch2offset+ch3offset+ch4offset+ch1gain+ch2gain+ch3gain+ch4gain) & 0x000000FF)
#checksum = ((chansel+ch1offset+ch1gain) & 0x000000FF)
print("checksum =", checksum)
bus1.write_byte_data(0x6F, 0x20, checksum)
bus1.write_byte_data(0x6F, 0x21, chansel)
bus1.write_byte_data(0x6F, 0x22, ch1offset)   #write Ch1offset
bus1.write_byte_data(0x6F, 0x26, ch1gain)   #write Ch1offset
bus1.write_byte_data(0x6F, 0x23, ch2offset)   #write Ch2offset
bus1.write_byte_data(0x6F, 0x27, ch2gain)   #write Ch2offset
bus1.write_byte_data(0x6F, 0x24, ch3offset)   #write Ch3offset
bus1.write_byte_data(0x6F, 0x28, ch3gain)   #write Ch3offset
bus1.write_byte_data(0x6F, 0x25, ch4offset)   #write Ch4offset
bus1.write_byte_data(0x6F, 0x29, ch4gain)   #write Ch4offset

time.sleep(.001)
bus1.close()