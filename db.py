"""SQLAlchemy session creation"""
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from config import DB_URI

SESSION_FACTORY = sessionmaker(autocommit=False,
                               autoflush=False,
                               bind=create_engine(DB_URI))

SESSION = scoped_session(SESSION_FACTORY)
