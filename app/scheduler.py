import threading
import logging
from time import sleep, time
from app.config import Config
from app.resources import store_location
from app.connection import get_secure_coords, TIME_DIFF
import requests

def schedule():
    logging.info(' * Starting Scheduler Thread')
    while True:
        store_location(get_secure_coords())
        sleep(Config.SCHEDULER_DELAY_TIME-TIME_DIFF)

SCHEDULER = threading.Thread(name='Scheduler', 
                             target=schedule, 
                             daemon=True
                             )