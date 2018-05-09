import RPi.GPIO as GPIO
from time import sleep
 
if GPIO.RPI_REVISION == 1:                          # check Pi Revision to set port 21/27 correctly
    # define ports list for Revision 1 Pi
    ports = [25, 24, 23, 22, 21, 18, 17, 11, 10, 9, 8, 7]
else:
    # define ports list all others
    ports = [25, 24, 23, 22, 27, 18, 17, 11, 10, 9, 8, 7]   
ports_rev = ports[:]                                # make a copy of ports list
ports_rev.reverse()                                 # and reverse it as we need both
 
GPIO.setmode(GPIO.BCM)                              # initialise RPi.GPIO
 
for port_num in ports:
    GPIO.setup(port_num, GPIO.OUT)                  # set up ports for output
 
def led_drive(reps, multiple, direction):           # define led_function:
    for i in range(reps):                           # (repetitions, single/multiple, direction)
        for port_num in direction:                  
            GPIO.output(port_num, 1)                # switch on an led
            sleep(0.11)                             # wait for ~0.11 seconds
            if not multiple:                        # if we're not leaving it on
                GPIO.output(port_num, 0)            # switch it off again
 
# Print Wiring Instructions appropriate to the board
print "These are the connections for the Gertboard LEDs test:"                
print "jumpers in every out location (U3-out-B1, U3-out-B2, etc)"
print "GP25 in J2 --- B1 in J3 \nGP24 in J2 --- B2 in J3"
print "GP23 in J2 --- B3 in J3 \nGP22 in J2 --- B4 in J3"
print "GP21 in J2 --- B5 in J3 \nGP18 in J2 --- B6 in J3"
print "GP17 in J2 --- B7 in J3 \nGP11 in J2 --- B8 in J3"
print "GP10 in J2 --- B9 in J3 \nGP9 in J2 --- B10 in J3"
print "GP8 in J2 --- B11 in J3 \nGP7 in J2 --- B12 in J3" 
 
raw_input("When ready hit enter.\n")
 
try:                                              
    # one repetition, switching off led before next one comes on, direction: forwards
    led_drive(1, 0, ports)                  
    # one repetition, switching off led before next one comes on, direction: backwards
    led_drive(1, 0, ports_rev)
    # one repetition, leaving each led on, direction: forwards
    led_drive(1, 1, ports)
    # one repetition, leaving each led on, direction: backwards
    led_drive(1, 0, ports)        
except KeyboardInterrupt:                         # trap a CTRL+C keyboard interrupt
    GPIO.cleanup()                                # clean up GPIO ports on CTRL+C
GPIO.cleanup()                                    # clean up GPIO ports on normal exit