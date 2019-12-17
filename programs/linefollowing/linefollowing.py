import cv2
import Jetson.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup([11,12,31,32], GPIO.OUT, initial=GPIO.LOW)


cap = cv2.VideoCapture(0)
if not(cap.isOpened()):
    print("Could not open camera")

while(1):

    ret, frame = cap.read()
    
    # convert to grayscale, gaussian blur, and threshold
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    cv2.imwrite("a.jpg", blur)
    ret,thresh1 = cv2.threshold(blur,100,255,cv2.THRESH_BINARY_INV)
    cv2.imwrite("b.jpg", thresh1)
    # Erode to eliminate noise, Dilate to restore eroded parts of image
    mask = cv2.erode(thresh1, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cv2.imwrite("c.jpg", mask)
    # Find all contours in frame
    something, contours, hierarchy = cv2.findContours(mask.copy(),1,cv2.CHAIN_APPROX_NONE)

    # Find x-axis centroid of largest contour and cut power to appropriate motor
    # to recenter camera on centroid.
    # This control algorithm was written referencing guide:
    # Author: Einsteinium Studios
    # Availability: http://einsteiniumstudios.com/beaglebone-opencv-line-following-robot.html
    if len(contours) > 0:
        # Find largest contour area and image moments
        c = max(contours, key = cv2.contourArea)
        M = cv2.moments(c)
        # Find x-axis centroid using image moments
        cx = int(M['m10']/M['m00'])
        print(cx)
        if cx >= 200:
            #Condition 1 Motion: Right
            GPIO.output(11, GPIO.LOW)
            GPIO.output(12, GPIO.LOW)
            GPIO.output(31, GPIO.HIGH)
            GPIO.output(32, GPIO.LOW)
            print("1")

        if cx < 200 and cx > 95:
            #Condition 2 Motion: Straight
            GPIO.output(11, GPIO.HIGH)
            GPIO.output(12, GPIO.LOW)
            GPIO.output(31, GPIO.HIGH)
            GPIO.output(32, GPIO.LOW)
            print("2")

        if cx <= 95:
            #Condition 3 Motion: Left
            GPIO.output(11, GPIO.HIGH)
            GPIO.output(12, GPIO.LOW)
            GPIO.output(31, GPIO.LOW)
            GPIO.output(32, GPIO.LOW)
            print("3")

        if cx >= 500:
            GPIO.output([11,12,31,32], GPIO.LOW)

    if cv2.waitKey(0) & 0xFF == ord('q'):
        print("end")
        break

GPIO.output([11,12,31,32], GPIO.LOW)
cap.release()
cv2.destroyAllWindows()
print("Done")
GPIO.cleanup()
