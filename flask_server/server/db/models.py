# pylint: disable=no-member
import re
import logging

from datetime import datetime

from sqlalchemy.orm import validates, composite
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from server.auth import make_thread_hash, members_from_thread_hash
from server.logging import make_logger
from server.game.geometric_types.vector import Vector
from server.game.geometric_types.rectangle import Rectangle

model_log = make_logger(__name__)


class CreatedTimestampMixin(object):
    model_log.info("Creating CreatedTimestampMixin")
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
model_log.info("Creating user_thread table")
user_thread = db.Table(
    "user_thread",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("thread_id", db.Integer, db.ForeignKey("thread.id")),
)


class Thread(CreatedTimestampMixin, db.Model):
    model_log.info("Creating thread table")
    id = db.Column(db.Integer, primary_key=True)
    thread_hash = db.Column(db.String(64))
    name = db.Column(db.String(100))

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
    model_log.info("Creating user table")
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
    user_status = db.relationship("UserStatus", uselist=False, back_populates="user")
    game_objects = db.relationship("GameObject", back_populates="owner")
    inventory_objects = db.relationship("UserInventory", back_populates="user")

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


class Message(CreatedTimestampMixin, db.Model):
    model_log.info("Creating message table")
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(256))
    color = db.Column(db.String(24))
    mods = db.Column(db.String(256))
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    thread_id = db.Column(db.Integer, db.ForeignKey("thread.id"))


class Email(db.Model):
    model_log.info("Creating email table")

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


class Environment(db.Model):
    model_log.info("Creating environment table")
    id = db.Column(db.Integer, primary_key=True)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    game_objects = db.relationship("GameObject", back_populates="environment")

    dim = composite(Vector, width, height)


game_inventory = db.Table(
    "game_inventory",
    db.Column("game_object_id", db.Integer, db.ForeignKey("game_object.id")),
    db.Column("inventory_object_id", db.Integer, db.ForeignKey("inventory_object.id")),
)


class GameObject(db.Model):
    model_log.info("Creating game_object table")
    id = db.Column(db.Integer, primary_key=True)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    posx = db.Column(db.Integer)
    posy = db.Column(db.Integer)
    acquirable = db.Column(db.Boolean)
    collidable = db.Column(db.Boolean)
    environment_id = db.Column(db.Integer, db.ForeignKey("environment.id"))
    environment = db.relationship("Environment", back_populates="game_objects")
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    owner = db.relationship("User", back_populates="game_objects")
    pos = composite(Vector, posx, posy)
    dim = composite(Vector, width, height)

    def to_dict(self):
        try:
            return {
                "id": self.id,
                "width": self.width,
                "height": self.height,
                "x": self.posx,
                "y": self.posy,
            }
        except Exception as e:
            model_log.error("GameObject.to_dict failed.")
            raise type(e)


class UserStatus(db.Model):
    model_log.info("Creating user_status table")
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    health = db.Column(db.Integer)
    weight = db.Column(db.Integer)

    user = db.relationship("User", back_populates="user_status")


class ObjectEffect(db.Model):
    model_log.info("Creating object_effect table")
    id = db.Column(db.Integer, primary_key=True)
    health = db.Column(db.Integer, default=0)
    weight = db.Column(db.Integer, default=1)

    def to_dict(self):
        return {}


class InventoryObject(db.Model):
    model_log.info("Creating inventory_object table")
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    use_effect = db.Column(db.Integer, db.ForeignKey("object_effect.id"))
    use_effect_id = db.relationship("ObjectEffect")


class UserInventory(db.Model):
    model_log.info("Creating user_inventory table")

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", back_populates="inventory_objects")

    inventory_object_id = db.Column(db.Integer, db.ForeignKey("inventory_object.id"))
    # game_object = db.relationship("GameObject")


"""
-- Display Object: Determines how something gets displayed
-- Inventory Object: Determines how an object gets saved in the inventory
-- Game Object: Objects that are currently in the game
-- UserInventory: Maps Inventory object to 
-- 


EnvironmentObjects gets Game Objects
InventoryObjects get Game Objects
EVERYONE GET GAME OBJECTS!

"""
