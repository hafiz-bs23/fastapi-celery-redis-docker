from tasks import app
from celery.utils.log import get_task_logger
from celery import group
import logging
import time

logger = get_task_logger(__name__)

app.conf.task_acks_late = True
app.conf.task_reject_on_worker_lost = True


@app.task(name='task_net_error', queue='power_task')
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
        
        
@app.task(name='task_retry_error',
          queue='power_task',
          autoretry_for=(ConnectionError,),
          retry_backoff=True,
          retry_jitter=True,
          default_retry_delay=5,
          retry_kwargs={
              'max_retries': 5
              }
          )
def task_retry_error():
    logger.info('Task retry error started...')
    try:
        logger.info('Task retry error processing...')
        raise ConnectionError('Connection error occurred...')
    except ConnectionError as e:
        logger.error(f'Error occurred: {e}.... Retrying!')
        raise ConnectionError()
    
    
# Group task
    
@app.task(name='task_error_status',
          queue='power_task')
def task_error_status(number: int):
    logger.info('Task error status started...')
    if number == 3:
        raise ValueError('Value error occurred...')
    else:
        return number

def result_handler(result):
    if result.successful():
        logger.info(f'Task result: {result.result} ... Completed!')
    elif result.failed() and isinstance(result.result, ValueError):
        logger.error(f'Task result: {result.result} ... Failed!')
    elif result.status == 'REVOKED':
        logger.warning(f'Task result: {result.result} ... Revoked!')
    else:
        logger.error(f'Task result: {result.result} ... Failed!')
        
def run_tasks():
    task_group = group(task_error_status.s(i) for i in range(5))
    result_group = task_group.apply_async()
    result_group.get(disable_sync_subtasks=False, propagate=False, callback=result_handler)


@app.task(name='task_dead_if_failed', queue='power_task')
def task_dead_if_failed(number: int):
    try:
        if number % 2 == 0:
            return number
        else:
            raise ValueError('Value error occurred...')
    except Exception as e:
        logger.error(f'Error occurred: {e}....')
        handle_failed_task.apply_async(args=(number, str(e)))
        raise 

@app.task(name='handle_failed_tast', queue='dead_letter')
def handle_failed_task(number, error):
    logger.error(f'Failed task: {number} with error: {error}....')
    
    
@app.task(name='task_with_time_limit', queue='power_task', time_limit=10)
def task_with_time_limit(sleep_time: int):
    logger.info('Task with time limit started...')
    time.sleep(sleep_time)
    return sleep_time
    

def perform_specific_error_handling():
    pass

def notify_admins():
    pass

def perform_fallback_action():
    pass