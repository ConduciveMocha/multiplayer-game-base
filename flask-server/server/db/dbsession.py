import re
import logging

from contextlib import contextmanager
from .db import Session
class DBSession():
    def __init__(self):
        self.session = None

    @contextmanager
    def db_open(self):

        self.session = Session()
        logging.info('MYSQL: SESSION CREATED')
        yield self.session
        self.session.close()
        logging.info('MYSQL: SESSION CLOSED')
        self.session = None
