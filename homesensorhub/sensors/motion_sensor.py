#!/bin/env python3

from time import sleep
import RPi.GPIO as GPIO

class MotionSensor:
    ms_dict = {}

    def __init__(self, gpio = 7, callback = None):
        self.MOTION_GPIO = gpio
        self.callback = None

    def initialize(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.MOTION_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        MotionSensor.ms_dict[self.MOTION_GPIO] = self
        GPIO.add_event_detect(self.MOTION_GPIO, GPIO.BOTH, callback=MotionSensor.motionChangedStatic)

    def motionChangedStatic(gpio):
        MotionSensor.ms_dict[gpio].motionChanged(gpio)

    def motionChanged(self, gpio):
        if GPIO.input(self.MOTION_GPIO):
            print ("Motion Started %d" % gpio)
            motion = 1
        else:
            print ("Motion Ended %d" % gpio)
            motion = 0

        if(self.callback is not None):
            self.callback(motion)