import time


# Import the ADS1x15 module.
import Adafruit_ADS1x15


# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()

GAIN = 1

def measure_power():
    m=2251.84
    b=13093.87
    voltage=236.0
    cntr = 0
    readings=[]
    samples = 50
    while(cntr < samples):
        sensor_reading = abs(adc.read_adc(1, gain=GAIN))
        cntr += 1
        readings.append(sensor_reading)
        time.sleep(0.02)
    max_reading = max(readings)

    current_rms=(max_reading-b)/m
    current_rms=round(current_rms, 3)
    if(current_rms < 0.009):
        current_rms = 0.0
    power=voltage*current_rms
    power=round(power, 2)
    if power < 1:
        power = 0
    return {'power': power, 'current_rms':current_rms}


while 1:
    pwr = measure_power()
    power = pwr['power']
    current_rms = pwr['current_rms']
    print(f'power: {power} W,\tCurrent(RMS): {current_rms} A')
