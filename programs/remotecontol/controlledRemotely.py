#!/usr/bin/env python
from __future__ import print_function
import sys
import rospy
from std_msgs.msg import Int16

#Import JetTank Motor Library
sys.path.append('../../lib')
import motorcontrol

def cb(x):
    print(x)
    x = x.data
    if(x == 1):
        print("forward")
        motorcontrol.forward()
    elif(x == 2):
        print("backward")
        motorcontrol.backward()
    elif(x == 3):
        print("right")
        motorcontrol.rightPivotTurn()
    elif(x == 4):
        print("left")
        motorcontrol.leftPivotTurn()
    else:
        print("stop")
        motorcontrol.stop()

def listener():
    motorcontrol.initializeMotorPins()
    rospy.init_node('RC_CommandsSub', anonymous=True)
    rospy.Subscriber("RC_Command", Int16, cb)
    rospy.spin()
    print("closing motorcontrol")
    motorcontrol.stop()
    motorcontrol.cleanup()

if __name__ == '__main__':
    try:
        listener()
    except(KeyboardInterrupt,SystemExit):
        print("---- Exiting ----")
        motorcontrol.stop()
        motorcontrol.cleanup()
        print("---- Done ----")
