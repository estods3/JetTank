#!/usr/bin/python3
import time
import sys
import rospy
from std_msgs.msg import Int16

sys.path.append('../../lib')
import motorcontrol

class motorcontroller:
    def __init__(self):
        self.mode = 4 # "stop", default
        motorcontrol.initializeMotorPins()
        self.modeSub = rospy.Subscriber('cc_mode_selection', Int16, self.setModeSelectionCallback, queue_size=1)
        #self.lfsub = rospy.Subscriber()
        self.wssub = rospy.Subscriber('jt_workspace_motorcontrol_command', Int16, self.wscb, queue_size=1)
        self.rcsub = rospy.Subscriber('cc_remotecontrol_motorcontrol_command', Int16, self.rccb, queue_size=1)

    def setModeSelectionCallback(self, data):
        self.mode = data.data
        print(self.mode)
        if self.mode == 4:
            motorcontrol.stop()

    def runCommandCode(self, commandCode):
        if commandCode == 6:
            motorcontrol.leftPivotTurn()
        elif commandCode == 7:
            motorcontrol.rightPivotTurn()
        elif commandCode == 8:
            motorcontrol.forward()
        elif commandCode == 9:
            motorcontrol.backward()
        elif commandCode == 10:
            motorcontrol.stop()
        elif commandCode == 11:
            motorcontrol.leftTurn()
        elif commandCode == 12:
            motorcontrol.rightTurn()
        else:
            print("Motor Control Command Error")

    def lfcb(self, data):
        c = data.data
        if(self.mode == 1):
            self.runCommandCode(c)

    def wscb(self, data):
        c = data.data
        if(self.mode == 2):
            self.runCommandCode(c)

    def rccb(self, data):
        c = data.data
        if(self.mode == 3):
            self.runCommandCode(c)

def main(args):
    mc = motorcontroller()
    rospy.init_node("jt_motor_controller_node", anonymous=True)
    rospy.spin()
    motorcontrol.stop()
    motorcontrol.cleanup()
    print("---- motor controller node exiting ----")

if __name__ == '__main__':
    main(sys.argv)
