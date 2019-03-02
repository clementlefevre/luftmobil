import gps
import logging

logger = logging.getLogger(__name__)


def init_gps():
    data = get_gps()
    if data is not None :
        #logging.info("data : {}".format(data))
       
        if  'gps_lat' in data:
            logger.info("*gps_lat FOUND*"*5)
            #logger.info("Lat/Lon found : {0}/{1}".format(data['gps_lat'],data['gps_lon']))
            return True
        return False
    else:
        logger.info("waiting for lat/lon")
        return False


def get_gps():
    session = gps.gps("localhost", "2947")
    session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

    report = None

    has_lat_lon = False

    while not has_lat_lon:

        try:
            report = session.next()
            #logging.info("report : {}".format(report))
            # Wait for a 'TPV' report and display the current time
            
            if report['class'] == 'TPV':
                if hasattr(report, 'time'):
                    gps_dict = {"gps_"+str(k) : str(report[k]) for k in report.keys()}
                    logging.info("report[time] : {}".format(report['time']))
                    has_lat_lon = True
                    return gps_dict
        except KeyError:
            return {}
        except KeyboardInterrupt:
            quit()
        except StopIteration:
            session = None
            logging.error("GPSD has terminated")

