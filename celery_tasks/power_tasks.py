from tasks import app
from celery.utils.log import get_task_logger

@app.task(name='heavy_task', queue='power_task')
def heavy_task():
    return 'Heavy task done'