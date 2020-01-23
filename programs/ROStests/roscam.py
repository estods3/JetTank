#!/usr/bin/env python
#import roslib
#roslib.load_manifest('my_package')
from __future__ import print_function
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
class image_converter:
    def __init__(self):
        self.image_pub = rospy.Publisher("image_topic_2",Image)
        self.bridge = CvBridge()
        cap = cv2.VideoCapture(1)
        if not(cap.isOpened()):
            print("Could not open camera")
        #self.image_sub = rospy.Subscriber("image_topic",Image,self.callback)
        while(1):
            ret, cv_image = cap.read()
            cv_image = cv_image[0:60, 0:60]
            (rows,cols,channels) = cv_image.shape
            if cols > 60 and rows > 60 :
                cv2.circle(cv_image, (50,50), 10, 255)

            try:
                self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
            except CvBridgeError as e:
                print(e)

    #def callback(self,data):
        #try:
        #    cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        #except CvBridgeError as e:
        #    print(e)
	#ret, cv_image = cap.read()
        #cv_image = cv_image(0:60, 0:60)
        #(rows,cols,channels) = cv_image.shape
        #if cols > 60 and rows > 60 :
        #    cv2.circle(cv_image, (50,50), 10, 255)
        #cv2.imshow("Image window", cv_image)
        #cv2.waitKey(3)

        #try:
        #    self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
        #except CvBridgeError as e:
        #    print(e)

def main(args):
    try:
        rospy.init_node('image_converterPub', anonymous=True)
        ic = image_converter()
    except(KeyboardInterrupt,SystemExit):
        print("---- Exiting ----")
        cap.release()
    #try:
    #    rospy.spin()
    #except KeyboardInterrupt:
    #    print("Shutting down")
    #cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
