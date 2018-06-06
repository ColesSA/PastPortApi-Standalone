"""All resources needed and used by the API"""

import logging
import threading
from datetime import timedelta
from time import sleep

import requests
from bs4 import BeautifulSoup
from flask_restful import Resource, ResponseBase, fields, marshal_with
from sqlalchemy import Column, DateTime, Float, Integer, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from app.config import Config

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

def get_coords():
    with requests.get(Config.URL,
                      verify=False, 
                      auth=(Config.WEB_UID, Config.WEB_PWD)
                      ) as req:
        return BeautifulSoup(req.content, 'html.parser').find(
            'div', {'id': 'latlong'})

def store_location():
    logging.debug(' * Getting Coordinates')
    loc = Location(get_coords())
    SESSION.add(loc)
    SESSION.commit()    
    return loc

def schedule():
    logging.debug(' * Starting Scheduler Thread')
    while True:
        try:
            store_location()
            sleep(599)
        except ConnectionError as CE:
            logging.error(CE)
            SCHEDULER.start()

SCHEDULER = threading.Thread(name='Scheduler', 
                             target=schedule, 
                             daemon=True
                             )

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
        return store_location()

class Location(BASE):
    """ORM Class Model for the Location object\n
    Arguments:
        BASE {DeclarativeMeta} -- Constructor Object Type.
    """

    __tablename__ = 'locations'
    def __init__(self, coords):
        self.latitude = coords['data-latitude']
        self.longitude = coords['data-longitude']

    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, default=func.now())
    latitude = Column(Float(10))
    longitude = Column(Float(10))
