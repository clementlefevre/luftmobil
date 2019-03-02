 #!/usr/bin/env python3
 
import gpsd

import logging

logger = logging.getLogger(__name__)


gpsd.connect("localhost", 2947) 


# Get gps position

def get_gps_data():
    data = {}
    raw_data= {}
    packet = gpsd.get_current()
    raw_data = packet.__dict__
    data = dict((k,str(v)) for k,v in raw_data.items())
    data.pop('error', None)
    return data

def has_gps_fix():
    if 'lat' in get_gps_data():
        logger.info("GPS Signal OK")
        return True
    else:
        return False


def init_gps():
    is_on = False

    while not is_on:
        is_on = has_gps_fix()