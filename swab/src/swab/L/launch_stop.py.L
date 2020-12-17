#! /usr/bin/env python
import rospy
from std_msgs.msg import String, Int16
from sensor_msgs.msg import Joy
import os
import json
import socket

ip = '169.254.254.169'
port = 80
mode = 0
left = 0
right = 0
l_tmp = 0
r_tmp = 0
data_json = {'mode':'', 'state':''}
tracking_left_launch = ""
tracking_right_launch = ""

def gpio_callback(msg):
    global left, right, l_tmp, r_tmp, mode, tracking_left_launch, tracking_right_launch
    gpio_data = msg.data
    gpio = gpio_data.split()
    left = int(gpio[0])
    right = int(gpio[1])
    if left == 1:       ## press left  mode:2
        l_tmp += 1
    elif right == 1:    ## press right  mode:2
        r_tmp += 1
    if left != 0 or right != 0:
        if l_tmp == 1 and r_tmp == 1:   ## cancel truning
            l_tmp = 0
            r_tmp = 0
        if l_tmp == 3:    ##   finish truning
            mode = 1
            pub_mode.publish(mode)
            p = os.popen('rosnode kill /move_base /laser_filter /link1_broadcaster /rplidarNode /explore /hector_height_mapping')
            cmd = "%02d*%03d*%05.2f*%04d*%04d*%d*%05.2f" % (0, 0, 0, 0, 0, mode, 0)
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((ip, port))
            client.send(("GET /cmd?=C01" + cmd).encode('utf-8'))
            client.close()
            r_tmp = 0
        elif r_tmp == 3:    ##   finish truning
            mode = 1
            pub_mode.publish(mode)
            p = os.popen('rosnode kill /move_base /laser_filter /link1_broadcaster /rplidarNode /explore /hector_height_mapping')
            cmd = "%02d*%03d*%05.2f*%04d*%04d*%d*%05.2f" % (0, 0, 0, 0, 0, mode, 0)
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((ip, port))
            client.send(("GET /cmd?=C01" + cmd).encode('utf-8'))
            client.close()
            l_tmp = 0
        elif r_tmp == 4:    ##   finish truning
            l_tmp = 0
            r_tmp = 0
        elif r_tmp == 4:    ##   finish truning
            l_tmp = 0
            r_tmp = 0

if __name__ == '__main__':
    rospy.init_node('launch_stop')
    gpio_topic = "/gpio"
    pub_mode = rospy.Publisher('mode', Int16, queue_size=1)
    rospy.Subscriber(gpio_topic, String, gpio_callback, queue_size = 1, buff_size = 52428800) 
    rospy.spin()
