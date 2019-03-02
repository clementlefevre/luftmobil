# sshfs -o nonempty pi@192.168.178.93:/home/pi /home/ramon/workspace/raspi_zero_clem/
# fusermount -u /home/ramon/workspace/raspi_zero_clem/
# activate  venv : source .env/bin/activate

import time
import json
import logging

from config import *

from service.adafruit_BME280 import get_bme280_data
from service.sds011 import  SDS011
from service.gpsd_pi import init_gps, get_gps_data
from service.aws import is_connected,upload_data
from service.converter import round_values, get_median

logging.basicConfig(filename='luftmobil.log',level=logging.INFO,format='%(asctime)s:%(levelname)s:%(message)s')


DATA_FILE = "data.json"

sensor = SDS011("/dev/ttyUSB1", use_query_mode=True)
sensor.sleep()  # Turn off fan and diode

init_gps()

def store_data(measures):

   
    
    try:
        with open(DATA_FILE) as f:
            data = json.load(f)
    except:
        data = []

    with open(DATA_FILE, mode='w') as f:
        data.append(measures)
        json.dump(data,f)
        logging.info("Finished dump data.")


def process_data():
    measures = {}
    measures = get_bme280_data()


    sensor.sleep(sleep=False)  # Turn on fan and diode

    time.sleep(15)  # Allow time for the sensor to measure properly

    sds_measures_pm25  = []
    sds_measures_pm10 = []

    for i in range(0,15):
        sensor_data = sensor.query()
        #logging.info("sensor_data : {}".format(sensor_data))
        sds_measures_pm25.append(sensor_data[0])
        sds_measures_pm10.append(sensor_data[1])
     
    measures['pm25']= get_median(sds_measures_pm25)
    measures['pm10']= get_median(sds_measures_pm10)
    measures['datetime']= time.strftime("%d.%m.%Y %H:%M:%S %Z")
    measures['capture_ts']= time.time()
    gps_data = get_gps_data()
    
    measures = round_values(measures)
    logging.info("GPS DATA : {0} : {1}".format(gps_data['time'],gps_data['lat']))
    measures_with_gps = {**measures, **gps_data}
    try:
        store_data(measures_with_gps)
    except Exception as e:
        print(e)

    finally:
        sensor.sleep()

    if is_connected():
        try:
            upload_data()
        except Exception as e:
            raise e

    print('sleep for {} minutes'.format(SLEEP_MINUTES))
    logging.info('sleep for {} minutes'.format(SLEEP_MINUTES))
    

if __name__ =="__main__":
    while True :
        try:
            process_data()

        except Exception as e:
            logging.exception(e)

        finally:
            logging.info("Job done.")
            time.sleep(60*SLEEP_MINUTES)
