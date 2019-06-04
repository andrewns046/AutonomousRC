#import modules
import os
import time
import sys
import signal
import RPi.GPIO as GPIO
import Adafruit_PCA9685
from encoderOld import RotaryEncoder
import VL53L1X


#RotaryEncoder
encoder = RotaryEncoder(22.1600, pin = 4, debug = False, poll_delay = .05)

#initialize pwm board
pwm = Adafruit_PCA9685.PCA9685()

#define values

throttle_center = 370
throttle_forward = 380
throttle_back = 360
throttle_max = 450
#time_traveled = 0.00

def scale(value, goal):
    return int(value + 377)

def PID(goal):
    goal = goal
    minSpeed = 370
    currentSpeed = 0
    while(True):
        value = encoder.update()
        error = goal-value
        ofset = scale(currentSpeed + error, goal) - scale(currentSpeed, goal)
        print(ofset,value, scale(currentSpeed, goal))
        currentSpeed = currentSpeed + error
        setSpeed = scale(currentSpeed, goal)
        if(setSpeed > throttle_max):
            setSpeed = throttle_max
        pwm.set_pwm(2, 0, setSpeed)

PID(0)

