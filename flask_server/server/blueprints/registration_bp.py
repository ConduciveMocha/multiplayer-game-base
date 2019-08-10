import json
import logging
from flask import Blueprint, request, jsonify

from server.db.user_actions import (
    create_account,
    query_user_by_username,
    query_user_by_email,
)
from server.logging import request_log, make_logger

registration_log = make_logger(__name__)

registration_bp = Blueprint("register", __name__, url_prefix="/register")


"""
    API endpoint for creating new user. 
"""


@registration_bp.route("/create", methods=["POST"])
@request_log(request)
def create_account():
    try:
        payload = request.get_json()
        username = payload["username"]
        password = payload["password"]
        email = payload["email"]
        return create_account(username, password, email)
    except KeyError as e:
        registration_log.error(e)
        return jsonify(error="Invalid Request")


"""
    API endpoint for checking if a username is valid before 
    account creation request is submitted.
"""


@registration_bp.route("/check-availability")
def check_availability():

    payload = request.get_json()
    email = payload.get("email", None)
    username = payload.get("username", None)

    response_dict = {}
    if email:
        registration_log.debug(f"Checking email availability: {email}")
        response_dict["email"] = (
            "Unavailable" if query_user_by_email(email) else "Available"
        )

    if username:
        registration_log.debug(f"Checking username availability: {username}")
        response_dict["username"] = (
            "Unavailable" if query_user_by_username(username) else "Available"
        )

    return jsonify(response_dict)
