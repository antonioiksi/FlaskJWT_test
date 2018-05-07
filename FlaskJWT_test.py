#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
import sys, os
import time
import json
import RPi.GPIO as GPIO
from flask import Flask, request, json, jsonify
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
import subprocess
from subprocess import Popen, PIPE, call
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import configparser


class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id


users = [
    User(1, 'user1', 'abcxyz'),
    User(2, 'user2', 'abcxyz'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWT(app, authenticate, identity)


@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity


@app.route('/on')
# @jwt_required()
def on():
    # insert code for RASPBERRY
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    gpio_pin_number = 12
    GPIO.setup(gpio_pin_number, GPIO.OUT)
    GPIO.output(gpio_pin_number, GPIO.HIGH)
    result = {"message": "Device is ON"}
    print("ON")
    return json.dumps(result)


@app.route('/off')
# @jwt_required()
def off():
    # insert code for RASPBERRY
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    gpio_pin_number = 12
    GPIO.setup(gpio_pin_number, GPIO.OUT)
    GPIO.output(gpio_pin_number, GPIO.LOW)
    result = {"message": "Device is OFF"}
    print("OFF")
    return json.dumps(result)


@app.route('/free')
def free():
    return "Hello free"


@app.route('/humidity', methods=['PUT'])
@jwt_required()
def humidity():
    if request.method == 'PUT':
        config = configparser.ConfigParser()
        config.read("/home/pi/poliv/global_config.conf")
        print("put")
        data = request.get_json()
        time = data["freq"]
        threshold = data["threshold"]
        irrigation_time = data["irrigation_time"]
        config.set("time", "time_checking", "%s" % time)
        config.set("sensor", "critical_position", "%s" % threshold)
        config.set("time", "time_irrigation", "%s" % irrigation_time)
        with open("/home/pi/poliv/global_config.conf", "w") as config_file:
            config.write(config_file)
        #        os.execv('/home/pi/poliv/autopoliv.py', [' '])
        #        print("начался полив")
        response = app.response_class(response=json.dumps(data), status=200, mimetype='application/json')
        return response


@app.route('/pump')
def pump():
    Popen("echo 12 > /sys/class/gpio/export", shell=True)
    txt = '''cat /sys/class/gpio/gpio12/value'''
    ret = Popen("%s" % txt, shell=True, stdout=PIPE)
    ret.wait()
    res = ret.communicate()
    print(res)
    print(res[0])
    res_1 = res[0].decode("utf-8")
    res_f = res_1.replace("\n", "")
    print(res_f)
    res_f = int(res_f)
    if res_f == 1:
        #        print("ura")
        message = {"status": "on"}
    else:
        #        print("no")
        message = {"status": "off"}
    js = json.dumps(message)
    response = app.response_class(response=js, status=200, mimetype='application/json')
    return response


@app.route('/irrigation')
# @jwt_required()
def irrigation():
    # insert code for RASPBERRY
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    gpio_pin_number = 12
    GPIO.setup(gpio_pin_number, GPIO.OUT)
    GPIO.output(gpio_pin_number, GPIO.HIGH)
    time.sleep(10)
    GPIO.output(gpio_pin_number, GPIO.LOW)
    result = {"message": "The irrigation has been made"}
    print("ON")
    return json.dumps(result)


@app.route('/show_humidity')
# @jwt_required()
def show_humidity():
    CLK = 11
    MISO = 9
    MOSI = 10
    CS = 8
    mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)
    a = mcp.read_adc(1)

    percent = a * 100 / 1024
    status = "Inactive" if a == 0 else "Active"
    mes = {
        "status": status,
        "humidity":
            {
                "absolute": a,
                "percent": round(percent, 1)
            }
    }

    js = json.dumps(mes)
    response = app.response_class(response=js, status=200, mimetype='application/json')
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
