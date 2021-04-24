#!/usr/bin/env python
#license removed for brevity
#coding=utf-8
import rospy
from std_msgs.msg import String
import cv2
import numpy as np
from panel.msg import Sticks

datax = " "
datay = " "
dataz = " "


def callback(data):

	global datax
	global datay
	global dataz

	#rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.x)
	#rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.y)
	#rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.z)

	datax = data.x
	datay = data.y
	dataz = data.z




def listener():

    rospy.init_node('camera_interface', anonymous=True, disable_signals=True)

    rospy.Subscriber("sticks", Sticks, callback) #String or Sticks

    # spin() simply keeps python from exiting until this node is stopped


    capture = cv2.VideoCapture(1)

    scale=100 #zoom scale

    isTrue, frame = capture.read()
    width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

    while(True):


        isTrue, frame = capture.read()

        width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        #for debug
        #print("Image Size: %d x %d" % (width, height))

        centerX,centerY=int(height/2),int(width/2)
        # set coordinates
        radiusX,radiusY= int(scale*height/100),int(scale*width/100)
        minX,maxX=centerX-radiusX,centerX+radiusX
        minY,maxY=centerY-radiusY,centerY+radiusY

        #cropped = frame[minX:maxX, minY:maxY]
        cropped = frame
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

        if (dataz > 14000):
            # zoom in w
            scale -= 5  
        elif (dataz < 12000):
            # zoom out s
            scale += 5  
        else:
            scale = scale


        if(scale > 50):
           scale = 50

        if(scale == 0):
            scale = 5

        if (key == 113):
            # quit q
            capture.release()
            cv2.destroyAllWindows()
            rospy.signal_shutdown("tokyo shut down")
            break

    rospy.spin()


if __name__ == '__main__':

	listener()


