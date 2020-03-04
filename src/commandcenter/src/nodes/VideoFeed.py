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
        self.image_sub = rospy.Subscriber("jt_vision_bw_image", Image, self.callback, queue_size=1)

    def callback(self, data):
        ## Get Image
        try:
            img = self.bridge.imgmsg_to_cv2(data, "mono8")
        except CvBridgeError as e:
            print(e)

        ## Upscale Image Size
        scale_percent = 100 * 10 # percent of original size
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        # resize image
        resizedImg = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

        ## Display Image
        cv2.imshow("Command Center Video Feed", resizedImg)
        cv2.waitKey(3)

def main(args):
    ic = image_converter()
    rospy.init_node('pc_command_center_video_viewer_node', anonymous=True)
    rospy.spin()
    print("--- Video Viewer Node Shutting down ---")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
