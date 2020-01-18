import cv2
import Jetson.GPIO as GPIO
import time

## ------------------ CALIBRATION --------------------
#motors
#motorLeftPos =
#motorLeftNeg = 
#motorRightPos = 
#motorRightNeg = 

#vision
#center is 320
thresholdLeft = 220 #lower X-values are on the left side of the screen, thus we need to turn left if the line is below this value
thresholdRight = 420 #higher X-values are on the right side of the screen, thus we need to turn right if the line is above this value
thresholdNoLineLeft = 30 #If the line is too far right, it is past this threshold to see in order to turn left
thresholdNoLineRight = 600 #If the line is too far left, it is past this threshold to see in order to turn right
movingAverageLength = 1

## ----------------- GPIO SETUP ----------------------
GPIO.setmode(GPIO.BOARD)
GPIO.setup([15,12,31,32], GPIO.OUT, initial=GPIO.LOW)

## -----------CAMERA INITIALIZATION -----------------
cap = cv2.VideoCapture(0)
if not(cap.isOpened()):
    print("Could not open camera")

## MAIN LOOP
try:
    movingaverage = [thresholdRight - thresholdLeft] * movingAverageLength
    initialTime = time.time()
    while(1):

        ret, frame = cap.read()
        ## ----------------- VISION ----------------------
        # convert to grayscale, gaussian blur, and threshold
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),0)
        cv2.imwrite("a.jpg", blur)
        ret,thresh1 = cv2.threshold(blur,100,255,cv2.THRESH_BINARY_INV)
        cv2.imwrite("b.jpg", thresh1)
        # Erode to eliminate noise, Dilate to restore eroded parts of image
        mask = cv2.erode(thresh1, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        h, w = mask.shape
        maskCloser = mask[int(2*h/3):int(h), 0:w]
        maskFarther = mask[int(1*h/3):int(2*h/3), 0:w]
        cv2.imwrite("c.jpg", maskCloser)
        # Find all contours in frame: Close Contour and Farther Counter
        something, contoursClose, hierarchy = cv2.findContours(maskCloser.copy(),1,cv2.CHAIN_APPROX_NONE)
        something, contoursFarther, hierarchy = cv2.findContours(maskFarther.copy(),1,cv2.CHAIN_APPROX_NONE)

        # Find x-axis centroid of largest contour and cut power to appropriate motor
        # to recenter camera on centroid.
        # This control algorithm was written referencing guide:
        # Author: Einsteinium Studios
        # Availability: http://einsteiniumstudios.com/beaglebone-opencv-line-following-robot.html
        if len(contoursClose) > 0:
            # Find largest contour area and image moments
            c = max(contoursClose, key = cv2.contourArea)
            M = cv2.moments(c)
            # Find x-axis centroid using image moments
            try:
                cx = int(M['m10']/M['m00'])
                movingaverage.insert(0, cx)
                movingaverage.pop()
            except(ZeroDivisionError):
                cx = 0
                print("division by zero")
            av = sum(movingaverage)/len(movingaverage)
            elapsedTime = time.time() - initialTime
            turnsleeptime = (abs((av - (thresholdRight - thresholdLeft))/(thresholdRight - thresholdLeft)) * 0.005) + 0.005

            if av < thresholdNoLineRight and av >= thresholdRight:
                #Condition 1 Motion: Right
                GPIO.output(15, GPIO.LOW)
                GPIO.output(12, GPIO.HIGH)
                GPIO.output(31, GPIO.HIGH)
                GPIO.output(32, GPIO.LOW)
                time.sleep(turnsleeptime)
                GPIO.output([15,12,31,32], GPIO.LOW)
                print(str(round(elapsedTime)) + "    Turning Right!            Avg: " + str(round(av)) + "      Last: " + str(cx))

            if av < thresholdRight and av > thresholdLeft:
                #Condition 2 Motion: Straight
                GPIO.output(15, GPIO.HIGH)
                GPIO.output(12, GPIO.LOW)
                GPIO.output(31, GPIO.HIGH)
                GPIO.output(32, GPIO.LOW)
                time.sleep(0.03)
                GPIO.output([15,12,31,32], GPIO.LOW)
                print(str(round(elapsedTime)) + "    Going Straight!!          Avg: " + str(round(av)) + "      Last: " + str(cx))

            if av > thresholdNoLineLeft and av <= thresholdLeft:
                #Condition 3 Motion: Left
                GPIO.output(15, GPIO.HIGH)
                GPIO.output(12, GPIO.LOW)
                GPIO.output(31, GPIO.LOW)
                GPIO.output(32, GPIO.HIGH)
                time.sleep(turnsleeptime + 0.005)
                GPIO.output([15,12,31,32], GPIO.LOW)
                print(str(round(elapsedTime)) + "    Turning Left!             Avg: " + str(round(av)) + "      Last: " + str(cx))

            if av >= thresholdNoLineRight or av <= thresholdNoLineLeft:
                GPIO.output([15,12,31,32], GPIO.LOW)
                if len(contoursFarther) > 0:
                    # Find largest contour area and image moments
                    c = max(contoursFarther, key = cv2.contourArea)
                    M = cv2.moments(c)
                    # Find x-axis centroid using image moments
                    try:
                        av = int(M['m10']/M['m00'])
                        print("FURTHER VALUE FOUND")
                        print(av)
                        turnsleeptime = (abs((av - (thresholdRight - thresholdLeft))/(thresholdRight - thresholdLeft)) * 0.006) + 0.0075
                        if av > thresholdRight:
                            #Condition 1 Motion: Right
                            GPIO.output(15, GPIO.LOW)
                            GPIO.output(12, GPIO.HIGH)
                            GPIO.output(31, GPIO.HIGH)
                            GPIO.output(32, GPIO.LOW)
                            time.sleep(turnsleeptime)
                            GPIO.output([15,12,31,32], GPIO.LOW)
                        if av > 1 and av < thresholdLeft:
                            #Condition 3 Motion: Left
                            GPIO.output(15, GPIO.HIGH)
                            GPIO.output(12, GPIO.LOW)
                            GPIO.output(31, GPIO.LOW)
                            GPIO.output(32, GPIO.HIGH)
                            time.sleep(turnsleeptime + 0.005)
                            GPIO.output([15,12,31,32], GPIO.LOW)
                    except(ZeroDivisionError):
                        av = 0
                        print("division by zero")
                print(str(round(elapsedTime)) + "    No More Line!             Avg: " + str(round(av)))


except(KeyboardInterrupt,SystemExit):
    print("---- Exiting ----")
    GPIO.output([15,12,31,32], GPIO.LOW)
    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()
    print("---- Done ----")
