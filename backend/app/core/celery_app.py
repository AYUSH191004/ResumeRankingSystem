from celery import Celery, Task
from celery.signals import worker_ready
from app.core.logging import logger
from app.core.log_events import *
from app.core.config import settings


class BaseRetryTask(Task):
    autoretry_for = (Exception,)

    retry_backoff = True
    retry_backoff_max = 300

    retry_jitter = True

    max_retries = 5

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        logger.warning(
            "TASK_RETRY",
            extra={
                "task_id": task_id,
                "task_name": self.name,
                "error": str(exc)
            }
        )

    def on_failure(
        self,
        exc,
        task_id,
        args,
        kwargs,
        einfo,
    ):
        logger.exception(
            "TASK_FAILURE",
            extra={
                "task_id": task_id,
                "task_name": self.name,
                "error": str(exc)
            }
        )


celery_app = Celery(
    "worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)
@worker_ready.connect
def on_worker_ready(**kwargs):
    logger.info("CELERY_WORKER_READY", extra={"event": "worker_ready"})

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,

    task_soft_time_limit=300,
    task_time_limit=360
)