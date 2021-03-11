import time
import pickle
import statistics
from os import listdir
from os.path import isfile, join


# Import the ADS1x15 module.
import Adafruit_ADS1x15



def write_file(fn, val):
    fn = f'vals/{fn}.pickle'
    with open(fn, 'wb') as handle:
        pickle.dump(val, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print(f'{fn} exported')

def read_file(fn):
    fn = f'vals/{fn}'
    with open(fn, 'rb') as handle:
        b = pickle.load(handle)
        return b




# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()

GAIN = 1
def read_samples():
    samples = 600
    cntr = 0
    readings = []
    current = 0.901
    # Main loop.
    while cntr < samples:
        # Read all the ADC channel values in a list.
        values = [0]*4
        val = adc.read_adc(1, gain=GAIN)
        rem = samples - cntr
        cntr += 1
        print(f'Remaining: {rem}\t{val}')
        readings.append(val)
        time.sleep(0.1)

    avg = statistics.mean(readings)
    fn = str(int(time.time()))
    val = {'current': current, 'avg': avg}
    write_file(fn, val)

def files_in_dir():
    path='/home/pi/src/vals/'
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    return onlyfiles

def extract_readings():
    fns = files_in_dir()
    current = []
    sensor_reading = []

    for i in fns:
        v = read_file(i)
        current.append(v['current'])
        sensor_reading.append(v['avg'])
    
    print(f'current: {current}')
    print(f'sensor_reading: {sensor_reading}')

def plt():
    # importing the required module 
    import matplotlib.pyplot as plt 
    import numpy as np


    # x axis values 
    x = [0.522, 0.782, 0.258]
    # corresponding y axis values 
    y = [14265, 14857, 13677]


    slope, intercept = np.polyfit(x, y, 1)
    print(f'slope: {slope}\nintercept: {intercept}')
    # plotting the points  
    plt.plot(x, y) 
    
    # naming the x axis 
    plt.xlabel('x - axis') 
    # naming the y axis 
    plt.ylabel('y - axis') 
    
    # giving a title to my graph 
    plt.title('current vs avg_sensor_reading') 
    
    # function to show the plot 
    plt.show() 

extract_readings()
