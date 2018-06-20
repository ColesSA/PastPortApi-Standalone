"""API Routing"""


from flask_restful import Resource, ResponseBase, fields, marshal_with

import api
from api.database import Session
from api.config import Config
from api.models import Loc_Fields, Location

class LocationsLast(Resource):
    @marshal_with(Loc_Fields)
    def get(self):
        return Session.query(Location).order_by(-Location.id).first()

class LocationsList(Resource):
    @marshal_with(Loc_Fields)
    def get(self):
        return Session.query(Location).all()

class LocationNow(Resource):
    @marshal_with(Loc_Fields)
    def get(self):
        now = api.sess.current_location_to_database(Config.WEB['URL'])
        return now
