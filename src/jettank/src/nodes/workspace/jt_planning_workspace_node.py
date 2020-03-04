#!/usr/bin/python3
import time
import sys
import rospy
from std_msgs.msg import Int16
from std_msgs.msg import Int32

## ------------------ CALIBRATION --------------------
#vision (center is  320x)
boundaryAreaThreshold = 2000

class workspaceMotionPlanning:
    def __init__(self):
        self.visionsub = rospy.Subscriber("jt_vision_bw_countour_maxarea", Int32, self.imageRecieved, queue_size=1)
        self.motorpub = rospy.Publisher("jt_workspace_motorcontrol_command", Int16, queue_size=1)
        self.r = rospy.Rate(60)
        self.initialTime = time.time()

    def imageRecieved(self, data):
        ## ----------------- VISION ------------------
        # determine if a boundary is present
        boundaryFound = data.data > boundaryAreaThreshold
        elapsedTime = round(time.time() - self.initialTime)

        ## -------------- TURN AROUND ----------------
        if boundaryFound:
            #print(str(elapsedTime) + "    Boundary Found!! Turning Around!!")
            self.motorpub.publish(10) #stop=10
            time.sleep(0.5)
            self.motorpub.publish(9) #backward=9
            time.sleep(0.1)

            if(elapsedTime % 2 == 0):
                #Condition 1 Motion: Right Turn
                self.motorpub.publish(7) #right=7
            else:
                #Condition 2 Motion: Left Turn
                self.motorpub.publish(6) #left=6
            time.sleep(0.8)
        else:
            self.motorpub.publish(8) #forward=8
            time.sleep(0.1)
            self.motorpub.publish(10) #stop=10
            time.sleep(0.05)
        self.r.sleep()

def main(args):
    rospy.init_node("jt_planning_workspace_node", anonymous=True)
    ws = workspaceMotionPlanning()
    rospy.spin()
    print("WORKSPACE: Exiting")

if __name__ == '__main__':
    main(sys.argv)
