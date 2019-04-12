
from app import celery
import logging


@celery.task(name='server.celery_tasks.tasks.print_hello')
def print_hello():

    logging.info("hello")
