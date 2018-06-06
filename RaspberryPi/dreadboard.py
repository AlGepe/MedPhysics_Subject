#!/usr/bin/env python2.7
# DONT READ COMMENTS

import RPi.GPIO as GPIO
from time import sleep
import sys
board_type = sys.argv[-1]

GPIO.setmode(GPIO.BCM)                              # initialise RPi.GPIO

GPIO.setup(25, GPIO.OUT)                             # 22 normal input no pullup

if board_type == "m":
    print "It's-a-  me, Mario!"

else:
    print "It's-a-  me, Mario!"
raw_input("When ready hit enter.\n")

button_press = 0                            # set intial values for variables
previous_status = ''

try:
    GPIO.output(25, 1)
    sleep(5)
    GPIO.output(25, 0)
    sleep(5)
    for i in range(10):
        if (i % 2):
            GPIO.output(25, 1)
            sleep(1)
        else:
            GPIO.output(25, 0)
            sleep(1)
except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt
    GPIO.cleanup()                 # resets all GPIO ports
GPIO.cleanup()                     # on exit, reset  GPIO ports used by program
