#! /usr/bin/env python
import rospy
from std_msgs.msg import String, Int16
from sensor_msgs.msg import Joy
import os
import json
import socket
import time
import datetime
import subprocess

ip = '169.254.254.169'
port = 80
mode = 0
left = 0
right = 0
l_tmp = 0
r_tmp = 0
diff = 1

with open('/home/nvidia/catkin_ws/data_turn.json' , 'r') as reader:
    data_json = json.loads(reader.read())


def diff_callback(msg):        #from joy info to real info(+/-)
    global diff, data_json
    diff = msg.data
    data_json['diff'] = diff
    with open('data_turn.json', 'w') as f:
        json.dump(data_json, f)
    if l_tmp == 2:
        pub_difft.publish(diff)
    elif r_tmp == 2:
        pub_difft.publish(-diff)





def gpio_callback(msg):
    global left, right, l_tmp, r_tmp, mode, data_json
    gpio_data = msg.data
    gpio = gpio_data.split()
    left = int(gpio[0])
    right = int(gpio[1])
    if left == 1:       ## press left  mode:2
        l_tmp += 1
    elif right == 1:    ## press right  mode:2
        r_tmp += 1
    print(l_tmp, r_tmp)
    if left != 0 or right != 0:
        if l_tmp == 1 and r_tmp == 1:   ## cancel truning
            mode = 1
            pub_mode.publish(mode)
            l_tmp = 0
            r_tmp = 0
            data_json['check'] = 0
            with open('data_turn.json', 'w') as f:
                json.dump(data_json, f)
        if l_tmp == 3:
            mode = 1
            pub_mode.publish(mode)
            data_json['check'] = 0
            with open('data_turn.json', 'w') as f:
                json.dump(data_json, f)
            p = subprocess.Popen('rosnode kill /link1_broadcaster /hector_height_mapping', shell=True)
            cmd = "%02d*%03d*%05.2f*%05.2f*%04d*%04d*%d*%02d*%02d*%02d*%021d" % (0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0)
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((ip, port))
            client.send(("GET /cmd?=C01" + cmd).encode('utf-8'))
            client.close()
            r_tmp = 0
            l_tmp = 0
            print("finished")
        elif r_tmp == 3:
            mode = 1
            pub_mode.publish(mode)
            data_json['check'] = 0
            with open('data_turn.json', 'w') as f:
                json.dump(data_json, f)
            p = subprocess.Popen('rosnode kill /link1_broadcaster /hector_height_mapping', shell=True)
            cmd = "%02d*%03d*%05.2f*%05.2f*%04d*%04d*%d*%02d*%02d*%02d*%021d" % (0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0)
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((ip, port))
            client.send(("GET /cmd?=C01" + cmd).encode('utf-8'))
            client.close()
            l_tmp = 0
            r_tmp = 0
            print("finished")
        elif l_tmp == 2:     ##  start to turn  mode:3
            mode = 3
            pub_mode.publish(mode)
            pub_difft.publish(diff)
            data_json['mode'] = mode
            data_json['state'] = 'turn_left'
            data_json['diff'] = diff
            data_json['check'] = 1
            with open('data_turn.json', 'w') as f:
                json.dump(data_json, f)
            r_tmp = 0        ## avoid press right
            a = subprocess.Popen('roslaunch rplidar_ros hectormapping.launch', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            print("start")
        elif r_tmp == 2:     ##  start to turn  mode:3
            mode = 3
            pub_mode.publish(mode)
            pub_difft.publish(-diff)
            data_json['mode'] = mode
            data_json['state'] = 'turn_right'
            data_json['diff'] = diff
            data_json['check'] = 1
            with open('data_turn.json', 'w') as f:
                json.dump(data_json, f)
            l_tmp = 0         ## avoid press left
            a = subprocess.Popen('roslaunch rplidar_ros hectormapping.launch', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            print("start")
        elif (l_tmp == 1 and r_tmp == 0):                #wait_left
            mode = 2
            data_json['mode'] = mode
            data_json['state'] = 'wait_left'
            data_json['check'] = 1
            with open('data_turn.json', 'w') as f:
                json.dump(data_json, f)
            pub_mode.publish(mode)
            cmd = "%02d*%03d*%05.2f*%05.2f*%04d*%04d*%d*%02d*%02d*%02d*%021d" % (0, 0, 0, 0, 0, 0, mode, 0, 0, 0, 0)
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((ip, port))
            client.send(("GET /cmd?=C01" + cmd).encode('utf-8'))
            client.close()
            print("wait_left")
        elif (r_tmp == 1 and l_tmp == 0):                #wait_right
            mode = 2
            data_json['mode'] = mode
            data_json['state'] = 'wait_right'
            data_json['check'] = 1
            with open('data_turn.json', 'w') as f:
                json.dump(data_json, f)
            pub_mode.publish(mode)
            cmd = "%02d*%03d*%05.2f*%05.2f*%04d*%04d*%d*%02d*%02d*%02d*%021d" % (0, 0, 0, 0, 0, 0, mode, 0, 0, 0, 0)
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((ip, port))
            client.send(("GET /cmd?=C01" + cmd).encode('utf-8'))
            client.close()
            print("wait_right")

if __name__ == '__main__':
    rospy.init_node('launch')
    gpio_topic = "/gpio"
    diff_topic = "/differential"
    rospy.Subscriber(diff_topic, Int16, diff_callback, queue_size = 1, buff_size = 52428800)
    pub_mode = rospy.Publisher('mode', Int16, queue_size=1)
    pub_difft = rospy.Publisher('differential_turn', Int16, queue_size=1)
    rospy.Subscriber(gpio_topic, String, gpio_callback, queue_size = 1, buff_size = 52428800) 
    rospy.spin()
