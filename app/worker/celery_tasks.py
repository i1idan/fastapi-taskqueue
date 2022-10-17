"""define celery tasks"""

from .celery_app import celery
import time

@celery.task(name="sample_task")
def sample_task(num:int):
    time.sleep(num)
    return {'status': '200'}

