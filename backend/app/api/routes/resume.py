from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.schemas.resume import ResumeParseResponse
from app.services.resume_service import process_resume_upload

router = APIRouter(prefix="/resume", tags=["Resume"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- Upload Resume ----------------
@router.post("/upload", response_model=ResumeParseResponse)
def upload_resume(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        return process_resume_upload(db, user_id, file)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
