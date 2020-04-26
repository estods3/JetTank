#!/usr/bin/env python2
import sys
import rospy
import cv2
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage
#from cv_bridge import CvBridge, CvBridgeError

class image_converter:
    def __init__(self):
        #self.bridge = CvBridge()
        #self.image_sub = rospy.Subscriber("jt_vision_bw_image", CompressedImage, self.callback, queue_size=1)
        self.image_sub = rospy.Subscriber("/camera/image_raw", CompressedImage, self.callback, queue_size=1)

    def callback(self, data):
        ## Get Image
        try:
            #img = self.bridge.imgmsg_to_cv2(data, "mono8")
            np_arr = np.fromstring(data.data, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
        except CvBridgeError as e:
            print(e)

        ## Upscale Image Size
        scale_percent = 100 * 20 # percent of original size
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
