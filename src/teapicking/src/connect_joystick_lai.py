#! /usr/bin/env python
import os

while(1):
 	p = os.popen('ls /dev/input').read().split()
	if 'js0' in p:
		p = os.popen('cd ~/catkin_ws && roslaunch teapicking integral_lai.launch')
		qq = os.popen('cd ~/catkin_ws && rosrun teapicking joy_lai.py')
		q = os.popen('cd ~/catkin_ws && rosrun teapicking http_lai.py')
		r = os.popen('cd ~/catkin_ws && rosrun teapicking launch.py')
		s = os.popen('cd ~/catkin_ws && rosrun teapicking launch_stop.py')


