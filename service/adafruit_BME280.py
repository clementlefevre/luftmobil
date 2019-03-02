import board
import digitalio
import busio
import time
import adafruit_bme280
from micropython import const

# Create library object using our Bus I2C port
i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c,address=const(0x76))

bme280.sea_level_pressure = 1013.25

data = {}

def get_bme280_data():
    data['temperature']= bme280.temperature
    data['humidity'] = bme280.humidity
    data['pressure'] = bme280.pressure
    data['altitude'] = bme280.altitude
    
    return data
