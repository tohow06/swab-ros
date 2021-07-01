#! /usr/bin/env python

# This file Subscribe '/joy_information' then use socket to send command to concerto
# then get limit switch status and publish it to '/limit_switch_state'
#

import socket
import time
import rospy
import roslaunch
from std_msgs.msg import Int16, String
from geometry_msgs.msg import PoseStamped
import json
from nav_msgs.msg import Path
import math
import os
import datetime
import numpy as np

#"%05.2f*%05.2f*%04.2f*%05.2f*%05.2f*%04.2f*%d*%05.2f*%05.2f*%04.2f*%02d"   57 strings

ip = '169.254.254.169'
port = 80
concerto_data = "00.00*00.00*0*00.00*00.00*00.00*0000.00*0000.00*00.00*00.00*00.00*00.00"
first_ = 0
pre_state = "go"


def joy_callback_lai(msg):
    global concerto_data
    limit_data = "0000"
    joy_data = msg.data
    print(joy_data)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    client.send(("GET /cmd?=C01" + joy_data).encode('utf-8'))
    limit_data = client.recv(1024)
    limit_pub.publish(str(ord(limit_data[0]))+str(ord(limit_data[1]))+str(ord(limit_data[2]))+str(ord(limit_data[3])))

    client.close()



def goReadyPos():
    print("Going Ready Position....")
    cmd = "%03d*%03d*%03d*%03d*%01d*%01d*%01d*%01d*%01d*%01d*%021d" % (25,0,0,0,0,0,0,1,1,0,0)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    client.send(("GET /cmd?=C01" + cmd).encode('utf-8'))
    client.close()
    
    time.sleep(0.3)
    cmd = "%03d*%03d*%03d*%03d*%01d*%01d*%01d*%01d*%01d*%01d*%021d" % (0,0,0,0,0,0,0,1,1,0,0)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    client.send(("GET /cmd?=C01" + cmd).encode('utf-8'))
    client.close()
    print("finish!!")

if __name__ == '__main__':
    rospy.init_node('http_lai')
    joy_topic = "/joy_information"
    position_topic = "/position"
    #goReadyPos()
    limit_pub = rospy.Publisher("limit_switch_state",String,queue_size=10)
    rospy.Subscriber(joy_topic, String, joy_callback_lai,queue_size = 1, buff_size = 52428800)

    rospy.spin()

