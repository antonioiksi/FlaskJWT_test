#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import RPi.GPIO as GPIO
from subprocess import Popen, PIPE, call

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
gpio_pin_number = 12
GPIO.setup(gpio_pin_number, GPIO.OUT)
GPIO.output(gpio_pin_number, GPIO.HIGH)
#txt = '''cat /sys/class/gpio/gpio12/value'''
#ret = Popen("%s" %txt, shell=True,  stdout = PIPE)
#ret.wait()
#res = ret.communicate()
#print(res[0])
#res=res[0].replace("\n","")
#print(res)
#res = int(res)
#if res == 1:
#    print("ura")
#else:
#    print("no")
