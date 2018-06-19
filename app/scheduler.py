"""Threaded Process that stores the Barge Location in the database in a specified time interval"""


import threading
from time import sleep

import app.resources
from app.config import Config
from app.connection import Debugger, get_coords
from app.database import Session

m, s = divmod(Config.SCHEDULER_DELAY_TIME, 60)
h, m = divmod(m, 60)
naptime = "%dh, %dm, %ds" % (h, m, s)

class Scheduler(object):
    isStarted = False

    def schedule():
        while True:
            Debugger.info('Sleeping for {}.'.format(naptime))
            sleep(Config.SCHEDULER_DELAY_TIME)
            get_coords()

    SchedThread = threading.Thread(name='Scheduler', 
                             target=schedule, 
                             daemon=True
                             )    

    def safe_start(self):
        if(self.isStarted):
            Debugger.debug('Scheduler already instantiated. Aborting start attempt.')
            return
        else:
            Debugger.info('Starting Scheduler Thread')
            self.isStarted = True
            self.SchedThread.start()
