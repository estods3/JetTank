import cv2
#import Jetson.GPIO as GPIO
import time
import keyboard
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup([11,12,31,32], GPIO.OUT, initial=GPIO.LOW)


#cap = cv2.VideoCapture(0)
#if not(cap.isOpened()):
#    print("Could not open camera")

while(1):
    time.sleep(2)
    #ret, frame = cap.read()
    # convert to grayscale, gaussian blur, and threshold
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #blur = cv2.GaussianBlur(gray,(5,5),0)
    #cv2.imwrite("a.jpg", blur)
    #ret,thresh1 = cv2.threshold(blur,100,255,cv2.THRESH_BINARY_INV)
    #cv2.imwrite("b.jpg", thresh1)
    # Erode to eliminate noise, Dilate to restore eroded parts of image
    #mask = cv2.erode(thresh1, None, iprint("1"
    if keyboard.is_pressed('q'):
        print("end")
        break

#cap.release()
print("Done")
