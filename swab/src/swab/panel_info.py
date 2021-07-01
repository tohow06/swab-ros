#! /usr/bin/env python

# This file Subscribe '/button_value' '/sticks' '/tof_data'
# construct cmd by sticks and publish to '/joy_information'
# if button be pressed will send a series of cmd by time.sleep to execute 
# swabbing process


import rospy
from std_msgs.msg import String, UInt16, UInt8
from panel.msg import Sticks
import os
import json
import time

button_value = 0
swab_status = 0

HZ=10
tofd = 0

stepAngle = 1.8
pulse_per_sec = 160 
lead = 2
dis_per_sec = stepAngle * pulse_per_sec * lead / 360

def callback1(data):
    global tofd
    tofd = data.data
    if tofd > 150 or tofd < 90:
        tofd = 100

def button_callback(msg):
    global button_value, dis_per_sec 
    button_value = msg.data
    up=down=left=right=front=behind=spin=rcm_en=ee_en=STOP=0
    if button_value !=0:

        '''
        front=1
        cmd = "%05d*%05d*%03d*%03d*%01d*%01d*%01d*%01d*%01d*%01d*%021d" % (0,0,0,0,front,behind,spin,rcm_en,ee_en,STOP,0)        
        swab_status = 1
        pub_joy.publish(cmd)
        pub_status.publish(swab_status)

        time.sleep(0.001)

        front=0
        cmd = "%05d*%05d*%03d*%03d*%01d*%01d*%01d*%01d*%01d*%01d*%021d" % (0,0,0,0,front,behind,spin,rcm_en,ee_en,STOP,0)        
        pub_joy.publish(cmd)
'''
        ee_en=1
        spin = 20
        cmd = "%05d*%05d*%03d*%03d*%01d*%01d*%01d*%01d*%01d*%01d*%021d" % (0,0,0,0,front,behind,spin,rcm_en,ee_en,STOP,0)        
        pub_joy.publish(cmd)
'''
        time.sleep(5)

        ee_en=0
        spin=0
        cmd = "%05d*%05d*%03d*%03d*%01d*%01d*%01d*%01d*%01d*%01d*%021d" % (0,0,0,0,front,behind,spin,rcm_en,ee_en,STOP,0)        
        pub_joy.publish(cmd)

        behind=1000
        cmd = "%05d*%05d*%03d*%03d*%01d*%01d*%01d*%01d*%01d*%01d*%021d" % (0,0,0,0,front,behind,spin,rcm_en,ee_en,STOP,0)        
        pub_joy.publish(cmd)
        time.sleep(7.5)
        
        behind=0
        cmd = "%05d*%05d*%03d*%03d*%01d*%01d*%01d*%01d*%01d*%01d*%021d" % (0,0,0,0,front,behind,spin,rcm_en,ee_en,STOP,0)        
        swab_status = 0
        pub_joy.publish(cmd)
        pub_status.publish(swab_status)
        '''
def sticks_remapping(msg):
    global button_value
    up=down=left=right=front=behind=spin=rcm_en=ee_en=STOP=0

    x = msg.x
    y = msg.y
    z = msg.z  

    rate = rospy.Rate(HZ)

    if button_value == 0:
        cmd = "%05d*%05d*%03d*%03d*%01d*%01d*%01d*%01d*%01d*%01d*%021d" % (x,y,0,0,front,behind,spin,rcm_en,ee_en,STOP,0)      
        pub_joy.publish(cmd)
    rate.sleep()


 
if __name__ == '__main__':
    rospy.init_node('panel_info_process')
 
    pub_joy = rospy.Publisher('joy_information', String, queue_size=1)
    pub_status = rospy.Publisher('swab_status', UInt8, queue_size=1)

    rospy.Subscriber('button_value', UInt8, button_callback, queue_size = 1, buff_size = 52428800)
    rospy.Subscriber('sticks', Sticks , sticks_remapping, queue_size = 1, buff_size = 52428800)
    rospy.Subscriber('tof_data', UInt16, callback1)
    rospy.spin()
