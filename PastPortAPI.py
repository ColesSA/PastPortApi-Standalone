from app import APP
from app.resources import SCHEDULER

SCHEDULER.start()
APP.run(debug=True)

