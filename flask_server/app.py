import json
import logging

from celery import Celery
from flask import Flask, request, make_response, redirect, g
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import Model
from flask_migrate import Migrate




from server.redis_cache.cachemanager import PoolManager
from server.serverconfig import get_config, TestingConfig, Config
from server.serverlogging import request_log
from server.auth import UserAuthenticator
from server.db.dbmeta import RedisORMMeta



celery = Celery(
    __name__, backend=Config.CELERY_RESULT_BACKEND, broker=Config.CELERY_BROKER_URL
)
socketio = SocketIO()
db = SQLAlchemy(model_class=declarative_base(cls=Model,metaclass=RedisORMMeta,name='model'))
migrate = Migrate()

auth = UserAuthenticator()
poolman = PoolManager()


serverlogger = logging.getLogger(__name__)
serverlogger.setLevel(logging.DEBUG)


def create_app(conf=None):
  
    app = Flask(__name__)
    config = conf if conf else get_config()
    app.config.from_object(config)
    serverlogger.debug(f"Config: {app.config}")
    poolman.init_app(app)
    RedisORMMeta._set_redis_pool(poolman)
    CORS(app)
    db.init_app(app)
    socketio.init_app(app)
    migrate.init_app(app,db=db)
    celery.conf.update(app.config)

    @app.before_request
    def attach_globs():
        if not poolman.pool:
            serverlogger.info("Init poolman")
        if not auth.app:
            serverlogger.debug("initializing UserAuthentiactor")
            auth.init_app(app)
        g.poolman = poolman
        g.auth = auth
        serverlogger.debug("Globals attached")

    # try:
    #     print('REDIS_POOL--instance:',m._REDIS_POOL)
    # except AttributeError:
    #     print('not definied in instance')

    # try:
    #     print('REDIS_POOL--instance: class',m.__class__._REDIS_POOL)
    # except AttributeError:
    #     print('not defined in class')

    from server.db.models import Message
    m = Message(content='some_content')
    print(m.CACHED)
    print(m.CACHE_KEY[1])
    



    from server.blueprints.registrationbp import registrationbp
    from server.blueprints.authbp import authbp
    from server.blueprints.userbp import userbp

    app.register_blueprint(authbp)
    serverlogger.info("Added authbp")
    app.register_blueprint(registrationbp)
    serverlogger.info("Added registrationbp")
    app.register_blueprint(userbp)
    serverlogger.info("Added userbp")

    @app.route("/", methods=["GET", "POST"])
    def index_page():

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
    app = create_app(TestingConfig)
    # app.app_context().push()
    socketio.run(app, log_output=True, log=serverlogger)
