import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

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
except KeyboardInterrupt:
    GPIO.cleanup()
GPIO.cleanup()
