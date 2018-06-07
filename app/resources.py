"""All resources needed and used by the API"""
import logging
from flask_restful import Resource, ResponseBase, fields, marshal_with
from flask import request
from sqlalchemy import Column, DateTime, Float, Integer, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from app.config import Config
from app.connection import get_secure_coords

import json

ENGINE = create_engine(Config.DB_URI)
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

@marshal_with(LOC_FIELDS)
def db_store(coords):
    loc = Location(coords)
    SESSION.add(loc)
    SESSION.commit() 
    return loc

def store_location(coords):
    if(isinstance(coords,tuple)):
        return db_store(coords)

class LocationsLast(Resource):
    def get(self):
        return SESSION.query(Location).order_by(-Location.id).first()

class LocationsList(Resource):
    @marshal_with(LOC_FIELDS)
    def get(self):
        return SESSION.query(Location).all()

class Now(Resource):
    def get(self):
        return store_location(get_secure_coords())

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
