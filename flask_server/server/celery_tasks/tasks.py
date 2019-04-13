
from celery.utils.log import get_task_logger
from app import celery
import logging

logger = get_task_logger('server.celery_tasks.tasks.print_hello')


@celery.task(name='server.celery_tasks.tasks.print_hello')
def print_hello():
    logger.info(__name__)
    logging.info("hello")
