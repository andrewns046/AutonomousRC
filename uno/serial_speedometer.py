import serial
import RPi.GPIO as GPIO
import time

ser = serial.Serial("/dev/ttyACM0",9600)  # change ACM number as found from ls /dev/tty/ACM*
ser.baudrate=9600

while True:
  velocity = read(4) # expecting 4 bytes
  print(velocity) 
