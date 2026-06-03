from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.schemas.match import ResumeMatchResponse
from app.services.match_service import match_resume_to_job as match_resume_to_job_service

router = APIRouter(prefix="/match", tags=["Matching"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/resume/{resume_id}/job/{job_id}",
    response_model=ResumeMatchResponse
)
def match_resume_to_job(resume_id: int, job_id: int, db: Session = Depends(get_db)):

    try:
        match = match_resume_to_job_service(resume_id, job_id)

        return ResumeMatchResponse(
            resume_id=match.resume_id,
            job_id=match.job_id,
            semantic_score=match.semantic_score,
            skill_score=match.skill_score,
            experience_score=match.experience_score,
            final_score=match.final_score,
            explanation=match.explanation
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
