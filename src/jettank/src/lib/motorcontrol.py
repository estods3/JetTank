import sys
sys.path.append('/opt/nvidia/jetson-gpio/lib/python/')
sys.path.append('/opt/nvidia/jetson-gpio/lib/python/Jetson/GPIO')
import Jetson.GPIO as GPIO
from loadCalFile import loadCalFile

## ------------------ CALIBRATION --------------------
cal = loadCalFile()
motorLeftPos = int(cal[cal.index("motorLeftPositivePin") + 1])
motorLeftNeg = int(cal[cal.index("motorLeftNegativePin") + 1])
motorRightPos = int(cal[cal.index("motorRightPositivePin") + 1])
motorRightNeg = int(cal[cal.index("motorRightNegativePin") + 1])

## ------------ JETBOT MOTOR FUNCTIONS ---------------
def initializeMotorPins():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup([motorLeftPos, motorLeftNeg, motorRightPos, motorRightNeg], GPIO.OUT, initial=GPIO.LOW)

def forward():
    GPIO.output(motorRightPos, GPIO.HIGH)
    GPIO.output(motorRightNeg, GPIO.LOW)
    GPIO.output(motorLeftPos, GPIO.HIGH)
    GPIO.output(motorLeftNeg, GPIO.LOW)

def leftTurn():
    GPIO.output(motorRightPos, GPIO.HIGH)
    GPIO.output(motorRightNeg, GPIO.LOW)
    GPIO.output(motorLeftPos, GPIO.LOW)
    GPIO.output(motorLeftNeg, GPIO.LOW)

def rightTurn():
    GPIO.output(motorRightPos, GPIO.LOW)
    GPIO.output(motorRightNeg, GPIO.LOW)
    GPIO.output(motorLeftPos, GPIO.HIGH)
    GPIO.output(motorLeftNeg, GPIO.LOW)

def leftPivotTurn():
    GPIO.output(motorRightPos, GPIO.HIGH)
    GPIO.output(motorRightNeg, GPIO.LOW)
    GPIO.output(motorLeftPos, GPIO.LOW)
    GPIO.output(motorLeftNeg, GPIO.HIGH)

def rightPivotTurn():
    GPIO.output(motorRightPos, GPIO.LOW)
    GPIO.output(motorRightNeg, GPIO.HIGH)
    GPIO.output(motorLeftPos, GPIO.HIGH)
    GPIO.output(motorLeftNeg, GPIO.LOW)

def backward():
    GPIO.output(motorRightPos, GPIO.LOW)
    GPIO.output(motorRightNeg, GPIO.HIGH)
    GPIO.output(motorLeftPos, GPIO.LOW)
    GPIO.output(motorLeftNeg, GPIO.HIGH)

def stop():
    GPIO.output([motorLeftPos, motorLeftNeg, motorRightPos, motorRightNeg], GPIO.LOW)

def cleanup():
    stop()
    GPIO.cleanup()
