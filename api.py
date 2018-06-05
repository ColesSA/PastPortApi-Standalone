"""Initialize app, api, resources, and run the app"""
from flask import Flask
from flask_restful import Api

from resources import LocationsLast, LocationsList, Now, Debug
from control import Scheduler 

APP = Flask(__name__)
API = Api(APP)

API.add_resource(LocationsLast, '/api/locations/last')
API.add_resource(LocationsList, '/api/locations')
API.add_resource(Now, '/api/now')
API.add_resource(Debug, '/api/debug')

if __name__ == '__main__':
    Scheduler.start()
    APP.run(debug=False)
    