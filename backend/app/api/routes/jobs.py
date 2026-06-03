from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.schemas.job import JobCreate, JobResponse
from app.services.job_service import create_job, get_job

router = APIRouter(prefix="/jobs", tags=["Jobs"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------
# Create Job
# ---------------------------
@router.post("/", response_model=JobResponse)
def create_job_route(job: JobCreate, db: Session = Depends(get_db)):
    try:
        return create_job(db, job)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------------------------
# Get Job
# ---------------------------
@router.get("/{job_id}", response_model=JobResponse)
def get_job_route(job_id: int, db: Session = Depends(get_db)):
    try:
        return get_job(db, job_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
