from celery import Celery, Task
import httpx

from src.config import redis_settings

celery_app = Celery(
    "worker",
    broker=redis_settings.REDIS_DSN,
    backend=redis_settings.REDIS_DSN
)
celery_app.conf.task_track_started = True
celery_app.conf.result_expires = 3600

