# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Create single-ended input on channel 0

# Create differential input between channel 0 and 1
chan = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)
chan2 = AnalogIn(ads, ADS.P2)


print("{:>5}\t{:>5}".format("raw", "v"))

while True:
    print("x = {:>5}\t{:>5.3f}".format(chan.value, chan.voltage))
    print("y = {:>5}\t{:>5.3f}".format(chan1.value, chan1.voltage))
    print("z = {:>5}\t{:>5.3f}".format(chan2.value, chan2.voltage))
    print("\n")
    time.sleep(0.5)
