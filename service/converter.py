from decimal import Decimal
import statistics

from config import NUMERIC_FIELDS, SERIAL_PARTICLE_SENSOR

def round_values(m):
    m['device_id']= SERIAL_PARTICLE_SENSOR
    
    for n in NUMERIC_FIELDS:
        m[n] = (round(m[n],2))
        
    return m

def float_to_decimal(m):
    for n in NUMERIC_FIELDS:
        m[n] = Decimal(str(m[n]))
    
    return m


def get_median(sds_measures):
    if len(sds_measures)>0:
        sds_measures.remove(max(sds_measures))
        sds_measures.remove(min(sds_measures))
        median_sds = statistics.median(sds_measures)

        return median_sds

    else : 
        return -1

def fill_empty_values(data_list):
    no_empty_list = []
    for data in data_list:
        for k,v in data.items():
            if isinstance(v,str) and len(str(v))<1:
                data[k]=None
                
        no_empty_list.append(data)
    return no_empty_list