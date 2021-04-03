# Import the ADS1x15 module.
import Adafruit_ADS1x15
import time
import board
import busio
import adafruit_character_lcd.character_lcd_i2c as character_lcd
import requests

# Modify this if you have a different sized Character LCD
lcd_columns = 20
lcd_rows = 4

# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()

GAIN = 1
# Initialise I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Initialise the lcd class
lcd = character_lcd.Character_LCD_I2C(i2c, lcd_columns, lcd_rows)

# Turn backlight on
lcd.backlight = True
lcd.clear()
# Print a two line message
lcd.message = "Initializing......"
time.sleep(5)
lcd.clear()

m=2251.84
b=13093.87
m1 = 108.72
b1 = 12955.26

voltage=236.0
samples = 50
min_current = 0.2
# min_current = 0.025
min_power = 1.0
total_energy = 0.0
totla_power = 0.0


def update_lcd_msg(l1="",l2="",l3="",l4=""):
    l1=f"Power: {l1} W"
    l1t = l1+" "*(19-len(l1)) + "\n"
    l2=f"Set Voltage: {l2}v"
    l2t = l2+" "*(19-len(l2)) + "\n"
    l3=f"Current(RMS): {l3}A"
    l3t = l3+" "*(19-len(l3)) + "\n"
    l4 = f"Energy: {l4} kw"
    l4t = l4+" "*(19-len(l4))
    # lcd.clear()
    # Print a two line message
    lcd.message = l1t+l2t+l3t+l4t

def measure_power():
    voltage=236.0
    samples = 50
    min_power = 1.0
    cntr = 0
    readings=[]
    while(cntr < samples):
        sensor_reading = abs(adc.read_adc(1, gain=GAIN))
        cntr += 1
        readings.append(sensor_reading)
        time.sleep(0.02)
    max_reading = max(readings)

    current_rms=(max_reading-b1)/m1
    current_rms=round(current_rms, 3)
    if(current_rms < min_current):
        current_rms = 0.0
    power=voltage*current_rms
    power=round(power, 2)
    if power < min_power:
        power = 0
    return {'power': power, 'current_rms':current_rms}


while 1:
    pwr = measure_power()
    power = pwr['power']
    current_rms = pwr['current_rms']
    totla_power += power
    total_energy = round(totla_power/1000.0, 2)
    print(f'power: {power} W,\tCurrent(RMS): {current_rms} A')
    update_lcd_msg(str(power), str(voltage), str(current_rms), str(total_energy))
    d={"current": current_rms, 'set_voltage': voltage, 'tot_energy': total_energy, 'pwr': power}
    url = f'http://3.137.144.214:5573/log_data/{d}'
    try:
        r = requests.get(url)
        print(d)
    except:
        print('Network Err')
