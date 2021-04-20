#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Revision $Id$

## Simple talker demo that published std_msgs/Strings messages
## to the 'chatter' topic

import rospy
from std_msgs.msg import String
from panel.msg import Sticks
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

c1_max = 17120
c1_min = 10112
c2_max = 17056
c2_min = 9809
c3_max = 18033
c3_min = 8576


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
		hello_str = "x %d value %d  y %d value %d  z %d value %d \n" %(chan.value, chan.voltage, chan1.value, chan1.voltage, chan2.value, chan2.voltage)
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
