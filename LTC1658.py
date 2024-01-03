#
import time
import spidev
import RPi.GPIO as GPIO

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
    

while True:
    Volts = input("Enter desired volts:")
    DACwriteCode(DACwriteVoltage(Volts))
    PIN21 = GPIO.input(HEARTBEAT)
    if PIN21 > 0:
        GPIO.output(HEARTBEAT,GPIO.LOW)
        PIN21 = 0
    else:
        GPIO.output(HEARTBEAT,GPIO.HIGH)
        PIN21 = 1
