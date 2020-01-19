import cv2
import time
import sys
sys.path.append('../../lib')
import motorcontrol

## ------------------ CALIBRATION --------------------
#vision (center is  320x)
boundaryAreaThreshold = 2000

## ----------------- GPIO SETUP ----------------------
motorcontrol.initializeMotorPins()

## -----------CAMERA INITIALIZATION -----------------
cap = cv2.VideoCapture(0)
if not(cap.isOpened()):
    print("Could not open camera")

def lookForWorkspaceBoundary():
    ret, frame = cap.read()
    cv2.imwrite("a.jpg", frame)
    # convert to grayscale, gaussian blur, and threshold
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    ret,thresh1 = cv2.threshold(blur,100,255,cv2.THRESH_BINARY_INV)
    # Erode to eliminate noise, Dilate to restore eroded parts of image
    mask = cv2.erode(thresh1, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    h, w = mask.shape
    maskCloser = mask[int(3*h/5):int(h), 0:w]
    cv2.imwrite("c.jpg", maskCloser)
    # Find all contours in frame: Close Contour and Farther Counter
    something, contours, hierarchy = cv2.findContours(maskCloser.copy(),1,cv2.CHAIN_APPROX_NONE)
    if len(contours) > 0:
        # Find largest contour area and image moments
        c = max(contours, key = cv2.contourArea)
        M = cv2.contourArea(c)
    else:
        M = 0
    print(M)
    return M > boundaryAreaThreshold

## MAIN LOOP
try:
    initialTime = time.time()
    while(1):
        ## ----------------- VISION ------------------
        boundaryFound = lookForWorkspaceBoundary()
        elapsedTime = round(time.time() - initialTime)

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
            time.sleep(0.1)
            motorcontrol.stop()
            print(str(elapsedTime) + "    Going Straight!!")

except(KeyboardInterrupt,SystemExit):
    print("---- Exiting ----")
    cap.release()
    cv2.destroyAllWindows()
    motorcontrol.stop()
    motorcontrol.cleanup()
    print("---- Done ----")
