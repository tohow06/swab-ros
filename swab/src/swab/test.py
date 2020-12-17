#! /usr/bin/env python
import rospy
import socket
import time
import os

from std_msgs.msg import Int16, String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy


ip = '169.254.254.169'
port = 80


#source devel/setup.bash
#rosrun joy joy_node _dev_name:="Logitech Logitech Cordless RumblePad 2"


  
def CarControl_callback(msg):
    #joystick index "http://wiki.ros.org/joy"
    buttons = msg.buttons
    axes = msg.axes       
    x = buttons[0]
    Duty1=axes[1]*100
    Duty2=axes[3]*100
    
    tmp1="GET /cmd?=C01"+str(Duty1)
    tmp2="GET /cmd?=C02"+str(Duty2)
    if x == 1:
      p = os.popen('shutdown now')
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    client.send((tmp1).encode('utf-8'))
    client.close()
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    client.send((tmp2).encode('utf-8'))
    client.close()

    time.sleep(0.05);
    print Duty1
    print Duty2


if __name__ == '__main__':
   
    rospy.init_node('http')

    joy_topic = "/joy"



    rospy.Subscriber(joy_topic, Joy, CarControl_callback, queue_size = 1, buff_size = 52428800)    
    
    rospy.spin()

