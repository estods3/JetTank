#!/usr/bin/python3
import sys
import cv2
import time
import rospy
from std_msgs.msg import Int32
from std_msgs.msg import Int16MultiArray

class vision:
    def __init__(self, caparg):
        ## ----------- CAMERA IITIALIZATION -----------------
        #self.linePub = rospy.Publisher("jt_vision_bw_contours_cx", Int16MultiArray)
        self.bPub = rospy.Publisher("jt_vision_bw_countour_maxarea", Int32, queue_size=5)
        self.r = rospy.Rate(60)
        self.cap = caparg
        if not(self.cap.isOpened()):
            print("Could not open camera")

        ## ---------- MAIN LOOP --------------
        #cx = Int16MultiArray()
        #M = Int16()
        while(not rospy.is_shutdown()):
            maskedImage = self.getMaskedImage()
            #cx.data = self.findLine(maskedImage)
            M = self.lookForWorkspaceBoundary(maskedImage)
            #TODOself.linePub.publish(cx)
            self.bPub.publish(M)
            self.r.sleep()

    def getMaskedImage(self):
        while(True):
            prev_time=time.time()
            ref=self.cap.grab()
            if (time.time()-prev_time)>0.030:#something around 33 FPS
                break
        ret, frame = self.cap.retrieve(ref)
        # convert to grayscale, gaussian blur, and threshold
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),0)
        #cv2.imwrite("a.jpg", blur)
        ret,thresh1 = cv2.threshold(blur,100,255,cv2.THRESH_BINARY_INV)
        #cv2.imwrite("b.jpg", thresh1)
        # Erode to eliminate noise, Dilate to restore eroded parts of image
        mask = cv2.erode(thresh1, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        return mask

    def findLine(self, mask):
        h, w = mask.shape
        maskCloser = mask[int(2*h/3):int(h), 0:w]
        maskFarther = mask[int(1*h/3):int(2*h/3), 0:w]
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
                    #print("division by zero")
        return cx

    def lookForWorkspaceBoundary(self, mask):
        h, w = mask.shape
        maskCloser = mask[int(3*h/5):int(h), 0:w]
        # Find all contours in close mask
        something, contours, hierarchy = cv2.findContours(maskCloser.copy(),1,cv2.CHAIN_APPROX_NONE)
        if len(contours) > 0:
            # Find largest contour area and image moments
            c = max(contours, key = cv2.contourArea)
            M = int(cv2.contourArea(c))
        else:
            M = 0
        return M

def main(args):
    rospy.init_node('jt_vision_node', anonymous=True)
    cap = cv2.VideoCapture(0)
    vis = vision(cap)
    cap.release()
    print("--- vision node exiting ---")

if __name__ == '__main__':
    main(sys.argv)
