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
data_json = {'mode':'', 'state':'', 'diff': ''}
tracking_left_launch = ""
tracking_right_launch = ""
diff = 1

def diff_callback(msg):
    global diff
    diff = msg.data
    data_json['diff'] = diff
    with open('data.json', 'w') as f:
        json.dump(data_json, f)
    if l_tmp == 2:
        pub_difft.publish(diff)
    elif r_tmp == 2:
        pub_difft.publish(-diff)



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
            mode = 1
            pub_mode.publish(mode)
            l_tmp = 0
            r_tmp = 0
        elif l_tmp == 1:
            mode = 2
            data_json['mode'] = mode
            data_json['state'] = 'wait_left'
            with open('data.json', 'w') as f:
                json.dump(data_json, f)
            pub_mode.publish(mode)
            cmd = "%02d*%03d*%05.2f*%04d*%04d*%d*%05.2f" % (0, 0, 0, 0, 0, mode, 0)
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((ip, port))
            client.send(("GET /cmd?=C01" + cmd).encode('utf-8'))
            client.close()
        elif r_tmp == 1:
            mode = 2
            data_json['mode'] = mode
            data_json['state'] = 'wait_right'
            with open('data.json', 'w') as f:
                json.dump(data_json, f)
            pub_mode.publish(mode)
            cmd = "%02d*%03d*%05.2f*%04d*%04d*%d*%05.2f" % (0, 0, 0, 0, 0, mode, 0)
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((ip, port))
            client.send(("GET /cmd?=C01" + cmd).encode('utf-8'))
            client.close()
        elif l_tmp == 2:     ##  start to turn  mode:3
            mode = 3
            pub_mode.publish(mode)
            pub_difft.publish(diff)
            data_json['mode'] = mode
            data_json['state'] = 'turn_left'
            data_json['diff'] = diff
            with open('data.json', 'w') as f:
                json.dump(data_json, f)
            a = os.popen('roslaunch rplidar_ros rplidar.launch')
            b = os.popen('roslaunch laser_filters alan_filter_right.launch')  # add left
            c = os.popen('roslaunch rplidar_ros hectormapping_tea.launch')
            d = os.popen('roslaunch explore_lite explore_alan_right.launch')
            r_tmp = 0        ## avoid press right
            print("start")
        elif r_tmp == 2:
            mode = 3
            pub_mode.publish(mode)
            pub_difft.publish(-diff)
            data_json['mode'] = mode
            data_json['state'] = 'turn_right'
            data_json['diff'] = diff
            with open('data.json', 'w') as f:
                json.dump(data_json, f)
            a = os.popen('roslaunch rplidar_ros rplidar.launch')
            b = os.popen('roslaunch laser_filters alan_filter_right.launch')   #add right
            c = os.popen('roslaunch rplidar_ros hectormapping_tea.launch')
            d = os.popen('roslaunch explore_lite explore_alan_right.launch')
            l_tmp = 0         ## avoid press left
            print("start")
        elif r_tmp == 4:    ##   finish truning
            l_tmp = 0
            r_tmp = 0
        elif r_tmp == 4:    ##   finish truning
            l_tmp = 0
            r_tmp = 0


if __name__ == '__main__':
    rospy.init_node('launch')
    gpio_topic = "/gpio"
    diff_topic = "/differential"
    rospy.Subscriber(diff_topic, Int16, diff_callback, queue_size = 1, buff_size = 52428800)
    pub_mode = rospy.Publisher('mode', Int16, queue_size=1)
    pub_difft = rospy.Publisher('differential_turn', Int16, queue_size=1)
    rospy.Subscriber(gpio_topic, String, gpio_callback, queue_size = 1, buff_size = 52428800) 
    rospy.spin()
