# pylint: disable=no-member
import re
import logging

from datetime import datetime

from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from server.auth import make_thread_hash, members_from_thread_hash
from server.logging import make_logger

model_log = make_logger(__name__)

class CreatedTimestampMixin(object):
    created = db.Column(db.DateTime, default=datetime.utcnow)

    @validates("created")
    def _validate_created(self, key, created):
        assert Thread.validate_created(created) == True
        return created

    @staticmethod
    def validate_created(created):
        if datetime.utcnow >= created:
            return True
        else:
            return False


# Defines the many-to-many mapping between Users and Threads
user_thread = db.Table(
    "user_thread",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("thread_id", db.Integer, db.ForeignKey("thread.id")),
)


class Message(CreatedTimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(256))
    color = db.Column(db.String(24))
    mods = db.Column(db.String(256))
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    thread_id = db.Column(db.Integer, db.ForeignKey("thread.id"))


class Thread(CreatedTimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thread_hash = db.Column(db.String(64))
    name = db.Column(db.String(100))

    # members = db.relationship("User",secondary=user_thread,primaryjoin=(user_thread.c.thread_id==id),lazy='dynamic')
    def __init__(self, members, thread_hash, created, thread_name=None):
        if len(members) > 10:
            raise ValueError("List of members must have fewer than 10 elements")

        member_ids = list(map(lambda user: user.id, members))
        self.thread_hash = make_thread_hash(member_ids)

        self.members = members
        self.created = created

        if thread_name:
            self.thread_name = thread_name

        else:
            self.thread_name = ""


class User(CreatedTimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16))
    password_hash = db.Column(db.String(100))
    password_salt = db.Column(db.String(10))
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    email = db.relationship("Email", uselist=False, backref="user", lazy=True)
    sent_messages = db.relationship("Message", backref="sender")
    message_threads = db.relationship(
        "Thread",
        secondary=user_thread,
        lazy="dynamic",
        backref=db.backref("members", lazy="dynamic"),
    )

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = Email(email, user=self)

    @validates("username")
    def _validate_username(self, key, username):
        assert User.validate_username(username) == True
        return username

    @hybrid_property
    def password(self):
        return "$".join(["pbkdf2:sha256", self.password_salt, self.password_hash])

    @password.setter
    def password(self, password):
        _, self.password_salt, self.password_hash = generate_password_hash(
            password
        ).split("$")

    @hybrid_method
    def check_login(self, username, password):
        if username != self.username:
            return False
        elif not check_password_hash(self.password, password):
            return False
        else:
            return True

    @staticmethod
    def validate_username(username):
        if re.fullmatch(r"^[0-9_]{8,16}$", username) is not None:
            model_log.debug(
                f'Invalid Username ({username}): Starts with a number or "_"'
            )
            return False
        elif re.fullmatch(r"^[A-Za-z0-9_]{8,16}$", username) is None:
            model_log.debug(
                f"Invalid Username ({username}): Contains invalid character"
            )
            return False
        else:
            return True

    @staticmethod
    def validate_password(password):

        if re.fullmatch(r"^[\S]{8,16}$", password):
            return True
        else:
            model_log.debug(
                f"Invalid password ({password}): Included whitespace character"
            )
            return False


class Email(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(75))
    verified = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, email, user=None):
        self.email = email.lower()
        self.verified = False
        if user is not None:
            self.user = user

    @validates("email")
    def _validate_email(self, key, email):
        assert Email.validate_email(email) == True
        return email

    @staticmethod
    def validate_email(email):
        fm = re.fullmatch(
            r"^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,63}$", email, flags=re.IGNORECASE
        )
        valid = fm != None
        if not valid:
            model_log.debug(f"Invalid Email ({email})")
        return valid
