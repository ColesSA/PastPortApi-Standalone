"""Contains the ORM Class Models for Database Objects"""

import logging

from bs4 import BeautifulSoup
from flask_restful import fields
from sqlalchemy import Column, DateTime, Float, Integer, func

from api.database import Base, Session

Loc_Fields = {
    'id': fields.Integer,
    'datetime': fields.DateTime(dt_format='rfc822'),
    'latitude': fields.Float(),
    'longitude': fields.Float(),
}     

class Location(Base):
    """Location object ORM"""

    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, default=func.now())
    latitude = Column(Float(10))
    longitude = Column(Float(10))

    def set_coordinates(self, coordinate_tuple):
        """Populate the latitude and longitude of the Location with tuple values

        Arguments:
            coordinate_tuple {tuple} -- Tuple containing the latitude and longitude
        """

        self.latitude, self.longitude = coordinate_tuple

    @staticmethod
    def from_request(req, to_database):
        """Instatiate a location from a request.

        Arguments:
            req {Request} -- requests_retry_session response
            to_database {bool} -- Whether to store in database or not (default: {True})            

        Returns:
            Location -- the instantiated location object with lat,lon from request
        """

        _db = to_database
        _soup = BeautifulSoup(req.content, 'html.parser').find('div', {'id': 'latlong'})
        _coords = (_soup['data-latitude'], _soup['data-longitude'])
        _loc = Location()
        _loc.set_coordinates(_coords)
        if _db:
            Session.add(_loc)
            Session.commit()
        else:
            logging.info('Location was not stored to database')
        return _loc
    