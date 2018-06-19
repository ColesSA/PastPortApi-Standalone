from flask_restful import fields
from sqlalchemy import Column, DateTime, Float, Integer, func

from app.database import Base

Loc_Fields = {
    'id': fields.Integer,
    'datetime': fields.DateTime(dt_format='rfc822'),
    'latitude': fields.Float(),
    'longitude': fields.Float(),
}     

class Location(Base):
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