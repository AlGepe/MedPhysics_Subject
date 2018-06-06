#!/usr/bin/env python2.7
# Python 2.7 version by Alex Eames of http://RasPi.TV 
# functionally similar to the Gertboard motor test by 
# Gert Jan van Loo & Myra VanInwegen
# Use at your own risk - I'm pretty sure the code is harmless, check it yourself
# This is the software PWM version. It's not as good as the WiringPi
# hardware PWM version, but will get you there in a pinch.
# There is a new soft PWM feature in RPi.GPIO, so I won't be developing this
# program any further. Once RPi.GPIO hardware PWM comes out, it will be cut out

# all print statements in this prog must now be in python 3 format
from __future__ import print_function
import RPi.GPIO as GPIO
import sys
from time import sleep
board_type = sys.argv[-1]

GPIO.setmode(GPIO.BCM)
ports = [18,17]             # define which ports to be pulsed (using a list)
Reps = 1                  # Number of time the signal is sent
Hertz = 2                # Frecuencia
period = (1 / float(Hertz)) - 0.0003           # Period [I know it's confusing, don't look at me I didn't write the code, I'm just here bodging something]

for port_num in ports:                       # set the ports up for output
    GPIO.setup(port_num, GPIO.OUT)           # set up GPIO output channel
    print ("setting up GPIO port:", port_num)
    GPIO.output(port_num, False)             # set both ports to OFF
    
def run_motor(Reps, pulse_width, port_num, time_period):
    try:                                     # try: except:, traps errors
        for i in range(0, Reps):
            GPIO.output(port_num, True)      # switch port on
            sleep(pulse_width)               # make sure pulse stays on for correct time
            GPIO.output(port_num, False)     # switch port off
            sleep(time_period)               # time_period for port OFF defined in run_loop
    except KeyboardInterrupt:                # reset all ports used by this program if CTRL-C pressed
        GPIO.cleanup()

def run_loop(startloop, endloop, step, port_num, printchar):
    for pulse_width_percent in range(startloop, endloop, step):
        # print (pulse_width_percent) 
        perc = 100 * (pulse_width_percent-startloop*1.0)/(endloop-startloop)
        print (perc, sep='', end='')
        sys.stdout.flush()
        pulse_width = pulse_width_percent / float(100) * period           # define exact pulse width
        time_period = period - (period * pulse_width_percent / float(100))  # sleep period needed to get required Hz
        run_motor(Reps, pulse_width, port_num, time_period)
    print("")                                                           # print line break between runs

# Print wiring instructions
if board_type == "m":
    print ("\nThese are the connections for the Multiface motor test:")
    print ("GPIO 17 --- MOTB")
    print ("GPIO 18 --- MOTA")
    print ("+ of external power source --- MOTOR +")
    print ("ground of external power source --- MOTOR - ")
    print ("one wire for your motor in MOTOR A screw terminal")
    print ("the other wire for your motor in MOTOR B screw terminal")

else:
    print ("\nThese are the connections for the Gertboard motor test:")
    print ("GP17 in J2 --- MOTB (just above GP1)")
    print ("GP18 in J2 --- MOTA (just above GP4)")
    print ("+ of external power source --- MOT+ in J19")
    print ("ground of external power source --- GND (any)")
    print ("one wire for your motor in MOTA in J19")
    print ("the other wire for your motor in MOTB in J19")

command = raw_input("When ready hit enter.\n>")
print (">>>", sep='', end='')
print("You spin me right 'round, baby \n right 'round like record, baby \n 'round 'round 'round 'round")
for i in range(5):
	run_motor(1, .013*period, 18, 1)
print("And reverse!")
print("You spin me right 'round, baby \n right 'round like record, baby \n 'round 'round 'round 'round")
for i in range(5):
	run_motor(1, .013*period, 17, 1)
print("\n The END")

GPIO.output(port_num, False)            # Finish up: set both ports to off
GPIO.cleanup()              # reset all ports used by this program on finishing
