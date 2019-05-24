#!/usr/bin/python
import sys
sys.path.insert(0,"python/")

import time
import VL53L0X
import RPi.GPIO as GPIO

class TOF(object):
    def __init__(self):
        # GPIO for FRONT sensor shutdown pin
        f_sensor_shutdown = 14

        # GPIO for SIDE1 sensor shutdown pin
        s1_sensor_shutdown = 4

        # GPIO for SIDE2 sensor shutdown pin
        s2_sensor_shutdown = 15

        # GPIO for BACK sensor shutdown pin
        b_sensor_shutdown = 18

        GPIO.setwarnings(False)

        # Setup GPIO for shutdown pins on each VL53L0X
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(f_sensor_shutdown, GPIO.OUT)
        GPIO.setup(s1_sensor_shutdown, GPIO.OUT)
        GPIO.setup(s2_sensor_shutdown, GPIO.OUT)
        GPIO.setup(b_sensor_shutdown, GPIO.OUT)
        # Set all shutdown pins low to turn off each VL53L0X
        GPIO.output(f_sensor_shutdown, GPIO.LOW)
        GPIO.output(s1_sensor_shutdown, GPIO.LOW)
        GPIO.output(s2_sensor_shutdown, GPIO.LOW)
        GPIO.output(b_sensor_shutdown, GPIO.LOW)
        # Keep all low for 500 ms or so to make sure they reset
        time.sleep(0.50)

        #change address of FRONT sensor and start ranging
        self.tof_f = VL53L0X.VL53L0X(i2c_address=0x29)
        GPIO.output(f_sensor_shutdown, GPIO.HIGH)
        time.sleep(0.50)
        self.tof_f.change_address(0x30)
        self.tof_f.open()
        self.tof_f.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)

        #change address of SIDE1 sensor
        self.tof_s1 = VL53L0X.VL53L0X(i2c_address=0x29)
        GPIO.output(s1_sensor_shutdown, GPIO.HIGH)
        time.sleep(0.50)
        self.tof_s1.change_address(0x32)
        self.tof_s1.open()
        self.tof_s1.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)

        #change address of SIDE2 sensor
        self.tof_s2 = VL53L0X.VL53L0X(i2c_address=0x29)
        GPIO.output(s2_sensor_shutdown, GPIO.HIGH)
        time.sleep(0.50)
        self.tof_s2.change_address(0x34)
        self.tof_s2.open()
        self.tof_s2.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)

        #change address of BACK sensor
        self.tof_b = VL53L0X.VL53L0X(i2c_address=0x29)
        GPIO.output(b_sensor_shutdown, GPIO.HIGH)
        time.sleep(0.50)
        self.tof_b.change_address(0x36)
        self.tof_b.open()
        self.tof_b.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)


    def run(self):
        distance1 = self.tof_f.get_distance()
        distance2 = self.tof_s1.get_distance()
        distance3 = self.tof_s2.get_distance()
        distance4 = self.tof_b.get_distance()
        print("FRONT: %d mm, SIDE1: %d mm, SIDE2: %d mm, BACK: %d mm" % (distance1, distance2, distance3, distance4))

        return distance1, distance2, distance3, distance4
