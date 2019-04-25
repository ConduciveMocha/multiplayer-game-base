import json
import logging
import logging.config
import sys

from celery import Celery
from flask import Flask, request, make_response, redirect, g
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import Model
from flask_migrate import Migrate


from server.serverlogging import (
    request_log,
    serverlogger,
    make_socket_loggers,
    make_logger,
    default_file_fmt,
)
from server.redis_cache.poolmanager import PoolManager
from server.serverconfig import get_config, TestingConfig, Config
from server.auth import UserAuthenticator


socketio_logger, engineio_logger = make_socket_loggers()
socketio = SocketIO()
celery = Celery(
    __name__, backend=Config.CELERY_RESULT_BACKEND, broker=Config.CELERY_BROKER_URL
)

db = SQLAlchemy()
migrate = Migrate()

auth = UserAuthenticator()
poolman = PoolManager()


#! Dont remove the logger kwargs or the custom logging settings will be overwritten


# TODO: Move these to serverlogging.py


def create_app(conf=None, log=False):

    logger = make_logger("APPFACTORY")
    if not log:
        logger.setLevel(logging.WARNING)
    # Socket event imports
    #! Dont move this or it will break things
    import server.socketevents.messageevents
    import server.socketevents.debugevents
    import server.socketevents.connectionevents

    app = Flask(__name__)
    config = conf if conf else get_config()

    logger.debug(f"Config name: {config.CONFIG_NAME}")
    app.config.from_object(config)
    logger.debug("App configured successfully")

    CORS(app)
    db.init_app(app)
    socketio.init_app(app, logger=socketio_logger, engineio_logger=engineio_logger)
    migrate.init_app(app, db=db)
    celery.conf.update(app.config)

    poolman.init_app(app)
    auth.init_app(app)

    logger.debug("Extensions initialized")

    @app.before_request
    def attach_globs():
        g.poolman = poolman
        g.auth = auth
        serverlogger.debug("Globals attached")

    from server.blueprints.registrationbp import registrationbp
    from server.blueprints.authbp import authbp
    from server.blueprints.userbp import userbp

    app.register_blueprint(authbp)
    logger.debug("Added authbp")
    app.register_blueprint(registrationbp)
    logger.debug("Added registrationbp")
    app.register_blueprint(userbp)
    logger.debug("Added userbp")
    logger.debug("Blueprints Added")

    @app.route("/", methods=["GET", "POST"])
    def index_page():

        return "<h1>hello world</h1>"

    return app


if __name__ == "__main__":

    app = create_app(log=True)

    serverlogger.debug(f"App Created. Config: {app.config['CONFIG_NAME']}")
    socketio.run(app)
