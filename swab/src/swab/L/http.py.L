#! /usr/bin/env python
import socket
import time
import rospy
import roslaunch
from std_msgs.msg import Int16, String
import json
from nav_msgs.msg import Path
import math





ip = '169.254.254.169'
port = 80
mode = 0
data_json = {'mode':'', 'state':'', 'diff':''}
diff = 1


def mode_callback(msg):
    global mode
    cc = msg.data
    if cc != 3 and cc != 2:        #mode:3 and 2is already written
        data_json['mode'] = cc
        data_json['state'] = ''
        data_json['diff'] = ''
        with open('data.json', 'w') as f:
            json.dump(data_json, f)
        print str(cc)+" OK"
    mode = msg.data

def diff_callback(msg):
    global diff
    diff = msg.data



def joy_callback(msg):
    joy_data = msg.data
    joy = joy_data.split()
    left_UD = joy[0]
    right_UD = joy[1]
    cmd = "%02d*%03d*%05.2f*%05.2f*%04d*%04d*%d*%02d" % (0, 0, 0, 0, int(left_UD), int(right_UD), mode, 0)
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
    cmd = "%02d*%03d*%05.2f*%05.2f*%04d*%04d*%d*%02d" % (x, y, th, 0, 0, 0, mode, 0)
    if mode == 1:
        data_json['mode'] = mode
        data_json['state'] = state
        with open('data.json', 'w') as f:
            json.dump(data_json, f)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        client.send(("GET /cmd?=C01" + cmd).encode('utf-8'))
        client.close()

        
##Lidar
def frontier_callback(msg):             
    frontier = msg.poses
    qx = frontier[15].pose.orientation.x
    qy = frontier[15].pose.orientation.y
    qz = frontier[15].pose.orientation.z
    qw = frontier[15].pose.orientation.w
    sqw = qw * qw
    sqx = qx * qx
    sqy = qy * qy
    sqz = qz * qz
    r11 = 2*(qx*qy + qw*qz)
    r12 = sqw + sqx - sqy - sqz
    r21 = -2*(qx*qz - qw*qy)
    r31 = 2*(qy*qz + qw*qx)
    r32 = sqw - sqx - sqy + sqz
    rz = round(math.atan2(r11, r12), 2)
    if diff > 0:
        rz = abs(rz)
    elif diff < 0:
        rz = -abs(rz)     
    x = int(frontier[15].pose.position.x * 100)
    y = int(frontier[15].pose.position.y * 100)
    cmd = "%02d*%03d*%05.2f*%05.2f*%04d*%04d*%d*%02d" % (x, y, rz, v, 0, 0, mode, diff)
    if mode == 3:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        client.send(("GET /cmd?=C01" + cmd).encode('utf-8'))
        client.close()

 
##realsense PI control
#def velocity_callback(msg):             
#    velocity_data = msg.data
#    velocity = velocity_data.split()
#    x = velocity[0]
#    y = velocity[1]
#    th = velocity[2]
#    v = velocity[3]
#    ##delete V
#    cmd = "%02d*%03d*%05.2f*%04d*%04d*%d*%05.2f" % (int(x), int(y), float(th), 0, 0, mode, v)
#    if mode == 2:
#        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        client.connect((ip, port))
#        client.send(("GET /cmd?=C01" + cmd).encode('utf-8'))
#        client.close()
#        print 'velocity OK'
#        print cmd
    

if __name__ == '__main__':
    rospy.init_node('http')
    diff_topic = "/differential_turn"
    joy_topic = "/joy_information"
    position_topic = "/position"
    frontier_topic = "/move_base/TrajectoryPlannerROS/global_plan"
    mode_topic = "/mode"
#    velocity_topic = "/velocity"
    rospy.Subscriber(diff_topic, Int16, diff_callback, queue_size = 1, buff_size = 52428800)
    rospy.Subscriber(mode_topic, Int16, mode_callback, queue_size = 1, buff_size = 52428800)
    rospy.Subscriber(position_topic, String, position_callback, queue_size = 1, buff_size = 52428800)
    rospy.Subscriber(frontier_topic, Path, frontier_callback, queue_size = 1, buff_size = 52428800)
#    rospy.Subscriber(velocity_topic, String, velocity_callback, queue_size = 1, buff_size = 52428800)
    rospy.Subscriber(joy_topic, String, joy_callback,queue_size = 1, buff_size = 52428800)
    rospy.spin()
    # Spin until ctrl + cl
