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
switch_state = "0000"  #up, down, left, right

class image_converter:

    def __init__(self):
        self.image_pub = rospy.Publisher("image_topic_2",Image,queue_size=10)

        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/usb_cam/image_raw",Image,self.callback)
        rospy.Subscriber("sticks", Sticks, stick_callback) #String or Sticks
        rospy.Subscriber("tof_data", UInt16, tof_callback) #String or Sticks
        rospy.Subscriber('button_value', UInt8, button_callback)
        rospy.Subscriber('limit_switch_state', String, limit_switch_callback)
        self.old_tofd = 0
    def callback(self,data):
        global scale, mode, switch_state
        global dataz
        
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
        # working space button parameter setting
        button_left  = np.array([[0, 160], [0, 320], [30, 270], [30, 210]], np.int32)
        button_right  = np.array([[640, 160], [640, 320], [610, 270], [610, 210]], np.int32)
        button_up  = np.array([[240, 0], [400, 0], [350,30], [290, 30]], np.int32)
        button_down  = np.array([[240, 480], [400, 480], [350, 450], [290, 450]], np.int32)

        color_searching = (10,255,0)
        color_swabing = (0,0,255)


        if mode == 0:
            self.old_tofd = tofd
            up_color = color_searching
            down_color = color_searching
            left_color = color_searching
            right_color = color_searching
            info_color = color_searching
            swabing_info = "Searching Target..."
        else:
            up_color = color_swabing
            down_color = color_swabing
            left_color = color_swabing
            right_color = color_swabing
            info_color = color_swabing
            swabing_info = "Swabing......"

        if switch_state != "0000":
            info_color = color_swabing
            if switch_state == "1000":
                up_color = color_swabing
                swabing_info = "Up limit"
            elif switch_state == "0100":
                down_color = color_swabing
                swabing_info = "Down limit"
            elif switch_state == "0010":
                left_color = color_swabing
                swabing_info = "Left limit"
            elif switch_state == "0001":
                right_color = color_swabing
                swabing_info = "Right limit"

        if (tofd > 0):
            # put text
            cv2.line(resized_cropped, (width_re//2-10+tip_woffset,height_re//2+tip_hoffset), (width_re//2+10+tip_woffset,height_re//2+tip_hoffset), info_color, thickness=2)
            cv2.line(resized_cropped, (width_re//2+tip_woffset,height_re//2-10+tip_hoffset), (width_re//2+tip_woffset,height_re//2+10+tip_hoffset), info_color, thickness=2)
            cv2.circle(resized_cropped, (width_re//2+tip_woffset,height_re//2+tip_hoffset), 20, (0,255,0), thickness=2)
            # draw the working space button

            cv2.fillPoly(resized_cropped, [button_up], up_color)
            cv2.fillPoly(resized_cropped, [button_down], down_color)
            cv2.fillPoly(resized_cropped, [button_left], left_color)
            cv2.fillPoly(resized_cropped, [button_right], right_color)
            cv2.rectangle(resized_cropped,(500,400),(640,480),(255,255,255),-1)
            cv2.rectangle(resized_cropped,(500,400),(640,480),info_color,2)
            cv2.putText(resized_cropped, swabing_info, (500,400), cv2.FONT_HERSHEY_PLAIN,1, info_color, 1, cv2.LINE_AA)

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

def stick_callback(data):

	global datax
	global datay
	global dataz
	datax = data.x
	datay = data.y
	dataz = data.z


def tof_callback(data):
	global tofd

	tofd = data.data

def button_callback(msg): 
    global mode
    button_value = msg.data
    mode = button_value

def limit_switch_callback(msg): 
    global switch_state
    button_value = msg.data
    switch_state = button_value



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
