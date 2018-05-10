#!/usr/bin/env python3
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import sys
import subprocess
import configparser
#from subprocess import call

CLK=11
MISO=9
MOSI=10
CS=8
mcp=Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

config = configparser.ConfigParser()
config.read("/home/pi/poliv/global_config.conf")

def main():
    a=mcp.read_adc(1)
    print(a)
    f=open('/home/pi/poliv/sost.txt', 'w')
    f.write('%s' %a)
    f.close()
    config.read("/home/pi/poliv/global_config.conf")
    sens = config.get("sensor","critical_position")
    time_hum = config.get("time","time_irrigation")
    print(sens)
    sens_final = int(sens)
    sens_final = sens_final*10
    if a<sens_final:
        subprocess.call("/home/pi/rele.py ", shell=True)
        time_hum = int(time_hum)
        print(time_hum)
        time.sleep(time_hum)
        subprocess.call("/home/pi/rele_off.py ", shell=True)
        mes="был произведен полив"
        print(mes)
#        b=mcp.read_adc(1)
#        print(b)
#        f=open('/home/pi/poliv/sost.txt', 'w')
#        f.write('%s' %b)
#        f.close()
#        main()
#        subprocess.call(['''/home/pi/sender.py "%s"''' %mes], shell=True)        
    else:
        ok=1

while True:
    main()
    config.read("/home/pi/poliv/global_config.conf")
    time_check = config.get("time","time_checking")
    time_check = int(time_check)
    time.sleep(time_check)

