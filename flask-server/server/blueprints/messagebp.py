import json
import base64
from flask import Blueprint, request,make_response
from flask_socketio import SocketIO,emit,send,Namespace

bp = Blueprint('message', __name__,url_prefix='/message')

def make_thread_id(members):
    enc = '_'.join(map(lambda x: str(x),members.sort()))
    return base64.b64encode(enc.encode('utf-8')).decode('utf-8')
def members_from_thread_id(thread_id):
    dec = base64.b64decode(thread_id).decode('utf-8')
    dec = dec.split('_')
    members = []
    for i,m in enumerate(dec):
        if i == 0:
            members.append(int(m))
        else:
            members.append(members[-1] + int(m))
    return members        
@bp.route('/getthread', methods=['GET'])
def get_thread():
    try:
        payload = request.get_json()
        members = payload.get('members', None)
                
    except Exception as e:
        return e.message

# class MessageThreadNamespace(Namespace):

#     def __init__(self,namespace_route,)

#     def on_connect(self):
#         pass
#     def on_disconnect(self):
#         pass
    
#     def on_connection_stale(self,data):
#         pass

#     def on_new_message(self,data):
#         pass



# @socketio.on('message')
# def handle_message(message):
#     emit('private message', ('fooo'))


# @socketio.on('private message')
# def handle_connect(data):

#     x = '{ "name":"John", "age":30, "city":"New York"}'
#     emit('private message', x)



@bp.route('/create')
def request_thread():
    pass

@bp.route('/history')
def thread_history():
    pass
