import os
from celery import Celery
import celeryconfig
from kombu import Queue, Exchange

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379/0'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')

app = Celery('tasks',
            broker=CELERY_BROKER_URL,
            backend=CELERY_RESULT_BACKEND,
            include=['power_tasks',
                     'regular_tasks',
                     'error_tasks',
                     'error_custom_tasks',
                     'scheduled_tasks'
                     ])
app.config_from_object(celeryconfig)
app.conf.task_queues = (
    Queue('power_task', Exchange('power_task'), routing_key='power_task'),
    Queue('dead_letter', routing_key='dead_letter'),
)
app.conf.task_acks_late = True
app.conf.task_default_priority = 5
app.conf.worker_prefetch_multiplier = 1



# Prioritize a task
# Priority can be set to 0 to 9 from low to high
# can be set in task decorator or in send_task method
# Redis you can use priority to prioritize tasks by just queueing tasks to high performance worker queue