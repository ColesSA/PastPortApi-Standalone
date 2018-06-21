"""API Routing"""


from flask_restful import Resource, marshal_with

import api
from api.config import Config
from api.database import Session
from api.models import Loc_Fields, Location

class LocationsLast(Resource):
    """Last location stored in the database

    Returns:
        json -- last location stored in the database
    """
    @marshal_with(Loc_Fields)
    def get(self):
        """GET request
        
        Returns:
            json -- location
        """
        return Session.query(Location).order_by(-Location.id).first()

class LocationsList(Resource):
    """All locations stored in the database

    Returns:
        json -- all locations stored in the database
    """
    @marshal_with(Loc_Fields)
    def get(self):
        """GET request
        
        Returns:
            json -- location list
        """
        return Session.query(Location).all()

class LocationNow(Resource):
    """Stores the current location into the database

    Returns:
        json -- last location stored in the database
    """
    @marshal_with(Loc_Fields)
    def get(self):
        """GET request
        
        Returns:
            json -- location
        """
        now = api.conn.current_location(Config.WEB['URL'])
        return now
