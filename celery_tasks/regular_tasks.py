from tasks import app
from celery.utils.log import get_task_logger

@app.task(name='regular_task', queue='celery')
def task1(arg1, arg2):
    result = arg1 + arg2
    return result