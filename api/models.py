"""Contains the ORM Class Models for Database Objects"""

import logging

from bs4 import BeautifulSoup
from flask_restful import fields
from sqlalchemy import Column, DateTime, Float, Integer, func

from api.database import base

Loc_Fields = {
    'id': fields.Integer,
    'datetime': fields.DateTime(dt_format='rfc822'),
    'latitude': fields.Float(),
    'longitude': fields.Float(),
}     

class Coordinate(object):
    """Cooordinate Functions"""
    @staticmethod
    def from_request(req):
        """Format the request into a coordinate tuple
        
        Arguments:
            req {Requests response object} -- the response containing the data
        """
        _soup = BeautifulSoup(req.content, 'html.parser').find('div', {'id': 'latlong'})
        _coords = (_soup['data-latitude'], _soup['data-longitude'])
        return _coords

class Location(base):
    """Location ORM"""

    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, default=func.now())
    latitude = Column(Float(10))
    longitude = Column(Float(10))           

    @staticmethod
    def get_new(coords):
        """Instatiate a location from a request.

        Arguments:
            req {Request} -- requests_retry_session response     

        Returns:
            Location -- the instantiated location object with lat,lon from request
        """
        _loc = Location()
        _loc.latitude, _loc.longitude = coords
        return _loc
    