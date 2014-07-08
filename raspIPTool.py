#!/usr/bin/python
# Import needed modules
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from subprocess import *
import socket
import time
import os
from datetime import datetime

# Gather the information

# Initialize the LCD plate.
# Pass '0' for early 256 MB Model B boards or '1' for all later versions
lcd = Adafruit_CharLCDPlate(busnum = 1)
lcd.clear()
cmd = "ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'" #Get IP
cmd2 = "ifconfig eth0 | grep 'Mask:' | cut -d: -f4 | awk '{ print $1}'" #Get Netmask
cmd3 = "ip route show | grep 'default via' | cut -d ' ' -f3 | awk '{ print $1}'" #Get Gateway
cmd4 = "ethtool eth0 | grep -w 'Speed\|Duplex' | awk '{ print $1$2}'"
cmd5 = "tail -n 100 /var/log/syslog | grep 'dhclient: DHCPACK from' | awk '{ print $8}'"
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

def con_gateway():
    try:
        # connect to the gateway -- tells us if the gateway is reachable
        s = socket.create_connection((gateway, 80), 2)
        return True
    except:
        pass
        return False

ipaddr = run_cmd(cmd)
netmask = run_cmd(cmd2)
gateway = run_cmd(cmd3)
speed = run_cmd(cmd4)
getdhcp = run_cmd(cmd5)
dns = is_connected()
gwconn = con_gateway()

# Button action below
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
        lcd.message(speed )
        time.sleep(2)
        lcd.clear()
        lcd.message("Ip-Address:\n")
        lcd.message(ipaddr )

    elif lcd.buttonPressed(lcd.DOWN):
        lcd.backlight(lcd.ON)
        lcd.clear()
        lcd.message("Connect to GW:\n")
        lcd.message(gwconn )
        time.sleep(2)
        lcd.clear()
        lcd.message("Resolve google:\n")
        lcd.message(dns )

    elif lcd.buttonPressed(lcd.LEFT):
        lcd.backlight(lcd.ON)            
        lcd.clear()
        lcd.message("Releasing IP.\n")
        os.system("sudo dhclient -r")
        time.sleep(2)
        lcd.clear()
        lcd.message("Deleting leases.\n")
        os.system("sudo rm /var/lib/dhcp/dhclient*")
        time.sleep(2)
        lcd.clear()
        lcd.message("Renewing IP\n")
        os.system("sudo dhclient eth0")
        lcd.message(ipaddr )
        time.sleep(2)
        lcd.clear()
        lcd.message("Ip-Address:\n")
        lcd.message(ipaddr )

    elif lcd.buttonPressed(lcd.RIGHT):
        lcd.backlight(lcd.ON)            
        lcd.clear()
        lcd.message("Got IP from:\n")
        lcd.message(getdhcp )

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
