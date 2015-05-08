#!/usr/bin/env python
#
# GrovePi Example for using the Grove HCHO Sensor (http://www.seeedstudio.com/wiki/Grove_-_HCHO_Sensor)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
# LICENSE: 
# These files have been made available online through a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/) license.

import os
import os.path
import sys
import psutil
import argparse
import time
import rrdtool
import grovepi
from grove_rgb_lcd import *

parser = argparse.ArgumentParser(description='environment monitor')
parser.add_argument('--quiet', action='store_true', help='disable displaying results on console')
parser.add_argument('--nolcd', action='store_true', help='disable displaying results on lcd')
args = parser.parse_args()



pidfile = "/var/run/mprobe.pid"
mypid = os.getpid()
counter = 0

if os.path.exists(pidfile):
    oldpid = int(open(pidfile).read())
    if psutil.pid_exists(oldpid):
        print("Sorry, found a pidfile!  Process {0} is still running.".format(oldpid))
        raise SystemExit
    else:
        os.remove(pidfile)
open(pidfile, 'w').write(str(os.getpid()))

if not os.path.isfile("aq_sensor.rrd"):
	ret_aq = rrdtool.create("aq_sensor.rrd", "--no-overwrite", "--step", "30", "--start", '0',
	 "DS:sensor_value:GAUGE:300:U:U",
	 "RRA:AVERAGE:0.5:1:600",
	 "RRA:AVERAGE:0.5:6:700",
	 "RRA:AVERAGE:0.5:24:775",
	 "RRA:AVERAGE:0.5:288:797",
	 "RRA:MAX:0.5:1:600",
	 "RRA:MAX:0.5:6:700",
	 "RRA:MAX:0.5:24:775",
	 "RRA:MAX:0.5:444:797")
if not os.path.isfile("hcho_sensor.rrd"):
	ret_hcho = rrdtool.create("hcho_sensor.rrd", "--no-overwrite", "--step", "30", "--start", '0',
	 "DS:sensor_value:GAUGE:300:U:U",
	 "RRA:AVERAGE:0.5:1:600",
	 "RRA:AVERAGE:0.5:6:700",
	 "RRA:AVERAGE:0.5:24:775",
	 "RRA:AVERAGE:0.5:288:797",
	 "RRA:MAX:0.5:1:600",
	 "RRA:MAX:0.5:6:700",
	 "RRA:MAX:0.5:24:775",
	 "RRA:MAX:0.5:444:797")
if not os.path.isfile("mq5_sensor.rrd"):
	ret_mq5 = rrdtool.create("mq5_sensor.rrd", "--no-overwrite", "--step", "30", "--start", '0',
	 "DS:sensor_value:GAUGE:300:U:U",
	 "RRA:AVERAGE:0.5:1:600",
	 "RRA:AVERAGE:0.5:6:700",
	 "RRA:AVERAGE:0.5:24:775",
	 "RRA:AVERAGE:0.5:288:797",
	 "RRA:MAX:0.5:1:600",
	 "RRA:MAX:0.5:6:700",
	 "RRA:MAX:0.5:24:775",
	 "RRA:MAX:0.5:444:797")
if not os.path.isfile("mq9_sensor.rrd"):
	ret_mq9 = rrdtool.create("mq9_sensor.rrd", "--no-overwrite", "--step", "30", "--start", '0',
	 "DS:sensor_value:GAUGE:300:U:U",
	 "RRA:AVERAGE:0.5:1:600",
	 "RRA:AVERAGE:0.5:6:700",
	 "RRA:AVERAGE:0.5:24:775",
	 "RRA:AVERAGE:0.5:288:797",
	 "RRA:MAX:0.5:1:600",
	 "RRA:MAX:0.5:6:700",
	 "RRA:MAX:0.5:24:775",
	 "RRA:MAX:0.5:444:797")
if not os.path.isfile("water_sensor.rrd"):
	ret_water1 = rrdtool.create("water_sensor.rrd", "--no-overwrite", "--step", "30", "--start", '0',
	 "DS:sensor_value:GAUGE:300:U:U",
	 "RRA:AVERAGE:0.5:1:600",
	 "RRA:AVERAGE:0.5:6:700",
	 "RRA:AVERAGE:0.5:24:775",
	 "RRA:AVERAGE:0.5:288:797",
	 "RRA:MAX:0.5:1:600",
	 "RRA:MAX:0.5:6:700",
	 "RRA:MAX:0.5:24:775",
	 "RRA:MAX:0.5:444:797")

if args.nolcd:
    setRGB(0,0,0)
    setText("")
if not args.nolcd:
    setRGB(0,255,0)
    setText("Initalizing Sensors...")
    time.sleep(2)

# The sensitivity can be adjusted by the onboard potentiometer

alarm = 0
# Connect the Grove HCHO Sensor to analog port A0
# SIG,NC,VCC,GND
hcho_sensor = 2
mq9_gas_sensor = 0
mq5_gas_sensor = 1
#aq_sensor = 1
# Connect the Grove Water Sensor to digital port D2
water_sensor = 0
buzzer = 2

grovepi.pinMode(hcho_sensor,"INPUT")
grovepi.pinMode(mq9_gas_sensor,"INPUT")
#grovepi.pinMode(aq_sensor,"INPUT")
grovepi.pinMode(mq5_gas_sensor,"INPUT")
grovepi.pinMode(buzzer,"OUTPUT")

if not args.nolcd:
    setRGB(0,0,0)
    setText("")

# Vcc of the grove interface is normally 5v
grove_vcc = 5

while True:
    try:
	counter = counter + 1
	if not args.nolcd:
            setRGB(0,0,200)
            setText("Polling Sensors...Iteration: %d" % (counter))
            time.sleep(3)
        # Get sensor value
        hcho_sensor_value = grovepi.analogRead(hcho_sensor)
	grovepi.pinMode(water_sensor,"INPUT")
        mq9_sensor_value = grovepi.analogRead(mq9_gas_sensor)
        #aq_sensor_value = grovepi.analogRead(aq_sensor)
        mq5_sensor_value = grovepi.analogRead(mq5_gas_sensor)
	## uncomment below to enable water monitoring ##
	#water_value = grovepi.digitalRead(water_sensor)
	water_value = 1
	

        # Calculate voltage
        voltage = (float)(hcho_sensor_value * grove_vcc / 1024)
        # Calculate gas density - large value means more dense gas
        mq9_density = (float)(mq9_sensor_value / 1024)
        mq5_density = (float)(mq5_sensor_value / 1024)

	if not args.quiet:
	    print "###########################################################"
	    print "Environmental Sensor Results - Interation %d" % (counter)
	    print "###########################################################"
            print "HCHO: sensor_value =", hcho_sensor_value
            print "Water:", water_value
            print "CO/LPG/CH4: density =", mq9_density
#            print "AIR:", aq_sensor_value
            print "MQ5: density =", mq5_density
            # print "CO/LPG/CH4: sensor_value =", mq9_sensor_value, " density =", mq9_density
	if not args.nolcd:
	    setRGB(0,255,0)
	    setText("CO:%d VOC:%d MQ5:%d" % (mq9_density, hcho_sensor_value, mq5_density))

	from rrdtool import update as rrd_update
#	ret_aq = rrd_update('aq_sensor.rrd', 'N:%s' %(aq_sensor_value));	
	ret_hcho = rrd_update('hcho_sensor.rrd', 'N:%s' %(hcho_sensor_value));	
	ret_mq9 = rrd_update('mq9_sensor.rrd', 'N:%s' %(mq9_sensor_value));	
	ret_mq5 = rrd_update('mq5_sensor.rrd', 'N:%s' %(mq5_sensor_value));	
	ret_water1 = rrd_update('water_sensor.rrd', 'N:%s' %(water_value));	

	if water_value == 0:
		alarm = 1
		if not args.nolcd:
		    setText("Water detected!")
    		    for c in range(0,255):
        		setRGB(255,255-c,255-c)
        		time.sleep(.01)
	if mq9_density > 2:
		alarm = 1
		if not args.nolcd:
		    setText("combustible gas detected!")
    		    for c in range(0,255):
        		setRGB(255,255-c,255-c)
        		time.sleep(.01)
	if mq5_density > 2:
		alarm = 1
		if not args.nolcd:
		    setText("combustible gas detected!")
 		    for c in range(0,255):
        		setRGB(255,255-c,255-c)
        		time.sleep(.01)
	#if aq_sensor_value > 300:
	#	alarm = 0
	#	if not args.nolcd:
	#	    setText("air pollution detected!")
    	#	    for c in range(0,255):
        #		setRGB(255,255-c,255-c)
        #		time.sleep(.01)
	if hcho_sensor_value > 2:
		alarm = 1
		if not args.nolcd:
		    setText("VOC particulates detected!")
    		    for c in range(0,255):
        		setRGB(255,255-c,255-c)
        		time.sleep(.01)
	if alarm == 1:
		alarmrepeat = 0
		while alarmrepeat <= 5:
			grovepi.digitalWrite(buzzer,1)
			time.sleep(1)
			grovepi.digitalWrite(buzzer,0)
			time.sleep(1)
			alarmrepeat = alarmrepeat + 1
		grovepi.digitalWrite(buzzer,0)
        time.sleep(30)

    except KeyboardInterrupt:
        setText("")
        setRGB(0,0,0)

    except IOError:
        print "Error"
        setText("")
        setRGB(0,0,0)
