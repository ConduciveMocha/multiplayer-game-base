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


from server.logging import (
    request_log,
    serverlogger,
    make_socket_loggers,
    make_logger,
    default_file_fmt,
)
from server.redis_cache.poolmanager import PoolManager
from server.serverconfig import get_config, TestingConfig, Config, DevelopmentConfig

from server.auth import UserAuthenticator

socketio_logger, engineio_logger = make_socket_loggers()

socketio = SocketIO(manage_session=False)
celery = Celery(__name__)
db = SQLAlchemy()
migrate = Migrate()
auth = UserAuthenticator()
poolman = PoolManager()

# Used to track how many app instances have been created
init = 0


def create_app(conf=None, log=False, return_ext=None):
    global init
    logger = make_logger("APPFACTORY")

    if not log:
        logger.setLevel(logging.WARNING)

    # Configures App
    app = Flask(__name__)
    config = conf if conf else get_config()
    logger.debug(f"Config name: {config.CONFIG_NAME}")
    # Session(app)
    app.config.from_object(config)
    logger.debug(f"App configured with {config.CONFIG_NAME}")

    # Logs app initialization type for debug mode
    if not config.DEBUG:
        logger.debug("Creating Application")
    elif not init:
        logger.debug("Creating watch instance")
    else:
        logger.debug("Creating Server instance")

    # Mock Setup
    if config.DEBUG or config.TESTING:
        from server.mocks import setup_mocks

        setup_mocks()

    # Configures socketio function wrappers
    from server.socket_events.socket_utils import configure_socket_functions

    # configure_socket_functions(config, logger=logger)

    # Socket event imports
    #! Dont move this or it will break things
    import server.socket_events.message_events
    import server.socket_events.debug_events
    import server.socket_events.connection_events
    import server.socket_events.game_events

    # Extention initialization
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db=db)
    socketio.init_app(
        app,
        logger=socketio_logger,
        engineio_logger=engineio_logger,
        cors_allowed_origins="*",
    )
    celery.conf.update(app.config)

    # Helper class initialization
    poolman.init_app(app)
    auth.init_app(app)

    # Attaches helper classes to g
    @app.before_request
    def attach_globs():
        g.poolman = poolman
        g.auth = auth
        serverlogger.debug("Globals attached")

    logger.debug("Extensions initialized")

    # Registering Blueprints
    from server.blueprints.registration_bp import registration_bp
    from server.blueprints.auth_bp import auth_bp
    from server.blueprints.user_bp import user_bp
    from server.blueprints.message_bp import message_bp
    from server.blueprints.load_bp import load_bp

    app.register_blueprint(auth_bp)
    logger.debug("Added authbp")
    app.register_blueprint(registration_bp)
    logger.debug("Added registrationbp")
    app.register_blueprint(user_bp)
    logger.debug("Added userbp")
    app.register_blueprint(message_bp)
    logger.debug("Added message_bp")
    app.register_blueprint(load_bp)
    logger.debug("Added load_bp")
    logger.debug("Blueprints Added")

    @app.route("/", methods=["GET", "POST"])
    def index_page():
        import server.db.game_actions

        server.db.game_actions.test3()
        return "<h1>hello world</h1>"

    # Logs app initialization type for debug mode
    if not config.DEBUG:
        logger.debug(f"App Created. Config: {app.config['CONFIG_NAME']}")
    elif not init:
        logger.debug(
            f"Application watch instance created. Config: {app.config['CONFIG_NAME']}"
        )
        init += 1
    else:
        logger.debug(
            f"Application server instance created. Config: {app.config['CONFIG_NAME']}"
        )
    if return_ext:
        if return_ext == "socketio":
            return app, socketio

    return app


if __name__ == "__main__":
    app = create_app(conf=TestingConfig, log=True)
    socketio.run(app)
