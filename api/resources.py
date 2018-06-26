"""API Routing"""


from flask_restful import Resource, marshal_with

import api
from api.config import Config
from api.database import session, to_database
from api.models import Loc_Fields, Location, Coordinate

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
        return session.query(Location).order_by(-Location.id).first()

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
        return session.query(Location).all()

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
        _response = api.conn.get_from(Config.WEB['URL'])
        _coordinate = Coordinate.from_request(_response)
        _location = Location.get_new(_coordinate)
        return to_database(_location)
