from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.schemas.analytics import JobAnalytics, RankedCandidate

# correct services
from app.services.analytics_service import job_summary
from app.services.ranking_service import rank_candidates_for_job

router = APIRouter(prefix="/analytics", tags=["Analytics"])


# -------------------------------------------------
# DB Dependency
# -------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------------------------------
# JOB SUMMARY
# -------------------------------------------------
@router.get(
    "/job/{job_id}/summary",
    response_model=JobAnalytics
)
def job_analytics(job_id: int, db: Session = Depends(get_db)):
    try:
        return job_summary(db, job_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# -------------------------------------------------
# RANKING (delegates to ranking_service)
# -------------------------------------------------
@router.get(
    "/job/{job_id}/ranking",
    response_model=list[RankedCandidate]
)
def ranking(job_id: int, limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):
    try:
        return rank_candidates_for_job(db, job_id, limit=limit, offset=offset)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
