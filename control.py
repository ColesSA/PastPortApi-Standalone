"""Stores the barge location once every 10 minutes"""

from resources import get_coords
from models import Location

import threading
from time import sleep
from db import SESSION

import logging

def store_location():
    logging.debug('Getting Coordinates')
    SESSION.add(Location(get_coords()))
    SESSION.commit()    

def schedule():
    logging.debug('Starting')
    while True:
        try:
            store_location()
            sleep(599)
        except ConnectionError as CE:
            logging.error(CE)

Scheduler = threading.Thread(name='Scheduler', target=schedule)
Scheduler.setDaemon(True)
