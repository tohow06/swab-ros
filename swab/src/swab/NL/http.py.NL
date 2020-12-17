#! /usr/bin/env python
import socket
import time
import rospy
import roslaunch
from std_msgs.msg import Int16, String
import json
from nav_msgs.msg import Path
import math


##This version without Lidar


ip = '169.254.254.169'
port = 80
mode = 0
data_json = {'mode':'', 'state':'', 'diff':'', 'encoder':''}
diff = 1


def mode_callback(msg):
    global mode
    cc = msg.data
    if cc != 3 and cc != 2:        #mode:3 and 2is already written
        data_json['mode'] = cc
        data_json['state'] = ''
        data_json['diff'] = ''
        data_json['encoder'] = ''
        with open('data.json', 'w') as f:
            json.dump(data_json, f)
        print str(cc)+" OK"
    mode = msg.data


def diff_callback(msg):
    diff = msg.data
    cmd = "%02d*%03d*%05.2f*%04d*%04d*%d*%05.2f" % (12, 0, 0, 0, 0, mode, diff)
    if mode == 3:
        print "3"
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        client.send(("GET /cmd?=C01" + cmd).encode('utf-8'))
        data = client.recv(1024)
        client.close()


def joy_callback(msg):
    joy_data = msg.data
    joy = joy_data.split()
    left_UD = joy[0]
    right_UD = joy[1]
    cmd = "%02d*%03d*%05.2f*%04d*%04d*%d*%05.2f" % (0, 0, 0, int(left_UD), int(right_UD), mode, 0)
    if mode == 0:          
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        client.send(("GET /cmd?=C01" + cmd).encode('utf-8'))
        client.close()



##realsense
def position_callback(msg):             
    position_data = msg.data
    position = position_data.split()
    x = int(position[0])
    y = int(position[1])
    th = float(position[2])
    state = position[3]
    cmd = "%02d*%03d*%05.2f*%04d*%04d*%d*%05.2f" % (x, y, th, 0, 0, mode, 0)
    if mode == 1:
        data_json['mode'] = mode
        data_json['state'] = state
        with open('data.json', 'w') as f:
            json.dump(data_json, f)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        client.send(("GET /cmd?=C01" + cmd).encode('utf-8'))
        client.close()

        

    

if __name__ == '__main__':
    rospy.init_node('http')
    diff_topic = "/differential_turn"
    joy_topic = "/joy_information"
    position_topic = "/position"
    mode_topic = "/mode"
    rospy.Subscriber(diff_topic, Int16, diff_callback, queue_size = 1, buff_size = 52428800)
    rospy.Subscriber(mode_topic, Int16, mode_callback, queue_size = 1, buff_size = 52428800)
    rospy.Subscriber(position_topic, String, position_callback, queue_size = 1, buff_size = 52428800)
    rospy.Subscriber(joy_topic, String, joy_callback,queue_size = 1, buff_size = 52428800)
    rospy.spin()
    # Spin until ctrl + cl
