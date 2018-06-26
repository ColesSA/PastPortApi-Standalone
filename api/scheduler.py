"""Threaded Process that stores the Barge Location in the database in a specified time interval"""

import os
import threading
import logging
from time import sleep

import api
from api.config import Config
from api.models import Location, Coordinate
from api.database import to_database

class Scheduler(object):
    """Thread to handle regular bachground fetching of barge location from PastPort."""

    hasRun = os.environ.get("WERKZEUG_RUN_MAIN")

    def __init__(self, url, interval=60):
        self.interval = interval - 1.5
        self.url = url

        self.thread = threading.Thread(target=self.schedule)
        self.thread.name='Scheduler'
        self.thread.daemon=True  

    def safe_start(self):
        """Instantiates a Scheduler that will regularly store the barge location into the database"""
        if(self.hasRun):
            logging.debug('Scheduler already instantiated. Aborting start attempt.')
            return
        else:
            logging.info('Starting Scheduler Thread')
            self.thread.start()

    def schedule(self):
        """Loop that waits, then collects and stores location"""
        while True:
            self.wait(self.interval)
            _response = api.conn.get_from(Config.WEB['URL'])
            _coordinate = Coordinate.from_request(_response)
            _location = Location.get_new(_coordinate)
            to_database(_location)
            break
        self.schedule()

    def wait(self, interval):
        """Sleeps the thread for the interval of time given

        Arguments:
            interval {int} -- interval (in seconds) to sleep the thread"""
        m, s = divmod(interval, 60)
        h, m = divmod(m, 60)
        naptime = "%dh, %dm, %ds" % (h, m, s)
        logging.debug('Sleeping for {}.'.format(naptime))
        sleep(interval)
