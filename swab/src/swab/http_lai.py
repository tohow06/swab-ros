#! /usr/bin/env python
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
mode = 0
diff = 1
check_cmd = 0
check_finished = 0
initial_x = 0
initial_y = 0
initial_th = 0
goal_x = 0
goal_y = 0
goal_th = 0
turn_finished = 0
concerto_data = "00.00*00.00*0*00.00*00.00*00.00*0000.00*0000.00*00.00*00.00*00.00*00.00"
first_ = 0
pre_state = "go"

    
def mode_callback(msg):
    global mode, data_json, turn_finished, first_, check_cmd, check_finished
    temp_mode = msg.data
    if temp_mode != 3 and temp_mode != 2:        #mode:3 and 2is already written
        data_json['mode'] = temp_mode
        data_json['state'] = ''
        with open('data.json', 'w') as f:
            json.dump(data_json, f)
        print("data_json", data_json)
    elif temp_mode == 3:
        turn_finished = 1
        check_cmd = 0
        first_ = 0
        check_finished = 0
    print("mode", temp_mode)
    mode = msg.data



def diff_callback(msg):               ##ignore
    global diff, data_json, concerto_data
    diff = msg.data
    data_json['diff'] = diff
    with open('data.json', 'w') as f:
        json.dump(data_json, f)
    if mode == 4:
        cmd = "%02d*%03d*%05.2f*%05.2f*%04d*%04d*%d*%02d*%02d*%02d*%021d" % (diffTable.xDis[diff], 0, 0, 0, 0, 0, mode, diffTable.Radius[diff], 0, 0, 0) #57
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        client.send(("GET /cmd?=C01" + cmd).encode('utf-8'))
        client.close()
        concerto_data = os.popen("curl -s http://169.254.254.169/cmd?=C03").read().strip()


def turnLocation_callback(msg):
    global lidar_data, pointCMD_data, initial_x, initial_y, initial_th, turn_finished, concerto_data, check_cmd, check_finished, goal_x, goal_y, goal_th, first_
    x=round(msg.pose.position.x,2)
    y=round(msg.pose.position.y,2)
    theta=round(2*math.acos(msg.pose.orientation.w),2)
    sign=msg.pose.orientation.z
    if sign<0:
        theta=-theta
    if sign>=0:
        theta=theta
    if (mode == 3 and check_cmd == 1 and turn_finished == 0):
        #lidar_data['x'] = x   Show localization
        #lidar_data['y'] = y
        #lidar_data['th'] = theta
        #with open('lidar.json', 'w') as f:
        #    json.dump(lidar_data, f)
        if(check_finished == 1):
            #initial_x = x - tempPoint.x
            #initial_y = y - tempPoint.y
            #initial_th = th - tempPoint.th
            pre_goal_x = pointCMD_data["via_point"][concerto_res['finished']-1]["x"]
            pre_goal_y = pointCMD_data["via_point"][concerto_res['finished']-1]["y"]
            pre_goal_th = pointCMD_data["via_point"][concerto_res['finished']-1]["th"]
            next_goal_x = pointCMD_data["via_point"][concerto_res['finished']]["x"]
            next_goal_y = pointCMD_data["via_point"][concerto_res['finished']]["y"]
            next_goal_th = pointCMD_data["via_point"][concerto_res['finished']]["th"]
            trans = np.array([[np.cos(pre_goal_th), np.sin(pre_goal_th), 0],
                              [-np.sin(pre_goal_th), np.cos(pre_goal_th), 0],
                              [0, 0, 1]])
            next_goal_arr = np.array([[next_goal_x-pre_goal_x], [next_goal_y-pre_goal_y], [next_goal_th-pre_goal_th]])
            print(next_goal_arr)
            goal_arr = np.dot(trans, next_goal_arr)
            goal_x = goal_arr[0]
            goal_y = goal_arr[1]
            goal_th = goal_arr[2]
            check_finished = 0
            print("check_finished")
            print(concerto_res['finished'])
            print(trans)
        if(first_ == 0):
            goal_x = pointCMD_data["via_point"][concerto_res['finished']]["x"]
            goal_y = pointCMD_data["via_point"][concerto_res['finished']]["y"]
            goal_th = pointCMD_data["via_point"][concerto_res['finished']]["th"]
            first_ = 1
            print("first")
            print(concerto_res['finished'])
        temp_radius = diffTable["Radius"][diff]
        if diff < 0:
            temp_radius = -diffTable["Radius"][-diff]
        print(goal_x, goal_y, goal_th)
        cmd = "%05.2f*%05.2f*%05.2f*%05.2f*%05.2f*%05.2f*%d*%05.2f*%05.2f*%05.2f*%05.2f" % (x, y, theta, goal_x, goal_y, goal_th, mode, initial_x, initial_y, initial_th, temp_radius)  #61
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        client.send(("GET /cmd?=C01" + cmd).encode('utf-8'))
        time.sleep(0.05)
        client.close()
        concerto_data = os.popen("curl -s http://169.254.254.169/cmd?=C03").read().strip()
        if(pointCMD_data["points"] == concerto_res['finished']):
            turn_finished = 1
            print("turn_finished")
    elif(mode == 3 and check_cmd == 0 and turn_finished == 1):
        with open("pointCMD.json") as f:
            t_pointCMD_data = json.load(f)
            pointCMD_data = t_pointCMD_data["posts"][0]
        check_cmd = 1
        turn_finished = 0
        check_finished = 0
        
    

def joy_callback(msg):
    global concerto_data
    joy_data = msg.data
    joy = joy_data.split()
    left_UD = joy[0]
    right_UD = joy[1]
    if mode == 0:  
        cmd = "%02d*%03d*%05.2f*%05.2f*%04d*%04d*%d*%02d*%02d*%02d*%021d" % (0, 0, 0, 0, int(left_UD), int(right_UD), mode, 0, 0, 0, 0)        
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        client.send(("GET /cmd?=C01" + cmd).encode('utf-8'))
        client.close()
        concerto_data = os.popen("curl -s http://169.254.254.169/cmd?=C03").read().strip()

def joy_callback_lai(msg):
    global concerto_data
    joy_data = msg.data
    print(joy_data)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    client.send(("GET /cmd?=C01" + joy_data).encode('utf-8'))
    client.close()



##realsense
def position_callback(msg):
    global concerto_data, pre_state      
    position_data = msg.data
    position = position_data.split()
    x = int(position[0])
    y = int(position[1])
    th = float(position[2])
    v = float(position[3])               #new v
    state = position[4]
    if mode == 1:
        cmd = "%02d*%03d*%05.2f*%05.2f*%04d*%04d*%d*%02d*%02d*%02d*%021d" % (x, y, th, v, 0, 0, mode, 0, 0, 0, 0)
        if(pre_state != state):
            data_json['state'] = state
            with open('data.json', 'w') as f:
                json.dump(data_json, f)
            pre_state = state
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        client.send(("GET /cmd?=C01" + cmd).encode('utf-8'))
        client.close()
        #concerto_data = os.popen("curl -s http://169.254.254.169/cmd?=C03").read().strip()

        
def fcheck_finished():              #update concerto data, and write encoder to res_data
    pre_finished = 0
    pre_concerto_data = ""
    try:
        while not rospy.is_shutdown():
            global concerto_res, check_finished
            if(pre_concerto_data != concerto_data):
                pre_concerto_data = concerto_data
                ret = concerto_data.split('*')
                if(len(ret) < 2):
                    ret = "00.00*00.00*0*00.00*00.00*00.00*0000.00*0000.00*00.00*00.00*00.00*00.00".split('*')
                #print(concerto_data)
                concerto_res['wheel_L'] = float(ret[8])
                concerto_res['wheel_R'] = float(ret[9])
                if mode == 3 or mode == 4:
                    if (pre_finished != int(ret[2])):
                        check_finished = 1
                        pre_finished = int(ret[2])
                    with open('concerto.txt', 'a') as f:
                        f.write(concerto_data+"......"+str(datetime.datetime.now())+"\n")
                concerto_res['finished'] = int(ret[2])
                print("concerto: ", concerto_res['finished'])
                with open('concerto.json', 'w') as f:
                        json.dump(concerto_res, f)  
                time.sleep(0.2)  
    finally:
        print("ok")

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
    diff_topic = "/differential_turn"
    joy_topic = "/joy_information"
    position_topic = "/position"
    turnLocation_topic = "/slam_out_pose"
    mode_topic = "/mode"
    #goReadyPos()
    rospy.Subscriber(joy_topic, String, joy_callback_lai,queue_size = 1, buff_size = 52428800)

    rospy.spin()
    # Spin until ctrl + cl
