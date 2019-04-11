
import re

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import  declared_attr,declarative_base
from sqlalchemy.orm import relationship,validates
from sqlalchemy.dialects.mysql import TIMESTAMP
from sqlalchemy.ext.hybrid import hybrid_property,hybrid_method

from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()

class PrivateMessage(Base):
    __tablename__ = "privatemessages"

    id = Column(Integer, primary_key=True)
    content = Column(String(256))
    sender_id = Column(Integer, ForeignKey("users.id"))
    reciever_id = Column(Integer, ForeignKey("users.id"))
    timestamp = Column(TIMESTAMP)


    
class User(Base):
    __tablename__='users'

    id = Column(Integer,primary_key=True)
    username = Column(String(16))
    password_hash = Column(String(100))
    password_salt = Column(String(10))
    email = relationship("Email", uselist=False,back_populates="user")
    sent_messages = relationship("PrivateMessage",foreign_keys=[PrivateMessage.sender_id])
    recieved_messages = relationship("PrivateMessage",foreign_keys=[PrivateMessage.reciever_id])

    def __init__(self,username,password,email):
        self.username=username
        self.password = password
        self.email = Email(email,user=self)
    
    @validates('username')
    def validate_username(self,key,username):
        assert re.fullmatch(r'^[0-9_]{8,16}$', username) is None
        assert re.fullmatch(r'^[A-Za-z0-9_]{8,16}$', username) is not None
        return username

    @hybrid_property
    def password(self):
        return '$'.join(['pbkdf2:sha256', self.password_salt, self.password_hash])

    @password.setter
    def password(self,password):
        _, self.password_salt, self.password_hash = generate_password_hash(password).split('$')


    @hybrid_method
    def check_login(self,username,password):
        if username != self.username:
            return False
        elif not check_password_hash(self.password, password):
            return False
        else:
            return True


class Email(Base):
    __tablename__='emails'

    id = Column(Integer, primary_key=True)
    email = Column(String(64))
    verified = Column(Boolean)
    user_id = Column(Integer,ForeignKey("users.id"))
    user = relationship("User", back_populates="email")
    
    @validates('email')
    def validate_email(self, key, email):
        fm = re.fullmatch(
            r'^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,63}$', email, flags=re.IGNORECASE)
        assert fm != None
        return email
    def __init__(self,email,user=None):
        self.email = email
        self.verified = False
        if user is not None:
            self.user = user





