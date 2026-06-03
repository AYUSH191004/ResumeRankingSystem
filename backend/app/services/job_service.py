from sqlalchemy.orm import Session
from app.models.job import Job
from app.services.match_service import match_job_against_all_resumes
from app.ml.embeddings.Embedding_generator import generate_embedding
from app.tasks.matching_tasks import match_resume_task
# -----------------------------------------
# Utilities
# -----------------------------------------
def _serialize_job(job: Job) -> dict:
    return {
        "id": job.id,
        "title": job.title,
        "description": job.description,
        "required_skills": _parse_skills(job.required_skills),
        "min_experience": job.min_experience,
        "status": job.status,
        "created_at": job.created_at
    }


def _parse_skills(skill_text: str):
    if not skill_text:
        return []
    return [s.strip() for s in skill_text.split(",") if s.strip()]


# -----------------------------------------
# Create Job
# -----------------------------------------
def create_job(db: Session, job_data, recruiter_id: int = 1):
    embedding = generate_embedding(job_data.description)

    db_job = Job(
    title=job_data.title,
    description=job_data.description,
    required_skills=job_data.required_skills,
    min_experience=job_data.min_experience,
    recruiter_id=recruiter_id,
    status="open",
    embedding_vector=embedding
)


    db.add(db_job)
    db.commit()
    db.refresh(db_job)

# trigger automatic evaluation

    match_resume_task.delay(db_job.id)

    return _serialize_job(db_job)



# -----------------------------------------
# Get Job
# -----------------------------------------
def get_job(db: Session, job_id: int):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise ValueError("Job not found")

    return _serialize_job(job)
