"""Threaded Process that stores the Barge Location in the database in a specified time interval"""

import os
import threading
import logging
from time import sleep

import api
from api.database import Session
from api.models import Location

class Scheduler(object):
    """Thread to handle regular bachground fetching of barge location from PaastPort."""

    hasRun = os.environ.get("WERKZEUG_RUN_MAIN")

    def __init__(self, url, interval=60):
        self.interval = interval - 1.5
        self.url = url

        self.thread = threading.Thread(target=self.schedule)
        self.thread.name='Scheduler'
        self.thread.daemon=True  

    def safe_start(self):
        if(self.hasRun):
            logging.debug('Scheduler already instantiated. Aborting start attempt.')
            return
        else:
            logging.info('Starting Scheduler Thread')
            self.thread.start()

    def schedule(self):
        while True:
            self.wait(self.interval)
            api.sess.current_location_to_database(self.url)

    def wait(self, interval):
        m, s = divmod(interval, 60)
        h, m = divmod(m, 60)
        naptime = "%dh, %dm, %ds" % (h, m, s)
        logging.debug('Sleeping for {}.'.format(naptime))
        sleep(interval)
