"""Initialize API"""

import logging
from logging.handlers import SMTPHandler

from flask import Flask
from flask.logging import default_handler
from flask_restful import Api

from api.config import Config
from api.connection import SafeSession
from api.resources import LocationNow, LocationsLast, LocationsList
from api.scheduler import Scheduler
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*", 'methods': 'GET', 'supports_credentials': True}})
api = Api(app)

app.config.from_object(Config)

api.add_resource(LocationsLast, '/api/v2/location/last')
api.add_resource(LocationsList, '/api/v2/location/all')
api.add_resource(LocationNow, '/api/v2/location/now')

sched = Scheduler(Config.WEB['URL'], Config.SCHEDULER_DELAY_TIME)

conn = SafeSession(Config.WEB['UID'], 
                   Config.WEB['PWD'], 
                   Config.WEB['VERIFICATION'],
                   Config.CONNECTION['MAX_RETRIES'], 
                   Config.CONNECTION['BACKOFF_FACTOR'], 
                   Config.CONNECTION['STATUS_FORCELIST'])

if(Config.LOGGING):
    smtp_handler = SMTPHandler(
        mailhost=Config.ERR['MAIL_HOST'],
        fromaddr=Config.ERR['FROM_ADDR'],
        toaddrs=Config.ERR['TO_ADDRS'],
        subject=Config.ERR['SUBJECT_DEFAULT'])
    smtp_handler.setLevel(logging.ERROR)

    for logger in (
        logging.getLogger(),
        logging.getLogger('sqlalchemy'),
        logging.getLogger('flask_cors'),
        logging.getLogger('click'),
    ):
        logger.level = logging.DEBUG if Config.DEBUG else logging.ERROR
        logger.addHandler(default_handler)
        logger.addHandler(smtp_handler)