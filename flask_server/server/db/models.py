
import re
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from server.auth import make_thread_hash, members_from_thread_hash


# Defines the many-to-many mapping between Users and Threads
user_thread = db.Table('user_thread', db.Model.metadata,
                       db.Column('user_id', db.Integer,
                                 db.ForeignKey('user.id')),
                       db.Column('thread_id', db.String(64),
                                 db.ForeignKey('thread.id'))
                       )


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(256))
    color = db.Column(db.String(24))
    mods = db.Column(db.String(256))
    sent_time = db.Column(db.DateTime)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    thread_id = db.Column(db.String(64), db.ForeignKey('thread.id'))


class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thread_hash = db.Column(db.String(64))
    thread_name = db.Column(db.String(100))
    created_time = db.Column(db.DateTime)

    def __init__(self, members, thread_hash, created_time, thread_name=None):
        if len(members) > 10:
            raise ValueError(
                'List of members must have fewer than 10 elements')

        member_ids = list(map(lambda user: user.id, members))
        self.thread_hash = make_thread_hash(member_ids)

        self.members = members
        if thread_name:
            self.thread_name = thread_name
        else:
            self.thread_name = ""


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16))
    password_hash = db.Column(db.String(100))
    password_salt = db.Column(db.String(10))
    email = db.relationship("Email", uselist=False, backref="user", lazy=True)

    sent_messages = db.relationship("Message", backref="sender")
    message_threads = db.relationship(
        "Thread", secondary=user_thread, backref="members")

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


class Email(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64))
    verified = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

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
