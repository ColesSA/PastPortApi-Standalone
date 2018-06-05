"""Initialize app as api with resources"""
from flask import Flask
from flask_restful import Api

from app.resources import LocationsLast, LocationsList, Now, Debug

APP = Flask(__name__)
API = Api(APP)

API.add_resource(LocationsLast, '/api/locations/last')
API.add_resource(LocationsList, '/api/locations')
API.add_resource(Now, '/api/now')
API.add_resource(Debug, '/api/debug')
    