"""API Runable"""

from app import app, sched

sched.safe_start()
app.run()
