import cv2
import time
import sys
sys.path.append('../../lib')
import motorcontrol

## ------------------ CALIBRATION --------------------
#vision (center is 320)
thresholdLeft = 220 #lower X-values are on the left side of the screen, thus we need to turn left if the line is below this value
thresholdRight = 420 #higher X-values are on the right side of the screen, thus we need to turn right if the line is above this value
thresholdNoLineLeft = 5 #If the line is too far right, it is past this threshold to see in order to turn left
thresholdNoLineRight = 635 #If the line is too far left, it is past this threshold to see in order to turn right
movingAverageLength = 2

## ----------------- GPIO SETUP ----------------------
motorcontrol.initializeMotorPins()

## -----------CAMERA INITIALIZATION -----------------
cap = cv2.VideoCapture(0)
if not(cap.isOpened()):
    print("Could not open camera")

def findLine():
    ret, frame = cap.read()
    # convert to grayscale, gaussian blur, and threshold
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    #cv2.imwrite("a.jpg", blur)
    ret,thresh1 = cv2.threshold(blur,100,255,cv2.THRESH_BINARY_INV)
    #cv2.imwrite("b.jpg", thresh1)
    # Erode to eliminate noise, Dilate to restore eroded parts of image
    mask = cv2.erode(thresh1, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    h, w = mask.shape
    maskCloser = mask[int(2*h/3):int(h), 0:w]
    maskFarther = mask[int(1*h/3):int(2*h/3), 0:w]
    #cv2.imwrite("c.jpg", maskCloser)
    # Find all contours in frame: Close Contour and Farther Counter
    something, contoursClose, hierarchy = cv2.findContours(maskCloser.copy(),1,cv2.CHAIN_APPROX_NONE)
    something, contoursFarther, hierarchy = cv2.findContours(maskFarther.copy(),1,cv2.CHAIN_APPROX_NONE)
    cx = []
    for contours in [contoursClose, contoursFarther]:
        if len(contours) > 0:
            # Find largest contour area and image moments
            c = max(contours, key = cv2.contourArea)
            M = cv2.moments(c)
            # Find x-axis centroid using image moments
            try:
                cx.append(int(M['m10']/M['m00']))
            except(ZeroDivisionError):
                cx.append(0)
                print("division by zero")
    return cx

## MAIN LOOP
try:
    movingaverage = [thresholdRight - thresholdLeft] * movingAverageLength
    initialTime = time.time()
    while(1):

        ## ----------------- VISION -----------------------
        cx = findLine()

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
            av = 0
            print("NO LINE AVAILABLE: SWEEPING TO SEE LINE")

        ## -------------- MOTOR ACTUATION ----------------
        if av < thresholdNoLineRight and av >= thresholdRight:
            #Condition 1 Motion: Right
            motorcontrol.rightPivotTurn()
            time.sleep(turnsleeptime + 0.003)
            motorcontrol.stop()
            print(str(round(elapsedTime)) + "    Turning Right!            Avg: " + str(round(av)) + "      Last: " + str(cx))

        if av < thresholdRight and av > thresholdLeft:
            #Condition 2 Motion: Forward
            motorcontrol.forward()
            time.sleep(0.03)
            motorcontrol.stop()
            print(str(round(elapsedTime)) + "    Going Straight!!          Avg: " + str(round(av)) + "      Last: " + str(cx))

        if av > thresholdNoLineLeft and av <= thresholdLeft:
            #Condition 3 Motion: Left
            motorcontrol.leftPivotTurn()
            time.sleep(turnsleeptime + 0.008)
            motorcontrol.stop()
            print(str(round(elapsedTime)) + "    Turning Left!             Avg: " + str(round(av)) + "      Last: " + str(cx))

        if av >= thresholdNoLineRight or av <= thresholdNoLineLeft:
            #Condition 4 Motion: Stop
            motorcontrol.stop()
            print(str(round(elapsedTime)) + "    Stopping!                 Avg: " + str(round(av)))

except(KeyboardInterrupt,SystemExit):
    print("---- Exiting ----")
    cap.release()
    cv2.destroyAllWindows()
    motorcontrol.stop()
    motorcontrol.cleanup()
    print("---- Done ----")
