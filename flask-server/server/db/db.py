import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.db.declaratives import Base,User,Email,PrivateMessage

engine = create_engine('mysql+pymysql://egghunt:password@localhost:3306/multiplayerserver')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)