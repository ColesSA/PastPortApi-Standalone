"""Initialize app as api with resources"""
from flask import Flask
from flask_restful import Api

from app.resources import LocationsLast, LocationsList, Now
from app.config import Config

APP = Flask(__name__)
APP.config.from_object(Config)
API = Api(APP)

API.add_resource(LocationsLast, '/api/locations/last')
API.add_resource(LocationsList, '/api/locations')
API.add_resource(Now, '/api/now')
    