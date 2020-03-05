#!/usr/bin/python2
from __future__ import print_function
import sys
import cv2
import time
import rospy
import numpy as np
from std_msgs.msg import Int32
from std_msgs.msg import Int16MultiArray

#Image Transfer
from std_msgs.msg import String
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage
#from cv_bridge import CvBridge, CvBridgeError

class vision:
    def __init__(self, caparg):
        ## ----------- CAMERA IITIALIZATION -----------------
        self.linePub = rospy.Publisher("jt_vision_bw_contours_cx", Int16MultiArray, queue_size=1)
        self.bPub = rospy.Publisher("jt_vision_bw_countour_maxarea", Int32, queue_size=1)
        self.r = rospy.Rate(60)
        self.cap = caparg

        #Image Transfer
        self.image_pub = rospy.Publisher("jt_vision_bw_image", CompressedImage, queue_size=1)
        #self.bridge = CvBridge()

        if not(self.cap.isOpened()):
            print("VISION: Error - Could not open camera")

        ## ---------- MAIN LOOP --------------
        # Images are pulled from camera, features are extracted and published to ROS network
        cx = Int16MultiArray()
        while(not rospy.is_shutdown()):
            maskedImage = self.getMaskedImage()

            ## Image Transfer
            scale_percent = 5 # percent of original size
            width = int(maskedImage.shape[1] * scale_percent / 100)
            height = int(maskedImage.shape[0] * scale_percent / 100)
            dim = (width, height)
            #resize image
            maskedImage_resized = cv2.resize(maskedImage, dim, interpolation = cv2.INTER_AREA)
            #self.image_pub.publish(self.bridge.cv2_to_imgmsg(maskedImage_resized, "mono8")
            msg = CompressedImage()
            msg.header.stamp = rospy.Time.now()
            msg.format = "jpeg"
            msg.data = np.array(cv2.imencode('.jpg', maskedImage_resized)[1]).tostring()
            #Publish new image
            self.image_pub.publish(msg)

            ## Functionality
            cx.data = self.findLine(maskedImage)
            M = self.lookForWorkspaceBoundary(maskedImage)
            self.linePub.publish(cx)
            self.bPub.publish(M)
            self.r.sleep()

    def getMaskedImage(self):
        ## Get Frame
        ref=self.cap.grab()
        ret, frame = self.cap.retrieve(ref)
        resizedFrame = cv2.resize(frame, (int(320), int(480/2)), interpolation = cv2.INTER_AREA)

        # Convert to Grayscale, Gaussian Blur, and Threshold
        gray = cv2.cvtColor(resizedFrame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),0)
        ret,thresh1 = cv2.threshold(blur,100,255,cv2.THRESH_BINARY_INV)

        # Erode to Eliminate Noise, Dilate to Restore Eroded parts of Image
        mask = cv2.erode(thresh1, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        return mask

    def findLine(self, mask):
        ## Create Regions Of Interests (ROI)
        h, w = mask.shape
        maskCloser = mask[int(2*h/3):int(h), 0:w]
        maskFarther = mask[int(1*h/3):int(2*h/3), 0:w]

        ## Find all contours in frame: Close Contour and Farther Counter
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
        return cx

    def lookForWorkspaceBoundary(self, mask):
        ## Create Regions Of Interest (ROI)
        h, w = mask.shape
        maskCloser = mask[int(3*h/5):int(h), 0:w]

        # Find all contours in ROI
        something, contours, hierarchy = cv2.findContours(maskCloser.copy(), 1, cv2.CHAIN_APPROX_NONE)
        if len(contours) > 0:
            # Find largest contour area and image moments
            c = max(contours, key = cv2.contourArea)
            M = int(cv2.contourArea(c))
        else:
            M = 0
        return M*2

def main(args):
    rospy.init_node('jt_vision_node', anonymous=True)
    cap = cv2.VideoCapture(0)
    vis = vision(cap)
    cap.release()
    print("VISION: Exiting")

if __name__ == '__main__':
    main(sys.argv)
