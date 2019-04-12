
import re

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.orm import relationship, validates
from sqlalchemy.dialects.mysql import TIMESTAMP
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

from werkzeug.security import generate_password_hash, check_password_hash
from server.auth import make_thread_id, members_from_thread_id


Base = declarative_base()

# Defines the many-to-many mapping between Users and Threads
user_thread = Table('user_thread', Base.metadata,
                    Column('user_id', Integer, ForeignKey('user.id')),
                    Column('thread_id', String(64), ForeignKey('thread.id'))
                    )


class Message(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True)
    content = Column(String(256))
    color = Column(String(24))
    mods = Column(String(256))

    sender_id = Column(Integer, ForeignKey('user.id'))
    sender = relationship("User", back_populates="sent_messages")

    thread_id = Column(String(64), ForeignKey('thread.id'))
    thread = relationship("Thread", back_populates="messages")


class Thread(Base):
    __tablename__ = "thread"
    id = Column(String(64), primary_key=True)
    thread_name = Column(String(100))

    members = relationship("User", secondary=user_thread,
                           back_populates="message_threads")
    messages = relationship("Message", back_populates="thread_id")

    def __init__(self, members, thread_name=None):
        if len(members) > 10:
            raise ValueError(
                'List of members must have fewer than 10 elements')

        member_ids = list(map(lambda user: user.id, members))
        member_names = list(map(lambda user: user.username, members))
        thread_id = make_thread_id(member_ids)

        self.id = thread_id
        self.members = members
        if thread_name:
            self.thread_name = thread_name
        else:
            self.thread_name = ""


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(16))
    password_hash = Column(String(100))
    password_salt = Column(String(10))
    email = relationship("Email", uselist=False, back_populates="user")

    sent_messages = relationship("Message", back_populates="sender")
    message_threads = relationship(
        "Thread", secondary=user_thread, back_populates="members")

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = Email(email, user=self)

    @validates('username')
    def validate_username(self, key, username):
        assert re.fullmatch(r'^[0-9_]{8,16}$', username) is None
        assert re.fullmatch(r'^[A-Za-z0-9_]{8,16}$', username) is not None
        return username

    @hybrid_property
    def password(self):
        return '$'.join(['pbkdf2:sha256', self.password_salt, self.password_hash])

    @password.setter
    def password(self, password):
        _, self.password_salt, self.password_hash = generate_password_hash(
            password).split('$')

    @hybrid_method
    def check_login(self, username, password):
        if username != self.username:
            return False
        elif not check_password_hash(self.password, password):
            return False
        else:
            return True


class Email(Base):
    __tablename__ = 'email'

    id = Column(Integer, primary_key=True)
    email = Column(String(64))
    verified = Column(Boolean)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="email")

    @validates('email')
    def validate_email(self, key, email):
        fm = re.fullmatch(
            r'^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,63}$', email, flags=re.IGNORECASE)
        assert fm != None
        return email

    def __init__(self, email, user=None):
        self.email = email
        self.verified = False
        if user is not None:
            self.user = user
