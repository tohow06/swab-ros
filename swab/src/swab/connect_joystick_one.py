#! /usr/bin/env python
import os

while(1):
    p = os.popen('ls /dev/input').read().split()
    if 'js0' in p:
        p = os.popen(
            'cd ~/catkin_ws_swab && roslaunch teapicking integral_lai.launch')
        qq = os.popen('cd ~/catkin_ws_swab && rosrun teapicking joy_one.py')
        q = os.popen('cd ~/catkin_ws_swab && rosrun teapicking http_lai.py')
