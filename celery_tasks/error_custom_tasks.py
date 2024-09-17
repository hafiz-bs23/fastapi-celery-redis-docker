from tasks import app
from celery import Task
from celery.utils.log import get_task_logger
import logging

logger = get_task_logger(__name__)

class CustomTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        if isinstance (exc, ConnectionError):
            perform_specific_error_handling()
            notify_admins()
            logger.error(f'Error occurred: {exc}....')
        else:
            logger.error(f'Error occurred: {exc}....')
            super().on_failure(exc, task_id, args, kwargs, einfo)

app.Task = CustomTask

@app.task(name='task_custom_net_error', queue='power_task')
def task_net_error():
    logger.info('Task net error started...')
    try:
        logger.info('Task net error processing...')
        raise ConnectionError('Connection error occurred...')
    except ConnectionError as e:
        logger.error(f'Error occurred: {e}....')
        logging.error(f'Error occurred: {e}....')
        raise ConnectionError()
    except ValueError as e:
        perform_fallback_action()
        logger.error(f'Error occurred: {e}....')

    
def perform_specific_error_handling():
    pass

def notify_admins():
    pass

def perform_fallback_action():
    pass