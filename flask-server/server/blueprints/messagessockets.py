from flask import session
from flask_socketio import emit, join_room, leave_room
from ...app import socketio

@socketio.on('MESSAGE_SENT', namespace='/message')
def process_message(message):
    pass

@socketio.on('MESSAGE_RECIEVED', namespace='/message')
def notify_recieved(message):
    pass

@socketio.on('MESSAGE_READ', namespace='/message')
def notify_read(message):
    pass

@socketio.on('GLOBAL_SENT', namespace='/message')
def process_global(message):
    pass

@socketio.on('CONFIRM_ALIVE', namespace='/message')
def confirm_alive(message):
    pass

def join_room_request(user_list,room_id):
    pass

def join_room_failed(user,room_id):
    pass

def room_closed(user_list,room_id):
    pass

def user_login(user_id):
    pass

def user_logout(user_id):
    pass

def send_new_message(message_id,message,user_id,room_id):
    pass

def message_failed(message_id,user_id):
    pass

def message_persisted(message_id,user_id):
    pass

def message_recieved(message_id, sender_id,recipient_id):
    pass

def message_read(message_id, sender_id,recipient_id):
    pass

def send_new_global(message_id,message,user_id):
    pass

def global_failed(message_id, user_id):
    pass

def check_is_alive(user_id):
    pass

