import serial
import time
import RPi.GPIO as GPIO
from time import sleep

#Pin definitions
RE_0 = 17
DE_0 = 18
RE_1 = 27
DE_1 = 23
RE_2 = 22
DE_2 = 24

def millis():
    return time.time() * 1000

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)

send = serial.Serial(
    port='/dev/ttyAMA0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)
print("Electroguard")
while 1:
    GPIO.output(RE_0,GPIO.HIGH)
    GPIO.output(DE_0,GPIO.HIGH)
    time.sleep(0.001)
    #print("hello")
    send.write(b'a')
    #send.write(b'\x0d')
    time.sleep(0.003)
    GPIO.output(RE_0,GPIO.LOW)
    GPIO.output(DE_0,GPIO.LOW)
    Vref=send.readline()
    print(Vref)
#     Anode=send.readline()
#     Temp=send.readline()
#     V3=send.readline()
#     I3=send.readline()
#     V2=send.readline()
#     I2=send.readline()
#     V1=send.readline()
#     I1=send.readline()
#     V0=send.readline()
#     I0=send.readline()
#     print("V3 is:",V3)
    #print(Vref, Anode, Temp, V3, I3, V2, I2, V1, I1, V0, I0)
    time.sleep(3)
send.close()
GPIO.cleanup()