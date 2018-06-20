"""Initialize API"""

import logging
from logging.handlers import SMTPHandler

from flask import Flask
from flask_restful import Api

from app.config import Config
from app.connection import SafeSession
from app.resources import LocationNow, LocationsLast, LocationsList
from app.scheduler import Scheduler
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*", 'methods': 'GET', 'supports_credentials': True}})
api = Api(app)

app.config.from_object(Config)

api.add_resource(LocationsLast, '/api/v2/location/last')
api.add_resource(LocationsList, '/api/v2/location/all')
api.add_resource(LocationNow, '/api/v2/location/now')

sched = Scheduler(Config.WEB['URL'], Config.SCHEDULER_DELAY_TIME)

sess = SafeSession(Config.CONNECTION['MAX_RETRIES'], 
                   Config.CONNECTION['BACKOFF_FACTOR'], 
                   Config.CONNECTION['STATUS_FORCELIST'])

sess.set_security_info(Config.WEB['UID'], Config.WEB['PWD'], Config.WEB['VERIFICATION'])

smtp_handler = SMTPHandler(
    mailhost=Config.ERR['MAIL_HOST'],
    fromaddr=Config.ERR['FROM_ADDR'],
    toaddrs=Config.ERR['TO_ADDRS'],
    subject=Config.ERR['SUBJECT_DEFAULT'])
smtp_handler.setLevel(logging.ERROR)

if not app.debug:
    app.logger.addHandler(smtp_handler)