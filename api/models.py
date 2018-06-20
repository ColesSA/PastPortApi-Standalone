"""Contains the ORM Class Models for Database Objects"""


from flask_restful import fields
from sqlalchemy import Column, DateTime, Float, Integer, func

from api.database import Base

Loc_Fields = {
    'id': fields.Integer,
    'datetime': fields.DateTime(dt_format='rfc822'),
    'latitude': fields.Float(),
    'longitude': fields.Float(),
}     

class Location(Base):
    """Location object ORM\n
    Arguments:
        BASE {DeclarativeMeta} -- Constructor Object Type.
    """

    __tablename__ = 'locations'
    def __init__(self, coordinateTuple):
        self.latitude, self.longitude = coordinateTuple

    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, default=func.now())
    latitude = Column(Float(10))
    longitude = Column(Float(10))
