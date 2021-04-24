#! /usr/bin/env python
import rospy
from std_msgs.msg import String, Int16, UInt8
from panel.msg import Sticks
import os
import json
import time

HZ=4



def button_callback(msg):
    button_value = msg.data
    up=down=left=right=front=behind=spin=rcm_en=ee_en=STOP=0
    if button_value == 1:
        #go forward
        ee_en = 1
        front = 50
        spin = 20
        cmd = "%03d*%03d*%03d*%03d*%01d*%01d*%01d*%01d*%01d*%01d*%021d" % (up,down,left,right,front,behind,spin,rcm_en,ee_en,STOP,0)
        pub_joy.publish(cmd)
        time.sleep(5)
        #stay and swab
        front = 0
        cmd = "%03d*%03d*%03d*%03d*%01d*%01d*%01d*%01d*%01d*%01d*%021d" % (up,down,left,right,front,behind,spin,rcm_en,ee_en,STOP,0)
        pub_joy.publish(cmd)
        time.sleep(5)
        #go backward
        behind = 50
        spin = 0
        cmd = "%03d*%03d*%03d*%03d*%01d*%01d*%01d*%01d*%01d*%01d*%021d" % (up,down,left,right,front,behind,spin,rcm_en,ee_en,STOP,0)
        pub_joy.publish(cmd)
        time.sleep(5)
        # stay
        behind = 0
        cmd = "%03d*%03d*%03d*%03d*%01d*%01d*%01d*%01d*%01d*%01d*%021d" % (up,down,left,right,front,behind,spin,rcm_en,ee_en,STOP,0)
        
        pub_joy.publish(cmd)
    


def sticks_remapping(msg):
	
    up=down=left=right=front=behind=spin=rcm_en=ee_en=STOP=0

    x = msg.x
    y = msg.y
    z = msg.z  

    rate = rospy.Rate(HZ)

    
    cmd = "%05d*%05d*%03d*%03d*%01d*%01d*%01d*%01d*%01d*%01d*%021d" % (x,y,0,0,front,behind,spin,rcm_en,ee_en,STOP,0)        
    pub_joy.publish(cmd)
    rate.sleep()

 
if __name__ == '__main__':
    rospy.init_node('panel_info_process')
 
    pub_joy = rospy.Publisher('joy_information', String, queue_size=1)

    rospy.Subscriber('button_value', UInt8, button_callback, queue_size = 1, buff_size = 52428800)
    rospy.Subscriber('sticks', Sticks , sticks_remapping, queue_size = 1, buff_size = 52428800)
    rospy.spin()
