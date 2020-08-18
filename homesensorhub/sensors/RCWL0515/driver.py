#!/usr/bin/env python3

import logging

import RPi.GPIO as GPIO


class MotionSensorRCWL0515:
    ms_dict = {}

    def __init__(self, gpio, callback=None):
        self.logger = logging.getLogger(__name__)
        self.MOTION_GPIO = gpio
        self.callback = callback

        # Read initial state
        self.motion = None
        self.initialize_gpio()
        self.__motionChanged(self.MOTION_GPIO)

        print("Motion initialized !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        self.install_callback()

    def get(self):
        return self.motion

    def initialize_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.MOTION_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def install_callback(self):
        MotionSensorRCWL0515.ms_dict[self.MOTION_GPIO] = self
        GPIO.add_event_detect(self.MOTION_GPIO, GPIO.BOTH,
                              callback=MotionSensorRCWL0515.__motionChangedStatic)

    def __motionChangedStatic(gpio):
        MotionSensorRCWL0515.ms_dict[gpio].__motionChanged(gpio)

    def __motionChanged(self, gpio):
        self.logger.debug("Motion Changed %d" % gpio)
        if GPIO.input(self.MOTION_GPIO):
            next_motion = True
            self.logger.debug("Motion Started %d" % gpio)
        else:
            next_motion = False
            self.logger.debug("Motion Ended %d" % gpio)

        if(next_motion == self.motion):
            self.logger.error("Motion Transitioned from {} to {}".format(self.motion, next_motion))
        else:
            self.motion = next_motion

            if(self.callback is not None):
                self.callback(self.motion)
