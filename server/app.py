
  
import json
import logging

from flask import Flask, request,make_response, redirect
from flask_cors import CORS
from flask_socketio import SocketIO,emit,send

from loggers.serverlogger import request_log
from blueprints.authbp import bp as authbp
from blueprints.registrationbp import bp as registerationbp


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!secret!';
CORS(app)
socketio = SocketIO(app)
logging.basicConfig(level=logging.DEBUG)
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
    54455
    x =  '{ "name":"John", "age":30, "city":"New York"}'
    emit('private message', x)

if __name__ == "__main__":
    socketio.run(app);
