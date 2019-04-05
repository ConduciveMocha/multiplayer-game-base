from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship,sessionmaker
from sqlalchemy.dialects.mysql import TIMESTAMP

Base = declarative_base()

# Generates a __repr__ function for a given declarative
def db_repr(s):
    ret = f"{s.__class__.__name__} <"
    for field in filter(lambda x: x[0] != '_' and x != 'metadata', s.__class__.__dict__.keys()):
        if len(ret) - ret.find('\n')>50:
            ret = ret + '\n' + ' ' * (len(s.__class__.__name__) + 2)
        ret = ret + f'{field}=({s.__dict__[field]}) '

    return ret+'>'




class PrivateMessage(Base):
    __tablename__ = "privatemessages"

    id = Column(Integer, primary_key=True)
    content = Column(String(256))
    sender_id = Column(Integer, ForeignKey("users.id"))
    reciever_id = Column(Integer, ForeignKey("users.id"))
    timestamp = Column(TIMESTAMP)

    __repr__ = db_repr

    
class User(Base):
    __tablename__='users'

    id = Column(Integer,primary_key=True)
    username = Column(String(16))
    password_hash = Column(String(100))
    password_salt = Column(String(10))
    email = relationship("Email", uselist=False,back_populates="user")
    sent_messages = relationship("PrivateMessage",foreign_keys=[PrivateMessage.sender_id])
    recieved_messages = relationship("PrivateMessage",foreign_keys=[PrivateMessage.reciever_id])

    __repr__ = db_repr

class Email(Base):
    __tablename__='emails'

    id = Column(Integer, primary_key=True)
    email = Column(String(64))
    verified = Column(Boolean)
    user_id = Column(Integer,ForeignKey("users.id"))
    user = relationship("User", back_populates="email")

    __repr__ = db_repr



