raspIPTool
==========
A script to use a raspberryPi equipedwith Adafruits LCD Pi Plate as a testertool when building and managing a rj45 lan or wan. All functions are availabe from the 5 buttons on the LCD-display. The idea was born when I patched up a new office and had to use my laptop to see if every lan-port worked. 24 release/renew with my laptop in one hand and changing lan-port with the other. To install the script just run:

git clone https://github.com/gissberg/raspIPTool.git

Further on I'll make this util menu-driven instead.


 I'm planning the following features:
 
  1. Display the IP, Netmask and gateway.
  2. releasing and renewing the IP
  3. Check for internet connectivity thru dns-resolving, pinging predetermined ip-addresses.
 

This list will probably grow with time as the project matures.


To use this script you will have to download the Adafruit-Raspberry-Pi-Python-Code, and this is how you do it with raspbian:

sudo apt-get install git
git clone https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code.git
cd Adafruit-Raspberry-Pi-Python-Code
cd Adafruit_CharLCDPlate

You will also need to install RPi.GPIO, the python library for Pi that allows easy GPIO access. On Raspbian, just run: 

sudo apt-get install python-dev
sudo apt-get install python-rpi.gpio
