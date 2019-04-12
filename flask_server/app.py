import json
import logging

from celery import Celery
from flask import Flask, request, make_response, redirect
from flask_cors import CORS
from flask_socketio import SocketIO, emit, send

from server.loggers.serverlogger import request_log
from server.blueprints.authbp import authbp
from server.blueprints.registrationbp import registrationbp
from server.db import db_session
from server.serverconfig import get_config, TestingConfig, Config


celery = Celery(__name__, backend=Config.CELERY_RESULT_BACKEND,
                broker=Config.CELERY_BROKER_URL)
socketio = SocketIO()


def create_application(conf=None):
    config = conf if conf else get_config()
    app = Flask(__name__)
    app.config.from_object(config)

    CORS(app)
    socketio.init_app(app)
    celery.conf.update(app.config)

    @app.teardown_appcontext
    def cleanup(resp_or_exc):
        db_session.remove()

    app.register_blueprint(authbp)
    app.register_blueprint(registrationbp)

    @app.route('/', methods=['GET', 'POST'])
    def index_page():
        from server.celery_tasks.tasks import print_hello

        logging.debug('Help me!')
        result = print_hello.delay()
        result.wait()
        return "<h1>hello world</h1>"

    return app


# @app.teardown_appcontext
# def cleanup(resp_or_exc):
#     db_session.remove()


# @request_log(request)

# @app.route('/initial-load-info', methods=['GET'])
# def get_initial_load_info():
#     return open('./constants/initial-load-info.json', 'rb').read()


if __name__ == "__main__":
    app = create_application(TestingConfig)
    socketio.run(app)
