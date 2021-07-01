#!/usr/bin/env python

# This file will start reading button status with TX2's GPIO
# and publish to '/button_value'

import Jetson.GPIO as GPIO
import time
import rospy
from std_msgs.msg import UInt8
GPIO.setmode(GPIO.BOARD)
buttonGpio=16
#GPIO.setwarnings(False)
GPIO.setup(buttonGpio,GPIO.IN)
def talker():
	pub = rospy.Publisher('button_value', UInt8, queue_size=10)
	rospy.init_node('button', anonymous=True)
	rate = rospy.Rate(10) # 10hz
	while not rospy.is_shutdown():
		if GPIO.input(buttonGpio)==GPIO.HIGH:
			msg = 1
		else:
			msg = 0

		#rospy.loginfo(msg)
		pub.publish(msg)
		rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        GPIO.cleanup()
    except KeyboardInterrupt:
        GPIO.cleanup()
    pass
