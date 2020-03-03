#!/usr/bin/env python2
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
class image_converter:
    def __init__(self):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("jt_vision_bw_image", Image, self.callback)

    def callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        (rows,cols,channels) = cv_image.shape
        if cols > 60 and rows > 60 :
            cv2.circle(cv_image, (50,50), 10, 255)
        cv2.imshow("Command Center Video Feed", cv_image)
        cv2.waitKey(3)

def main(args):
    ic = image_converter()
    rospy.init_node('pc_command_center_video_viewer_node', anonymous=True)
    rospy.spin()
    print("--- Video Viewer Node Shutting down ---")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
