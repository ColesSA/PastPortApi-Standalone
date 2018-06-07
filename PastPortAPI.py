"""Runable for API"""


from app import APP
from app.scheduler import SCHEDULER

SCHEDULER.start()
APP.run()

