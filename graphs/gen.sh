#!/bin/bash

rrdtool xport -s now-3h -e now --step 300 \
DEF:a=/home/pi/mprobe/hcho_sensor.rrd:sensor_value:AVERAGE \
DEF:b=/home/pi/mprobe/mq5_sensor.rrd:sensor_value:AVERAGE \
DEF:c=/home/pi/mprobe/mq9_sensor.rrd:sensor_value:AVERAGE \
DEF:d=/home/pi/mprobe/aq_sensor.rrd:sensor_value:AVERAGE \
XPORT:a:"HCHO" \
XPORT:b:"MQ5" \
XPORT:c:"MQ9" \
XPORT:d:"AQ" > sensors3h.xml
