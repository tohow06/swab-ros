#!/usr/bin/env python

import sys, time
#numpy and scipy
import numpy as np
# OpenCV
import cv2
import rospy
from std_msgs.msg import String
from panel.msg import Sticks

datax = " "
datay = " "
dataz = " "

class camera_interface:

    def __init__(self):
        '''Initialize ros publisher, ros subscriber'''
        rospy.init_node('camera_interface', anonymous=True)
        # subscribed Topic
        self.subscriber = rospy.Subscriber("sticks", Sticks, self.stick_callback)
        self.datax = " "
        self.datay = " "
        self.dataz = " "

        self.capture = cv2.VideoCapture(1)
        self.scale=100 #zoom scale

        self.gui()

    def stick_callback(self, data):
        self.datax = data.x
        self.datay = data.y
        self.dataz = data.z
        if (self.dataz > 14000):
            # zoom in w
            self.scale -= 5  
        elif (self.dataz < 12000):
            # zoom out s
            self.scale += 5  
        else:
            self.scale = self.scale
        if(self.scale > 50):
            self.scale = 50

        if(self.scale == 0):
            self.scale = 5
        print(self.scale)

    def gui(self):
        while not rospy.is_shutdown():
            isTrue, frame = self.capture.read()
            width = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
            height = self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
            centerX,centerY=int(height/2),int(width/2)
            # set coordinates
            radiusX,radiusY= int(self.scale * height / 100), int(self.scale * width / 100)
            minX,maxX=centerX-radiusX,centerX+radiusX
            minY,maxY=centerY-radiusY,centerY+radiusY

            cropped = frame[minX:maxX, minY:maxY]
            #cropped = frame
            resized_cropped = cv2.resize(cropped, (int(width), int(height)))

            # put text
            cv2.putText(resized_cropped,'depth', (resized_cropped.shape[1]//2 + 20 ,resized_cropped.shape[0]//2+20), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0,255,255), thickness=1)
            cv2.line(resized_cropped, (resized_cropped.shape[1]//2-10,resized_cropped.shape[0]//2),
            (resized_cropped.shape[1]//2+10,resized_cropped.shape[0]//2), (0,255,0), thickness=1)

            cv2.line(resized_cropped, (resized_cropped.shape[1]//2,resized_cropped.shape[0]//2-10),
            (resized_cropped.shape[1]//2,resized_cropped.shape[0]//2+10), (0,255,0), thickness=1)

            cv2.imshow('camera', resized_cropped)

            key = cv2.waitKey(100)
            #print(key)

            if (key == 113):
            # quit q
                self.capture.release()
                cv2.destroyAllWindows()
                rospy.signal_shutdown("tokyo shut down")
                break



def main(args):
    '''Initializes and cleanup ros node'''
    ci = camera_interface()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down ROS Image feature detector module"
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
