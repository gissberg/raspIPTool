#!/usr/bin/python
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from subprocess import *
import socket
import time
import os
from datetime import datetime

# Initialize the LCD plate.
# Pass '0' for early 256 MB Model B boards or '1' for all later versions

lcd = Adafruit_CharLCDPlate(busnum = 1)
lcd.clear()
cmd = "ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'" #Get IP
cmd2 = "ifconfig eth0 | grep 'Mask:' | cut -d: -f4 | awk '{ print $1}'" #Get Netmask
cmd3 = "ip route show | grep 'default via' | cut -d ' ' -f3 | awk '{ print $1}'" #Get Gateway
REMOTE_SERVER = "www.google.com"
lcd.begin(16,1)

def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output

def is_connected():
  try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname(REMOTE_SERVER)
    # connect to the host -- tells us if the host is actually
    # reachable
    s = socket.create_connection((host, 80), 2)
    return True
  except:
     pass
  return False

ipaddr = run_cmd(cmd)
netmask = run_cmd(cmd2)
gateway = run_cmd(cmd3)
dns = is_connected()


pressed_time = None

while True:
    if lcd.buttonPressed(lcd.UP):
            lcd.backlight(lcd.ON)
            lcd.clear()
            lcd.message("Ip-Address:\n")
            lcd.message(ipaddr )
            time.sleep(2)
            lcd.clear()
            lcd.message("Netmask:\n")
            lcd.message(netmask )
            time.sleep(2)
            lcd.clear()
            lcd.message("Default GW:\n")
            lcd.message(gateway )
            time.sleep(2)
            lcd.clear()
            lcd.message("Internet works:\n")
            lcd.message(dns )

    elif lcd.buttonPressed(lcd.DOWN):
            lcd.backlight(lcd.ON)
            lcd.clear()
            lcd.message("Down we go:\n")

    elif lcd.buttonPressed(lcd.LEFT):
            lcd.backlight(lcd.ON)            
            lcd.clear()
            lcd.message("Left we go:\n")

    elif lcd.buttonPressed(lcd.RIGHT):
            lcd.backlight(lcd.ON)            
            lcd.clear()
            lcd.message("Internet works:\n")
            lcd.message(dns )

    elif lcd.buttonPressed(lcd.SELECT):
        if pressed_time is None:
            #just pressed
            lcd.backlight(lcd.OFF)
            pressed_time = time.time()
        elif time.time() - pressed_time >= 3.0:
            lcd.clear()
            lcd.message("Shutting Down")
            time.sleep(1)
            lcd.clear()
            lcd.backlight(lcd.OFF)
            os.system("sudo shutdown -h now")

    else:
        pressed_time = None

    time.sleep(0.1)
