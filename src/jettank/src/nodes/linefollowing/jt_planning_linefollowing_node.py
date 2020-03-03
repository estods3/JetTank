#!/usr/bin/python3
import time
import sys
import rospy
from std_msgs.msg import Int16MultiArray
from std_msgs.msg import Int16

## ------------------ CALIBRATION --------------------
#vision (center is 320)
thresholdLeft = 220 #lower X-values are on the left side of the screen, thus we need to turn left if the line is below this value
thresholdRight = 420 #higher X-values are on the right side of the screen, thus we need to turn right if the line is above this value
thresholdNoLineLeft = 5 #If the line is too far right, it is past this threshold to see in order to turn left
thresholdNoLineRight = 635 #If the line is too far left, it is past this threshold to see in order to turn right
movingAverageLength = 2

class lineFollowingMotionPlanning:
    def __init__(self):
        self.visionsub = rospy.Subscriber("jt_vision_bw_contours_cx", Int16MultiArray, self.imageRecieved, queue_size=1)
        self.motorpub = rospy.Publisher("jt_linefollowing_motorcontrol_command", Int16, queue_size=1)
        self.r = rospy.Rate(60)
        self.movingaverage = [thresholdRight - thresholdLeft] * movingAverageLength
        self.initialTime = time.time()

    def imageRecieved(self, data):
        ## ----------------- VISION -----------------------
        cx = data.data

        ## --------------- MOTOR CONTROL ------------------
        elapsedTime = time.time() - self.initialTime
        if (len(cx) >= 1 and cx[0] > 0):
            self.movingaverage.insert(0, cx[0])
            self.movingaverage.pop()
            av = sum(self.movingaverage)/len(self.movingaverage)
            turnsleeptime = (abs((av - (thresholdRight - thresholdLeft))/(thresholdRight - thresholdLeft)) * 0.003) + 0.002
        elif (len(cx) == 2 and cx[1] > 0):
            self.movingaverage.insert(0, cx[1])
            self.movingaverage.pop()
            av = sum(self.movingaverage)/len(self.movingaverage)
            turnsleeptime = (abs((av - (thresholdRight - thresholdLeft))/(thresholdRight - thresholdLeft)) * 0.006) + 0.002
        else:
            print("NO LINE AVAILABLE: USING LAST AV VALUE")
            av = 0

        ## -------------- MOTOR ACTUATION ----------------
        if av < thresholdNoLineRight and av >= thresholdRight:
            #Condition 1 Motion: Right
            self.motorpub.publish(7) #right=7
            time.sleep(turnsleeptime + 0.03)
            self.motorpub.publish(10) #stop=10
            time.sleep(0.1)

        if av < thresholdRight and av > thresholdLeft:
            #Condition 2 Motion: Forward
            self.motorpub.publish(8) #forward=8
            time.sleep(0.05)
            self.motorpub.publish(10) #stop=10
            time.sleep(0.1)

        if av > thresholdNoLineLeft and av <= thresholdLeft:
            #Condition 3 Motion: Left
            self.motorpub.publish(6) #left=6
            time.sleep(turnsleeptime + 0.03)
            self.motorpub.publish(10) #stop=10
            time.sleep(0.1)

        if av >= thresholdNoLineRight or av <= thresholdNoLineLeft:
            #Condition 4 Motion: Stop
            self.motorpub.publish(10) #stop=10
            time.sleep(0.1)
        self.r.sleep()

def main(args):
    rospy.init_node("jt_planning_linefollowing_node", anonymous=True)
    lf = lineFollowingMotionPlanning()
    rospy.spin()
    print("---- Exiting ----")

if __name__ == '__main__':
    main(sys.argv)
