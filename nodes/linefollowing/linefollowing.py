import time
import sys
import rospy

## ------------------ CALIBRATION --------------------
#vision (center is 320)
thresholdLeft = 220 #lower X-values are on the left side of the screen, thus we need to turn left if the line is below this value
thresholdRight = 420 #higher X-values are on the right side of the screen, thus we need to turn right if the line is above this value
thresholdNoLineLeft = 5 #If the line is too far right, it is past this threshold to see in order to turn left
thresholdNoLineRight = 635 #If the line is too far left, it is past this threshold to see in order to turn right
movingAverageLength = 2


class lineFollowingMotionPlanning:
    def __init__(self):
        self.visionsub = rospy.Subscriber("jt_vision_bw_contours_cx", )

    def imageRecieved(data):
        ## ----------------- VISION -----------------------
        # TODO - Do something with data
        #cx = findLine()

        ## --------------- MOTOR CONTROL ------------------
        elapsedTime = time.time() - initialTime
        if (len(cx) >= 1 and cx[0] > 0):
            movingaverage.insert(0, cx[0])
            movingaverage.pop()
            av = sum(movingaverage)/len(movingaverage)
            turnsleeptime = (abs((av - (thresholdRight - thresholdLeft))/(thresholdRight - thresholdLeft)) * 0.003) + 0.002
        elif (len(cx) == 2 and cx[1] > 0):
            movingaverage.insert(0, cx[1])
            movingaverage.pop()
            av = sum(movingaverage)/len(movingaverage)
            turnsleeptime = (abs((av - (thresholdRight - thresholdLeft))/(thresholdRight - thresholdLeft)) * 0.006) + 0.002
        else:
            print("NO LINE AVAILABLE: USING LAST AV VALUE")

        ## -------------- MOTOR ACTUATION ----------------
        if av < thresholdNoLineRight and av >= thresholdRight:
            #Condition 1 Motion: Right
            motorcontrol.rightPivotTurn()
            time.sleep(turnsleeptime + 0.03)
            motorcontrol.stop()
            print(str(round(elapsedTime)) + "    Turning Right!            Avg: " + str(round(av)) + "      Last: " + str(cx))

        if av < thresholdRight and av > thresholdLeft:
            #Condition 2 Motion: Forward
            motorcontrol.forward()
            time.sleep(0.05)
            motorcontrol.stop()
            print(str(round(elapsedTime)) + "    Going Straight!!          Avg: " + str(round(av)) + "      Last: " + str(cx))

        if av > thresholdNoLineLeft and av <= thresholdLeft:
            #Condition 3 Motion: Left
            motorcontrol.leftPivotTurn()
            time.sleep(turnsleeptime + 0.03)
            motorcontrol.stop()
            print(str(round(elapsedTime)) + "    Turning Left!             Avg: " + str(round(av)) + "      Last: " + str(cx))

        if av >= thresholdNoLineRight or av <= thresholdNoLineLeft:
            #Condition 4 Motion: Stop
            motorcontrol.stop()
            print(str(round(elapsedTime)) + "    Stopping!                 Avg: " + str(round(av)))

def main(args):
    movingaverage = [thresholdRight - thresholdLeft] * movingAverageLength
    initialTime = time.time()
    lf = lineFollowingMotionPlanning()
    rospy.init_node("jt_planning_linefollowing_node", anonymous=True)
    rospy.spin()
    print("---- Exiting ----")

if __name__ == '__main__':
    main(sys.argv)
