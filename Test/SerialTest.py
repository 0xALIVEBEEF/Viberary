import serial
import time

ser = serial.Serial(

    port='/dev/serial0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

while True:
    while ser.inWaiting():
        print(ser.read())
    ser.write(input("Input serial: ").encode('utf-8'))