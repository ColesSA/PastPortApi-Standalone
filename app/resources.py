"""API routing and Database Connection"""
from flask_restful import Resource, ResponseBase, fields, marshal_with

from app.config import Config
from app.connection import get_coords
from app.database import Session
from app.models import Loc_Fields, Location

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
        now = Location(get_coords(Config.WEB['URL'], Config.WEB['UID'], Config.WEB['PWD']))
        Session.add(now)
        Session.commit()
        return now
