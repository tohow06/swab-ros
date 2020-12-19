#! /usr/bin/env python
import rospy
from std_msgs.msg import String, Int16
from sensor_msgs.msg import Joy
import os
import json
count2 = 0     #mode 
count = 0      #mode 0~1
mode = 0
diff = 1       #1~9

other_mode = 0

HZ=4

def mode_callback(msg):
    global other_mode
    other_mode = msg.data


def joy_remapping(msg):
    global count, mode, diff, count2
    buttons = msg.buttons
    axes = msg.axes
    axes = map(lambda x:int(x*15),axes)  
    LR,UD,_,_,_,_,_,_ = axes
    A,B,X,Y,LB,RB,back,start,_,_,_=buttons       
    if back == 1:        ## press back to shutdown
    	p = os.popen('shutdown now')
    
    rate = rospy.Rate(HZ)
    
    if LR>0:
    	left=LR
    	right=0
    else:
   	left=0
   	right=-LR
    if UD>0:
        up=UD*2
   	down=0
    else:
   	up=0
   	down=-UD
    spin=X
    front=A
    behind=B
    rcm_en=LB
    ee_en=RB
    STOP=start
    
    cmd = "%03d*%03d*%03d*%03d*%01d*%01d*%01d*%01d*%01d*%01d*%021d" % (up,down,left,right,front,behind,spin,rcm_en,ee_en,STOP,0)        
    pub_joy.publish(cmd)
    print cmd
    rate.sleep()


 
if __name__ == '__main__':
    rospy.init_node('joy_lai')
    joy_topic = "/joy"
    gpio_topic = "/gpio"
    mode_topic = "/mode"
    pub_joy = rospy.Publisher('joy_information', String, queue_size=1)
    pub_diff = rospy.Publisher('differential', Int16, queue_size=1)
    pub_mode = rospy.Publisher('mode', Int16, queue_size=1)
    rospy.Subscriber(mode_topic, Int16, mode_callback, queue_size = 1, buff_size = 52428800)
    rospy.Subscriber(joy_topic, Joy, joy_remapping, queue_size = 1, buff_size = 52428800)
    rospy.spin()
