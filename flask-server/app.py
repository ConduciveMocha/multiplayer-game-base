import json
import logging

from serverconfig import get_config

from flask import Flask, request,make_response, redirect
from flask_cors import CORS
from flask_socketio import SocketIO,emit,send

from server.loggers.serverlogger import request_log
from server.blueprints.authbp import bp as authbp
from server.blueprints.registrationbp import bp as registerationbp


app = Flask(__name__)
app.config.from_object(get_config())

# app.config['DEBUG'] = True
# logging.basicConfig(level=logging.DEBUG)



app.config['SECRET_KEY'] = 'secret!secret!';
CORS(app)
socketio = SocketIO(app)
app.register_blueprint(authbp)
app.register_blueprint(registerationbp)


@app.route('/',methods=['GET','POST'])
@request_log(request)
def index_page():
    return "<h1>hello world</h1>"


@app.route('/initial-load-info', methods=['GET'])
def get_initial_load_info():
    return open('./constants/initial-load-info.json', 'rb').read()
    
@socketio.on('message')
def handle_message(message):
    emit('private message', ('fooo'))

@socketio.on('private message')
def handle_connect(data):
    
    x =  '{ "name":"John", "age":30, "city":"New York"}'
    emit('private message', x)

if __name__ == "__main__":
    socketio.run(app);
