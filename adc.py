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
    az = adc.read_adc(0, gain=GAIN)
    ao = adc.read_adc(1, gain=GAIN)
    print(f'A0: {az}\tA1: {ao}')
    time.sleep(0.5)
