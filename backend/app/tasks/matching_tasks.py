from app.core.celery_app import (
    celery_app,
    BaseRetryTask
)
from app.core.logging import logger
from app.core.log_events import *
from app.services.match_service import (
    match_resume_against_all_jobs,
    match_job_against_all_resumes
)


@celery_app.task(
    bind=True,
    base=BaseRetryTask,
    name="matching.match_resume"
)
def match_resume_task(self,resume_id: int):

    logger.info(
        TASK_STARTED,
        extra={"resume_id": resume_id}
    )

    try:
        match_resume_against_all_jobs(resume_id)

        logger.info(
            TASK_COMPLETED,
            extra={"resume_id": resume_id}
        )

    except Exception:
        logger.exception(
            TASK_FAILED,
            extra={"resume_id": resume_id}
        )
        raise


@celery_app.task(
    bind=True,
    base=BaseRetryTask,
    name="matching.match_job")
def match_job_task(self,job_id: int):

    logger.info(
        TASK_STARTED,
        extra={"job_id": job_id}
    )

    try:
        match_job_against_all_resumes(job_id)

        logger.info(
            TASK_COMPLETED,
            extra={"job_id": job_id}
        )

    except Exception:
        logger.exception(
            TASK_FAILED,
            extra={"job_id": job_id}
        )
        raise