import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from server.models import Base

engine = create_engine(
    'mysql+pymysql://egghunt:password@localhost:3306/multiplayerserver')
db_session = scoped_session(sessionmaker(
    bind=engine, autocommit=False, autoflush=False))

Base.query = db_session.query_property()

Base.metadata.create_all(engine)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
