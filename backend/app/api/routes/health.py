from fastapi import APIRouter
from sqlalchemy import text
from uvicorn import logging
from app.core.database import engine
from app.core.config import Settings
from app.core.logging import logger
from app.core.log_events import *
import redis
from fastapi import HTTPException
router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get("")
def health():
     return {
        "status": "healthy"
    }
  
@router.get("/ready")
def ready():
    checks = {}

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        checks["database"] = "connected"

    except Exception:
        checks["database"] = "failed"

    try:
        redis.Redis.from_url(
            Settings.REDIS_URL
        ).ping()

        checks["redis"] = "connected"
        logging.logger.info(
            "READINESS_CHECK_PASSED",
            extra={
                "checks": checks
            }
        )

    except Exception:
        checks["redis"] = "failed"

    if all(v == "connected" for v in checks.values()):
        return {
            "status": "ready",
            **checks
        }
        logging.logger.info(
            "READINESS_CHECK_FAILED",
            extra={
                "checks": checks
            }
        )
    
    raise HTTPException(
        status_code=503,
        detail={
            "status": "not_ready",
            **checks
        }
    )