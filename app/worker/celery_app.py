"""define celery job queue to run the tasks in the background."""

from celery import Celery
from .config import Config
import os

#  Backend: Keep track of task results in a database.
#  Broker: Mediate between clients and workers.
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', f"amqp://{Config.RABBITMQ_USERNAME}:{Config.RABBITMQ_PASSWORD}@{Config.RABBITMQ_HOST}:{Config.RABBITMQ_PORT}")
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', f"redis://{Config.REDIS_HOST}:{Config.REDIS_PORT}/{Config.REDIS_STORE_DB_INDEX}")


# Initialize Celery
celery = Celery('APP', broker_url=CELERY_BROKER_URL, result_backend=CELERY_RESULT_BACKEND)
