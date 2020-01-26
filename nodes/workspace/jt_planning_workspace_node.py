import cv2
import time
import sys
import rospy
from std_msgs.msg import Int32
from std_msgs.msg import Int16MultiArray

sys.path.append('../../lib')
import motorcontrol

## ------------------ CALIBRATION --------------------
#vision (center is  320x)
boundaryAreaThreshold = 2000

## ----------------- GPIO SETUP ----------------------
motorcontrol.initializeMotorPins()

class workspaceMotionPlanning:
    def __init__(self):
        self.visionsub = rospy.Subscriber("jt_vision_bw_countour_maxarea", Int32, self.imageRecieved)
        self.initialTime = time.time()

    def imageRecieved(self, data):
        ## ----------------- VISION ------------------
        boundaryFound = data.data > boundaryAreaThreshold
        elapsedTime = round(time.time() - self.initialTime)

        ## -------------- TURN AROUND ----------------
        if boundaryFound:
            motorcontrol.stop()
            print(str(elapsedTime) + "    Boundary Found!! Turning Around!!")
            time.sleep(0.5)
            motorcontrol.backward()
            time.sleep(0.1)

            if(elapsedTime % 2 == 0):
                #Condition 1 Motion: Right Turn
                motorcontrol.rightPivotTurn()
            else:
                #Condition 2 Motion: Left Turn
                motorcontrol.leftPivotTurn()
            time.sleep(0.8)
        else:
            motorcontrol.forward()
            time.sleep(0.2)
            motorcontrol.stop()
            print(str(elapsedTime) + "    Going Straight!!")

def main(args):
    ws = workspaceMotionPlanning()
    rospy.init_node("jt_planning_workspace_node", anonymous=True)
    rospy.spin()
    motorcontrol.stop()
    motorcontrol.cleanup()
    print("---- Exiting ----")

if __name__ == '__main__':
    main(sys.argv)
