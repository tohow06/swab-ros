#!/usr/bin/python3

# this file will start reading VL53L0X using i2c and publish to '/tof_data'


import time
import VL53L0X
import rospy
from std_msgs.msg import UInt16

# Create a VL53L0X object
tof = VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x29)
# I2C Address can change before tof.open()
# tof.change_address(0x32)
tof.open()
# Start ranging
tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)

timing = tof.get_timing()
if timing < 20000:
    timing = 20000
print("Timing %d ms" % (timing/1000))


def talker():
    pub = rospy.Publisher('tof_data', UInt16, queue_size=10)
    rospy.init_node('tof')
    while not rospy.is_shutdown():
        distance = tof.get_distance()
        if distance > 0:
            print("%d mm" % (distance))
            pub.publish(distance)
        rospy.sleep(timing/1000000.00)
if __name__ == '__main__':
    try:
        talker()
        tof.stop_ranging()
        tof.close()
    except rospy.ROSInterruptException:
        rospy.signal_shutdown("tof shut down")
        pass
