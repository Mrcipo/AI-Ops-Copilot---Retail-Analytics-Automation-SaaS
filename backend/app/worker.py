from celery import Celery

from .core.config import settings

celery_app = Celery(
    "worker",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.broker_connection_retry_on_startup = True
