import logging

from flask import jsonify

from app import db
from server.db.models import User
from server.logging import make_logger

ua_logger = make_logger(__name__)


def verify_user(username, password):
    user_match = User.query.filter_by(username=username).first()
    if not user_match:
        ua_logger.info(f"No user {username} found")
        return None
    else:
        return user_match if user_match.check_login(username, password) else None


def query_user_by_id(user_id):
    return User.query.filter_by(id=user_id).first()


def query_user_by_username(username):
    return User.query.filter_by(username=username).first()


def query_user_by_email(email):

    return User.query.filter_by(email=email).first()


def create_account(username, password, email):
    try:
        new_user = User(username, password, email)
        db.session.add(new_user)
        db.session.commit()
        ua_logger.info(f"New user `{username}` created")
        return jsonify(message="success", userId=new_user.user_id)
    except AssertionError as e:
        ua_logger.error(e)
        return jsonify(error="Invalid username or password")

    except Exception as e:
        ua_logger.error(e)
        return jsonify(error="Internal Error")
