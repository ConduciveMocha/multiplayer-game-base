import json
from flask import Blueprint,request,make_response


bp = Blueprint('message',__name__,url_prefix='/message')

@bp.route('/create')
def request_thread():
    pass

@bp.route('/history')
def thread_history():
    pass