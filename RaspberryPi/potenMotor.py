from __future__ import print_function
import RPi.GPIO as GPIO
from time import sleep
import sys
import spidev
# reload spi drivers to prevent spi failures
import subprocess
unload_spi = subprocess.Popen('sudo rmmod spi_bcm2835', shell=True, stdout=subprocess.PIPE)
start_spi = subprocess.Popen('sudo modprobe spi_bcm2835', shell=True, stdout=subprocess.PIPE)
sleep(3)


board_type = sys.argv[-1]


GPIO.setmode(GPIO.BCM)
ports = [18,17]             # define which ports to be pulsed (using a list)
Reps = 200                  # 2000 Hz cycle time, so Reps=400 is 0.1s for each percentage ON
Hertz = 2000                # Cycle time. You can tweak this, Max 3000               
Freq = (1 / float(Hertz)) - 0.0003           # run_motor loop code takes 0.0003s

for port_num in ports:                       # set the ports up for output
    GPIO.setup(port_num, GPIO.OUT)           # set up GPIO output channel
    print ("setting up GPIO port:", port_num)
    GPIO.output(port_num, False)             # set both ports to OFF

def which_channel():
    channel = raw_input("Which channel do you want to test? Type 0 or 1.\n")  # User inputs channel number
    while not channel.isdigit():                                              # Check valid user input
        channel = raw_input("Try again - just numbers 0 or 1 please!\n")      # Make them do it again if wrong
    return channel

def get_adc(channel):                                   # read SPI data from MCP3002 chip
    if ((channel > 1) or (channel < 0)):                # Only 2 channels 0 and 1 else return -1
        return -1
    r = spi.xfer2([1,(2+channel)<<6,0])  # these two lines are explained in more detail at the bottom
    ret = ((r[1]&31) << 6) + (r[2] >> 2)
    return ret 

def display(char, reps, adc_value, spaces):        # function handles the display of ##### 
    print ('\r',"{0:04d}".format(adc_value), ' ', char * reps, ' ' * spaces,'\r', sep='', end='') 
    sys.stdout.flush()

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
        print (printchar, sep='', end='')
        sys.stdout.flush()
        pulse_width = pulse_width_percent / float(100) * Freq           # define exact pulse width
        time_period = Freq - (Freq * pulse_width_percent / float(100))  # sleep period needed to get required Hz
        run_motor(Reps, pulse_width, port_num, time_period)
    print("")                                                           # print line break between runs

# Print wiring instructions
while not (channel == 1 or channel == 0):       # continue asking until answer 0 or 1 given
    channel = int(which_channel())              # once proper answer given, carry on

if board_type == "m":
    print("Let's do it")

else:
    print("Let's do it _else_")

command = raw_input("When ready hit enter.\n>")

spi = spidev.SpiDev()
spi.open(0,0)          # The Gertboard ADC is on SPI channel 0 (CE0 - aka GPIO8)

while iterations < 6000:
    adc_value = (get_adc(channel))
    reps = adc_value / 16
    spaces = 64 - reps
    display(char, reps, adc_value, spaces)
    percSignal = 2 * ((adc_value/1023.)-.5)
    pWidth = percSignal * Freq
    time_period = Freq - (Freq * percSignal)
    run_motor(Reps, pWidth, port, time_period)
    # sleep(0.05)       # need a delay so people using ssh don't get slow response
    iterations += 1   # limits length of program running to 30s [600 * 0.05]

# Max value of potentiometer is 4.7Ohm
GPIO.output(port_num, False)            # Finish up: set both ports to off
GPIO.cleanup()              # reset all ports used by this program on finishing
