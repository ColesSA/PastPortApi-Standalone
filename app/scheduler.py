import threading
import logging
from time import sleep, time
from app.resources import store_location
from app.connection import get_coords

def schedule():
    logging.debug(' * Starting Scheduler Thread')
    while True:
        try:
            coords = get_coords()
            store_location((coords['latitude'],coords['longitude']))
            sleep(599)
        except ConnectionError as CE:
            logging.error(CE)

SCHEDULER = threading.Thread(name='Scheduler', 
                             target=schedule, 
                             daemon=True
                             )