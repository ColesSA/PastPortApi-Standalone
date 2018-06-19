"""Initialize API"""
from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from app.resources import LocationsLast, LocationsList, LocationNow
from app.config import Config

APP = Flask(__name__)
APP.config.from_object(Config)
CORS(APP, resources={r"/api/*": {"origins": "*", 'methods': 'GET', 'supports_credentials': True}})
API = Api(APP)

API.add_resource(LocationsLast, '/api/v2/location/last')
API.add_resource(LocationsList, '/api/v2/location/all')
API.add_resource(LocationNow, '/api/v2/location/now')
    