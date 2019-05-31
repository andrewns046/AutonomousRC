#import modules
import os
import time
import sys
import signal
import RPi.GPIO as GPIO
import Adafruit_PCA9685
from t6_encoder import RotaryEncoder
import VL53L1X
from pynput import keyboard
#RotaryEncoder
encoder = RotaryEncoder(22.1600, 13, True)

#initialize time of flight sensor
tof = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
tof.open()
tof.start_ranging(1) # Start ranging, 1 = Short Range, 2 = Medium Range, 3 = Long Range

#initialize pwm board
pwm = Adafruit_PCA9685.PCA9685()

#define values
servo_min = 255
servo_max = 407
servo_center = 331
alpha = 407
beta = 255

#equation variables
spot_length = 630  # 1.5 x the length of car in mm
spot_width = 180 # width of the spot
wheel_distance = 254 # distance between the front and back wheel 254 mm
half_width = 80 # half width of the car is 80 mm

throttle_center = 360
throttle_forward = 370
throttle_back = 350
distance_old = 0
#time_traveled = 0.00


def brake():
    pwm.set_pwm(2, 0, throttle_center)
    time.sleep(0.05)
    pwm.set_pwm(2, 0, throttle_back)
    time.sleep(0.05)
    pwm.set_pwm(2, 0, throttle_center)
    time.sleep(0.05)

# tell the car how far you want it to travel
def drive(distance, direction):
    start_dist = encoder.get_distance()
    pwm.set_pwm(2, 0, throttle_center) #stop car

    throttle = 0;

    if( direction == "forward"):
        throttle = throttle_forward
    else if( direction == "reverse"):
        throttle = throttle_back
    else:
        print("Err:\tIncorrect direction definition")
        return

    dist_travled = 0;
    while( dist_travled <= distance ):
        pwm.set_pwm(2, 0, throttle)
        dist_travled = encoder.get_distance()

# give it angle and turn wheels accordingly
def turn_wheels(direction):
    if(direction == "right"):
        pwm.set_pwm(1, 0,servo_max)
    else if( direction == "center"):
        pwm.set_pwm(1, 0, servo_center)
    else if( direction == "left"):
        pwm.set_pwm(1, 0, servo_min)


#keep going if no parking space or space too small

#========================EDGE DETECT========================================
pwm.set_pwm(1, 0, servo_center)
while True:
    listener.start()
    def on_press(up):
        pwm.set_pwm(2, 0, throttle_forward)
    def on_release(up):
        pwm.set_pwm(2, 0, throttle_center)
    def on_press(down):
        pwm.set_pwm(2, 0, throttle_reverse)
    def on_release(down):
        pwm.set_pwm(2, 0, throttle_center)
    def on_press(left):
        pwm.set_pwm(1, 0, servo_min)
    def on_release(left):
        pwm.set_pwm(1, 0, servo_center)
    def on_press(right):
        pwm.set_pwm(1, 0, servo_max)
    def on_release(right):
        pwm.set_pwm(1, 0, servo_center)

    distance1 = tof.get_distance()
    difference = distance1 - distance_old
    if(difference > 120):
        print("edge 1 detected")
        dist1 = encoder.get_distance();
    if(difference < -120):
        print("edge 2 detected")
        # insert distance traveled
        dist2 = encoder.get_distance();
        distance = dist2 - dist1;
        print("distance travled: " + distance);
        #if distance travled > a little more than length of the car
        # 1.5 x the length of car 630 mm
        if(distance > spot_length):
            print("Parking spot found ")
            b_dist1 = encoder.get_distance()
            brake();
            b_dist2 = encoder.get_distance()
            print("stop err:\t" +b_dist2-b_dist1);
            listener.stop()
            break
        else:
            print("spot too small!")
    distance_old = distance1

#===========================================================================

print("Start parallel parking...")

listener.stop()

print("parking completed!")
