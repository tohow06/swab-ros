#! /usr/bin/env python
import rospy
import Jetson.GPIO as gpio
import time
from std_msgs.msg import Int16, String
import os

left_pin = 15
right_pin = 22
left_val_n = 0
right_val_n = 0

def main():
    left_preVal = ""
    right_preVal = ""
    rate = rospy.Rate(10)
    gpio.setmode(gpio.BOARD)
    gpio.setup(left_pin, gpio.IN) 
    gpio.setup(right_pin, gpio.IN) 
    try:
        while not rospy.is_shutdown():
            left_val = gpio.input(left_pin)
            right_val = gpio.input(right_pin)
            if left_val != left_preVal or right_val != right_preVal:
                if left_val == gpio.HIGH:
                    left_val_n = 1
                else:
                    left_val_n = 0
                if right_val == gpio.HIGH:
                    right_val_n = 1
                else:
                    right_val_n = 0
                left_preVal = left_val
                right_preVal = right_val
                pub_mode.publish(str(left_val_n) + " " + str(right_val_n))
            rate.sleep()
    finally:
        gpio.cleanup()
        print("ok")


if __name__ == '__main__':
    rospy.init_node('GPIO', anonymous=True)
    pub_mode = rospy.Publisher('gpio', String, queue_size=1)
    main()
