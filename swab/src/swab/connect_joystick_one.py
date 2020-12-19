#! /usr/bin/env python
import os

while(1):
    p = os.popen('ls /dev/input').read().split()
    if 'js0' in p:
        p = os.popen(
            'cd ~/catkin_ws_swab && roslaunch swab integral_lai.launch')
        qq = os.popen('cd ~/catkin_ws_swab && rosrun swab joy_one.py')
        q = os.popen('cd ~/catkin_ws_swab && rosrun swab http_lai.py')
    else:
	print("Can't find /dev/input/js0 ..........")
