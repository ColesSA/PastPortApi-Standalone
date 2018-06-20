"""Threaded Process that stores the Barge Location in the database in a specified time interval"""

import os
import threading
from time import sleep

from app.connection import Debugger, get_coords
from app.database import Session
from app.models import Location

class Scheduler(object):
    hasRun = os.environ.get("WERKZEUG_RUN_MAIN")

    def __init__(self, url, interval=60):
        self.interval = interval - 1.5
        self.url = url

        self.thread = threading.Thread(target=self.schedule)
        self.thread.name='Scheduler'
        self.thread.daemon=True  

    def safe_start(self):
        if(self.hasRun):
            Debugger.debug('Scheduler already instantiated. Aborting start attempt.')
            return
        else:
            Debugger.info('Starting Scheduler Thread')
            self.thread.start()

    def schedule(self):
        while True:
            self.wait(self.interval)
            now = Location(get_coords(self.url))
            Session.add(now)
            Session.commit()

    def wait(self, interval):
        m, s = divmod(interval, 60)
        h, m = divmod(m, 60)
        naptime = "%dh, %dm, %ds" % (h, m, s)
        Debugger.debug('Sleeping for {}.'.format(naptime))
        sleep(interval)
