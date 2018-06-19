"""Runable for API"""

from app import APP
from app.scheduler import Scheduler

sched = Scheduler()
sched.safe_start()

APP.run()

