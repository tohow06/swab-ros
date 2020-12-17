#! /usr/bin/env python
import rospy
from std_msgs.msg import String, Int16
from sensor_msgs.msg import Joy
import os
import json
count2 = 0     #mode 
count = 0      #mode 0~1
mode = 0
diff = 1       #1~9

other_mode = 0


def mode_callback(msg):
    global other_mode
    other_mode = msg.data


def CarControl_callback(msg):
    global count, mode, diff, count2
    buttons = msg.buttons
    axes = msg.axes       
    a = buttons[1]
    x = buttons[0]         #mode 4
    y = buttons[3]         #stop testing
    back = buttons[8]
    LB = buttons[4]        #increse turning radius
    LT = buttons[6]        #decrese turning radius
    rate = rospy.Rate(4)
    if back == 1:        ## press back to shutdown
      p = os.popen('shutdown now')
    if (a == 1 and other_mode < 2):           ## change mode:0-1
        count += 1
        mode = count % 2
        pub_mode.publish(mode)
    if (x == 1 and (other_mode == 4 or other_mode == 0)):           ## change mode:0-4
        count2 += 1
        temp = count2 % 2
        if temp:
            pub_mode.publish(4)
        else:
            pub_mode.publish(0)

    if LB == 1 or LT == 1:                    ## change turning radius
      if LB == 1:
        if diff < 9:
          diff += 1
      elif LT == 1:
        if diff > 1:
          diff -= 1
    Duty1=int(axes[1]*100)
    Duty2=int(axes[3]*100)
    string = "%04d %04d" %(Duty1, Duty2)
    pub_joy.publish(string)
    pub_diff.publish(diff)
    print string
    rate.sleep()
 
 
if __name__ == '__main__':
    rospy.init_node('joy')
    joy_topic = "/joy"
    gpio_topic = "/gpio"
    mode_topic = "/mode"
    pub_joy = rospy.Publisher('joy_information', String, queue_size=1)
    pub_diff = rospy.Publisher('differential', Int16, queue_size=1)
    pub_mode = rospy.Publisher('mode', Int16, queue_size=1)
    rospy.Subscriber(mode_topic, Int16, mode_callback, queue_size = 1, buff_size = 52428800)
    rospy.Subscriber(joy_topic, Joy, CarControl_callback, queue_size = 1, buff_size = 52428800)
    rospy.spin()
