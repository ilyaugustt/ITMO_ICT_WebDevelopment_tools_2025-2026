import os
from celery import Celery

redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
celery_broker_url = os.getenv("CELERY_BROKER_URL", redis_url)
celery_backend_url = os.getenv("CELERY_RESULT_BACKEND", redis_url)

app = Celery(
    "parser",
    broker=celery_broker_url,
    backend=celery_backend_url,
    include=["main"]
)

app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,  # 5 минут максимум на задачу
    broker_connection_retry_on_startup=True,
)

app.autodiscover_tasks(force=False)
