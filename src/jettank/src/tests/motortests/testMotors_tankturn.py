import Jetson.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup([15, 12, 31, 32], GPIO.OUT, initial=GPIO.LOW)

i = 0
while(i < 4):
    GPIO.output(31, GPIO.LOW)
    GPIO.output(32, GPIO.HIGH)
    
    GPIO.output(15, GPIO.HIGH)
    GPIO.output(12, GPIO.LOW)
    
    time.sleep(2)
    
    GPIO.output(15, GPIO.LOW)
    GPIO.output(12, GPIO.HIGH)
    
    GPIO.output(31, GPIO.HIGH)
    GPIO.output(32, GPIO.LOW)
    time.sleep(1.8)
    i = i + 1

GPIO.output([15,12,31,32], GPIO.LOW)
GPIO.cleanup()
