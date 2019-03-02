import time
from service.sds011 import  SDS011
#sensor = SDS011("/dev/serial/by-id/usb-Silicon_Labs_CP2104_USB_to_UART_Bridge_Controller_016D625A-if00-port0", use_query_mode=True)
while True:
    try :
        sensor = SDS011("/dev/ttyUSB1")
        #sensor.sleep()  # Turn off fan and diode
        sensor.sleep(sleep=False)  # Turn on fan and diode
        time.sleep(15)  # Allow time for the sensor to measure properly
        for i in range(0,15):
            sensor_data = sensor.query()
            print("sensor_data : {}".format(sensor_data))
    except Exception as e:
        print(e)
