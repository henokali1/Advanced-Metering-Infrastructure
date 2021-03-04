#!/usr/bin/env python3
import time
from Adafruit_IO import *
import math
from random import randint
import os

username = os.environ["IO_USERNAME"]
AIO_KEY = os.environ["IO_KEY"]

aio = Client(username, AIO_KEY)
GAIN = 1         # see ads1015/1115 documentation for potential values.
samples = 5      # number of samples taken from ads1115
places = int(2)    # set rounding
# create a while loop to monitor the current and voltage and send to Adafruit io.
while True:
    #calculate power
    power = randint(1,100)
    print('Power: {0}'.format(power))
    #post data to adafruit.io
    energyconsumption = aio.feeds('energyconsumption')
    aio.send_data('energyconsumption', power)
    # Wait before repeating loop
    print('Sleep: 30')
    time.sleep(30)
