import json
import logging


from flask import Flask, request,make_response, redirect
from flask_cors import CORS
from flask_socketio import SocketIO,emit,send

from server.loggers.serverlogger import request_log
from server.blueprints.authbp import authbp
from server.blueprints.registrationbp import registrationbp
from server.db import db_session
from server.serverconfig import get_config, TestingConfig

app = Flask(__name__)
app.config.from_object(TestingConfig)

logging.basicConfig(level=logging.DEBUG)



CORS(app)
socketio = SocketIO(app)

app.register_blueprint(authbp)
app.register_blueprint(registrationbp)

@app.teardown_appcontext
def cleanup(resp_or_exc):
    db_session.remove()


@app.route('/',methods=['GET','POST'])
@request_log(request)
def index_page():
    return "<h1>hello world</h1>"


@app.route('/initial-load-info', methods=['GET'])
def get_initial_load_info():
    return open('./constants/initial-load-info.json', 'rb').read()

if __name__ == "__main__":
    socketio.run(app);
