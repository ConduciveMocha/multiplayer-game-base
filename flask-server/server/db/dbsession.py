import re
import logging

from contextlib import contextmanager
from .db import Session
class DBSession():
    def __init__(self):
        self.session = None

        self.log = logging.getLogger(type(self).__name__)
        self.log.setLevel(logging.INFO)  
        

    @contextmanager
    def db_open(self):

        self.session = Session()
        self.log.info('SESSION OPENED')
        yield self.session
        self.session.close()
        self.log.info('SESSION CLOSED')
        self.session = None
