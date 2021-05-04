#!/usr/bin/env python
from __future__ import print_function
import os
import time
import sys
import rospy
import cv2
import numpy as np

from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import String, UInt16, UInt8
from sensor_msgs.msg import Image
from panel.msg import Sticks


datax = " "
datay = " "
dataz = 20000
tofd = 0
scale=50

mode = 0

class image_converter:

    def __init__(self):
        self.image_pub = rospy.Publisher("image_topic_2",Image,queue_size=10)

        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/usb_cam/image_raw",Image,self.callback)
        rospy.Subscriber("sticks", Sticks, callback0) #String or Sticks
        rospy.Subscriber("tof_data", UInt16, callback1) #String or Sticks
        rospy.Subscriber('button_value', UInt8, button_callback)
        self.old_tofd = 0
    def callback(self,data):
        global scale, mode
        
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        width = cv_image.shape[1]
        height = cv_image.shape[0]
        centerX,centerY=int(height/2),int(width/2)
        # set coordinates
        radiusX,radiusY= int(scale*height/100),int(scale*width/100)
        minX,maxX=centerX-radiusX,centerX+radiusX
        minY,maxY=centerY-radiusY,centerY+radiusY

        cropped = cv_image[minX:maxX, minY:maxY]
        resized_cropped = cv2.resize(cropped, (int(width), int(height)))
        width_re = resized_cropped.shape[1]
        height_re = resized_cropped.shape[0]
        tip_woffset = 50
        tip_hoffset = 100
        if mode == 0:
            self.old_tofd = tofd

        if (tofd > 0):
            # put text
            cv2.putText(resized_cropped,"depth: " + str(self.old_tofd), (width_re//2 + 20+tip_woffset ,height_re//2+20+tip_hoffset), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0,255,255), thickness=1)
            cv2.line(resized_cropped, (width_re//2-10+tip_woffset,height_re//2+tip_hoffset), (width_re//2+10+tip_woffset,height_re//2+tip_hoffset), (0,255,0), thickness=2)
            cv2.line(resized_cropped, (width_re//2+tip_woffset,height_re//2-10+tip_hoffset), (width_re//2+tip_woffset,height_re//2+10+tip_hoffset), (0,255,0), thickness=2)
            cv2.circle(resized_cropped, (width_re//2+tip_woffset,height_re//2+tip_hoffset), 20, (0,255,0), thickness=2)
        else:
            cv2.putText(resized_cropped,"PREPARING...", (resized_cropped.shape[1]//2-20, resized_cropped.shape[0]//2), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0,255,255), thickness=1)
        

        cv2.namedWindow("camera", cv2.WND_PROP_FULLSCREEN)

        cv2.setWindowProperty("camera",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        cv2.imshow("camera", resized_cropped)


        key = cv2.waitKey(1)

        if (dataz > 21500 or key == 119):
            # zoom in
            scale -= 1  
        elif (dataz < 18500 or key == 115):
            # zoom out
            scale += 1  
        else:
            scale = scale

        if(scale > 50):
            scale = 50

        if(scale == 0):
            scale = 1
        if (key == 113):
            # quit q
            rospy.signal_shutdown("tokyo shut down")
            

        try:
            self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
        except CvBridgeError as e:
            print(e)

def callback0(data):

	global datax
	global datay
	global dataz
	datax = data.x
	datay = data.y
	dataz = data.z


def callback1(data):
	global tofd

	tofd = data.data

def button_callback(msg): 
    global mode
    button_value = msg.data
    if button_value ==1:
        mode = 1
    



def main(args):
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True, disable_signals=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
