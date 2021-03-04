import time

# Import the ADS1x15 module.
import Adafruit_ADS1x15


# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()

GAIN = 1

# Main loop.
while True:
    # Read all the ADC channel values in a list.
    values = [0]*4
    print(adc.read_adc(0, gain=GAIN))
    time.sleep(0.5)
