"""
Rotary Encoder
"""

from datetime import datetime
from donkeycar.parts.teensy import TeensyRCin
import re
import time

class RotaryEncoder():
    def __init__(self, mm_per_tick=0.306096, pin=13, debug=False):
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.IN)
        GPIO.add_event_detect(pin, GPIO.RISING, callback=self.isr)

        # initialize the odometer values
        self.mm_per_tick = mm_per_tick
        self.last_time = time.time()
        self.counter = 0
        self.debug = debug

    def isr(self, channel):
        self.counter += 1

    def get_distance(self):
        #save the ticks
        ticks = self.counter
        print('ticks:', ticks)
        distance = ticks * self.mm_per_tick
        if(self.debug):
            print('distance(m):',distance)
        #calculate distance traveled
        return distance

    def get_velocity(self):
        #save off the last time interval and reset the timer
        start_time = self.last_time
        end_time = time.time()
        self.last_time = end_time

        #calculate elapsed time and distance traveled
        seconds = end_time - start_time
        distance = ticks * self.m_per_tick
        velocity = distance / seconds
        if(self.debug):
            print('seconds:', seconds)
            print('distance(m):', distance)
            print('velocity(m/s):', velocity)

        return velocity

    def run_threaded(self):
        return self.meters, self.meters_per_second

    def shutdown(self):
        GPIO.cleanup()
