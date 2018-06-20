"""API Runable"""

from api import app, sched

sched.safe_start()
app.run()
