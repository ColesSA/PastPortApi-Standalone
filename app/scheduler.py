"""Threaded Process that stores the Barge Location in the database in a specified time interval"""


import threading
from time import sleep
from app.config import Config
from app.resources import to_db
from app.connection import get_secure_coords, DEBUGGER

def schedule():
    DEBUGGER.info(' * Starting Scheduler Thread')
    while True:
        to_db(get_secure_coords())
        sleep(Config.SCHEDULER_DELAY_TIME)

SCHEDULER = threading.Thread(name='Scheduler', 
                             target=schedule, 
                             daemon=True
                             )