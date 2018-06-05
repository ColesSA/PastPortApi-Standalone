"""Flask_Restful Routing"""

import requests
from bs4 import BeautifulSoup
from flask_restful import Resource, fields, marshal_with, ResponseBase

from models import Location
from db import SESSION
from config import URL, UID, PWD

import json
from datetime import timedelta

location_fields = {
    'id': fields.Integer,
    'datetime': fields.DateTime(dt_format='rfc822'),
    'latitude': fields.Float(),
    'longitude': fields.Float(),
}

def get_coords():
    with requests.get(URL, verify=False, auth=(UID, PWD)) as req:
        return BeautifulSoup(req.content, 'html.parser').find(
            'div', {'id': 'latlong'})

class TimedeltaEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, timedelta):
            return obj.__str__()
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

class LocationsLast(Resource):
    @marshal_with(location_fields)
    def get(self):
        return SESSION.query(Location).order_by(-Location.id).first()

class LocationsList(Resource):
    @marshal_with(location_fields)
    def get(self):
        return SESSION.query(Location).all()

class Now(Resource):
    @marshal_with(location_fields)
    def get(self):
        loc = Location(get_coords())
        SESSION.add(loc)
        SESSION.commit()
        return loc

class Debug(Resource):
    def get(self):
        from api import APP
        return json.loads(json.dumps(APP.config, cls=TimedeltaEncoder))
