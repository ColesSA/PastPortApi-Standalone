from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from app.config import Config
from sqlalchemy.ext.declarative import declarative_base

Engine = create_engine(Config.DB['URI'])
Session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=Engine))
                                    
Base = declarative_base(bind=Engine)         