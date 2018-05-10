#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
gpio_pin_number = 12
GPIO.setup(gpio_pin_number, GPIO.OUT)
GPIO.output(gpio_pin_number, GPIO.LOW)
