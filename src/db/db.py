from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src.db.session import SessionManager

Base = declarative_base()

class DB:
    def __init__(self, db_uri):
        self.engine = create_engine(db_uri)
        self.Session = sessionmaker(bind=self.engine)
        self.session_manager = SessionManager(self.Session())

    def create_all(self):
        Base.metadata.create_all(self.engine)
