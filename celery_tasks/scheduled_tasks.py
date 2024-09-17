from tasks import app
from datetime import datetime, timedelta
import time
from celery.schedules import crontab

app.conf.beat_schedule = {
    'min_task':{
        'task': 'celery_tasks.scheduled_tasks.per_min_task',
        'schedule': timedelta(seconds=60),
        'kwargs': {'arg1': 1, 'arg2': 2},
        'args': (1, 2),
        'options':{
            'queue': 'power_task',
            'priority': 5
        }
    },
    '5_sec_task':{
        'task': 'celery_tasks.scheduled_tasks.per_5_sec_task',
        'schedule': timedelta(seconds=5)
    },
    'complex_schedule':{
        'task': 'celery_tasks.scheduled_tasks.complex_schedule',
        'schedule': crontab(minute='*/1', hour='9-17', day_of_week='mon-fri')
    }
}

@app.task(name='per_min_task', queue='power_task')
def per_min_task(arg1, arg2):
    print('Task per min started...')
    time.sleep(5)
    return 'Task per min done'

@app.task(name='per_5_sec_task', queue='power_task')
def per_5_sec_task():
    print('Task per 5 sec started...')
    time.sleep(5)
    return 'Task per 5 sec done'

@app.task(name='complex_schedule', queue='power_task')
def complex_schedule():
    print('Complex schedule task started...')
    time.sleep(5)
    return 'Complex schedule task done'

'''
Corntab schedule
* * * * * (every minute)
*/5 * * * * (every 5 minutes)
30 * * * * (every hour at 30 minutes)
0 9 * * * (every day at 9:00AM)
0 14 * * 1 (every Monday at 2:00PM)
0 0 1,15 * * (every 1st and 15th of the month)
0 20,23 * * 5 (every Friday at 8:00PM and 11:00PM)
*/15 * * * * (every 15 minutes)
0 0 * * * (every day at midnight)
0 0 * * 0 (every Sunday at midnight)
0 12 * * MON (every Monday at noon)
0 0 1-7 * * (every day at midnight for the first 7 days of the month)
0 0/2 * * * (every 2 hours)
0 */6 * * * (every 6 hours)
0 0-8/2 * * 1-5 (every 2 hours from midnight to 8:00AM, Monday to Friday)
'''

