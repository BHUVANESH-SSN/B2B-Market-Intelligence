from __future__ import annotations

import ssl

from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "market_intelligence",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.workers.tasks"],
)

celery_app.conf.broker_connection_retry_on_startup = True
celery_app.conf.task_track_started = True

if settings.redis_url.startswith("rediss://"):
    ssl_options = {"ssl_cert_reqs": ssl.CERT_REQUIRED}
    celery_app.conf.broker_use_ssl = ssl_options
    celery_app.conf.redis_backend_use_ssl = ssl_options
