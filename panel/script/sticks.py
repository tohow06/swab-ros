#!/usr/bin/env python3

# This file will start reading sticks information with i2c by ads1115
# and publish to '/sticks' in self-defined msg type "Sticks"
# ADS1115 (at line 25) need about 5 to 10 seconds to start
#

import rospy
from std_msgs.msg import String
from panel.msg import Sticks
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


def talker():
	pub = rospy.Publisher('sticks', Sticks, queue_size=10)
	rospy.init_node('ads1115', anonymous=True)
	rate = rospy.Rate(10) # 10hz
	# Create the I2C bus
	i2c = busio.I2C(board.SCL, board.SDA)

	# Create the ADC object using the I2C bus
	ads = ADS.ADS1115(i2c)
	# you can specify an I2C adress instead of the default 0x48
	# ads = ADS.ADS1115(i2c, address=0x49)

	# Create single-ended input on channel 0
	chan = AnalogIn(ads, ADS.P0)
	chan1 = AnalogIn(ads, ADS.P1)
	chan2 = AnalogIn(ads, ADS.P2)
	
	print("############ Sticks   start ############")	
	while not rospy.is_shutdown():
	
		msg=Sticks()
		msg.x=chan.value
		msg.y=chan1.value
		msg.z=chan2.value

		#rospy.loginfo(msg)
		pub.publish(msg)
		rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
