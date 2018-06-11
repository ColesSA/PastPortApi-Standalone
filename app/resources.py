"""API routing and Database Connection"""
from flask_restful import Resource, ResponseBase, fields, marshal_with
from flask import request
from sqlalchemy import Column, DateTime, Float, Integer, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from app.config import Config
from app.connection import safe_session, DEBUGGER, LOGGER

import time

from bs4 import BeautifulSoup

DB=Config.DB
ENGINE = create_engine(DB['URI'])
SESSION = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=ENGINE
                                      )
                        )
BASE = declarative_base(bind=ENGINE)
LOC_FIELDS = {
    'id': fields.Integer,
    'datetime': fields.DateTime(dt_format='rfc822'),
    'latitude': fields.Float(),
    'longitude': fields.Float(),
} 

class Hound(object): 
    def get_coords():
        t0 = time.time()
        try:
            DEBUGGER.debug(' * Getting Coordinates')
            req = safe_session()
            req.raise_for_status()
        except Exception as x:
            LOGGER.exception('Connection failed, {}'.format(x))
        else:
            DEBUGGER.debug('Connection Successful, {}'.format(req.status_code))
            soup = BeautifulSoup(req.content, 'html.parser').find('div', {'id': 'latlong'})
            coords = (soup['data-latitude'],soup['data-longitude'])
            loc = Location(coords)
            SESSION.add(loc)
            SESSION.commit() 
            return loc
        finally:
            t1 = time.time()
            DEBUGGER.debug('Took {} seconds'.format(t1-t0))
         

class LocationsLast(Resource):
    @marshal_with(LOC_FIELDS)
    def get(self):
        return SESSION.query(Location).order_by(-Location.id).first()

class LocationsList(Resource):
    @marshal_with(LOC_FIELDS)
    def get(self):
        return SESSION.query(Location).all()

class Now(Resource):
    @marshal_with(LOC_FIELDS)
    def get(self):
        return Hound.get_coords

class Location(BASE):
    """ORM Class Model for the Location object\n
    Arguments:
        BASE {DeclarativeMeta} -- Constructor Object Type.
    """

    __tablename__ = 'locations'
    def __init__(self, coords):
        self.latitude, self.longitude = coords

    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, default=func.now())
    latitude = Column(Float(10))
    longitude = Column(Float(10))
