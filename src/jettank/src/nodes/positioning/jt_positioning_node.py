#!/usr/bin/python3
# Resources:
#https://www.jetsonhacks.com/2019/07/22/jetson-nano-using-i2c/
#https://learn.adafruit.com/adafruit-mma8451-accelerometer-breakout/python-circuitpython
import board
import busio
import adafruit_mma8451
import time

import sys
import rospy
import numpy as np
from geometry_msgs.msg import Accel
from std_msgs.msg import Float32

class positioning:
    def __init__(self):
        self.r = rospy.Rate(60)

        self.accel_pub = rospy.Publisher("jt_positioning_acceleration", Accel, queue_size=1)
        self.orientation_pub = rospy.Publisher("jt_positioning_orientation", Float32, queue_size=1)

        i2c = busio.I2C(board.SCL, board.SDA)
        #i2c_bus0=(busio.I2C(board.SCL_1, board.SDA_1))
        self.sensor = adafruit_mma8451.MMA8451(i2c)

        ## ---------- MAIN LOOP --------------
        # Data is read from accelerometer and transmitted on ROS
        while(not rospy.is_shutdown()):
            a = Accel()
            x, y, z = self.sensor.acceleration
            a.linear.x = x
            a.linear.y = y
            a.linear.z = z
            o = self.sensor.orientation
            self.accel_pub.publish(a)
            self.orientation_pub.publish(o)
            self.r.sleep()

def main(args):
    rospy.init_node('jt_positioning_node', anonymous=True)
    pose = positioning()
    print("POSITIONING: Exiting")

if __name__ == '__main__':
    main(sys.argv)
