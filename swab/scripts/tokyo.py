#!/usr/bin/env python
#license removed for brevity
#coding=utf-8
import os
import rospy
from std_msgs.msg import String
import cv2
import numpy as np
from panel.msg import Sticks

datax = " "
datay = " "
dataz = " "
tofd = 0

def callback0(data):


	global datax
	global datay
	global dataz
	

	#rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.x)
	#rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.y)
	#rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.z)

	datax = data.x
	datay = data.y
	dataz = data.z


def callback1(data):
	global tofd
	
	tofd = data.data


def listener():

	rospy.init_node('camera_interface', anonymous=True, disable_signals=True)

	rospy.Subscriber("sticks", Sticks, callback0) #String or Sticks
	rospy.Subscriber("tof_data", UInt16, callback1) #String or Sticks





	capture = cv2.VideoCapture(-1)

	scale=25 #zoom scale

	isTrue, frame = capture.read()
	width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
	height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

	while(True):

    		isTrue, frame = capture.read()

		#for debug
		#print(isTrue)
		#print(frame)

    		width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    		height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    		#for debug
    		#print("Image Size: %d x %d" % (width, height))

    		centerX,centerY=int(height/2),int(width/2)
    		# set coordinates
    		radiusX,radiusY= int(scale*height/100),int(scale*width/100)
    		minX,maxX=centerX-radiusX,centerX+radiusX
    		minY,maxY=centerY-radiusY,centerY+radiusY

    		cropped = frame[minX:maxX, minY:maxY]
    		resized_cropped = cv2.resize(cropped, (int(width), int(height)))

    		# put text
    		cv2.putText(resized_cropped,str(todf), (resized_cropped.shape[1]//2 + 20 ,resized_cropped.shape[0]//2+20),
				 cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0,255,255), thickness=1)
    		cv2.line(resized_cropped, (resized_cropped.shape[1]//2-10,resized_cropped.shape[0]//2),
				 (resized_cropped.shape[1]//2+10,resized_cropped.shape[0]//2), (0,255,0), thickness=1)

    		cv2.line(resized_cropped, (resized_cropped.shape[1]//2,resized_cropped.shape[0]//2-10),
				 (resized_cropped.shape[1]//2,resized_cropped.shape[0]//2+10), (0,255,0), thickness=1)

		cv2.namedWindow("camera", cv2.WND_PROP_FULLSCREEN)


		cv2.setWindowProperty("camera",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    		#cv2.imshow("camera", resized_cropped)
		#fordebug
    		cv2.imshow("camera", frame)

		key = cv2.waitKey(100)
		#print(key)

    		#119 w 115 s 113 q


    		if (dataz > 14000):
      			# zoom in
        		scale -= 5  
    		elif (dataz < 12000):
        		# zoom out
        		scale += 5  
		else:
			scale = scale


    		if(scale > 50):
        		scale = 50

    		if(scale == 0):
        		scale = 5
    
		#print(scale)


    		if (key == 113):
        		# quit q
			capture.release()
			cv2.destroyAllWindows()
			rospy.signal_shutdown("tokyo shut down")
        		break



	# spin() simply keeps python from exiting until this node is stopped
	rospy.spin()



if __name__ == '__main__':

	listener()


