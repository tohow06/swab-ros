#! /usr/bin/env python
import rospy
from std_msgs.msg import String, Int16, UInt8
from panel.msg import Sticks
import os
import json

HZ=4

button_value =0

def button_callback(msg):
    global button_value
    button_value = msg.data

def sticks_remapping(msg):
    global button_value
	
    up=down=left=right=front=behind=spin=rcm_en=ee_en=STOP=0

    x = msg.x
    y = msg.y
    z = msg.z 
    spin = button_value    

    rate = rospy.Rate(HZ)
    
    if y < 11000:
    	up=50
    	down=0
    elif y > 15000:
   	up=0
    	down=50
    if x < 11000:
    	right=50
    	left=0
    elif x > 15000:
   	right=0
    	left=50
    
    cmd = "%03d*%03d*%03d*%03d*%01d*%01d*%01d*%01d*%01d*%01d*%021d" % (up,down,left,right,front,behind,spin,rcm_en,ee_en,STOP,0)        
    pub_joy.publish(cmd)

    print cmd
    rate.sleep()

 
if __name__ == '__main__':
    rospy.init_node('panel_info_process')
 
    pub_joy = rospy.Publisher('joy_information', String, queue_size=1)

    rospy.Subscriber('button_value', UInt8, button_callback, queue_size = 1, buff_size = 52428800)
    rospy.Subscriber('sticks', Sticks , sticks_remapping, queue_size = 1, buff_size = 52428800)
    rospy.spin()
