import os
import uuid
from sqlalchemy.orm import Session

from app.models.resume import Resume
from app.ml.parser.pipeline import ResumeParser
from app.ml.features.Profile_builder import build_resume_text
from app.services.match_service import  match_job_against_all_resumes

from app.ml.embeddings.Embedding_generator import generate_embedding
from app.tasks.matching_tasks import match_resume_task



UPLOAD_DIR = "data/raw"
parser = ResumeParser()


# -------------------------------------------------
# Save file safely (streaming)
# -------------------------------------------------
def _save_upload(file) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    unique_name = f"{uuid.uuid4()}_{file.filename}"
    path = os.path.join(UPLOAD_DIR, unique_name)

    with open(path, "wb") as buffer:
        while chunk := file.file.read(1024 * 1024):
            buffer.write(chunk)

    return path


# -------------------------------------------------
# Process Resume
# -------------------------------------------------
def process_resume_upload(db: Session, user_id: int, file):

    # 1. store file
    file_path = _save_upload(file)

    # 2. parse
    parsed = parser.parse(file_path)
    if parsed.get("status") != "success":
        raise ValueError("Resume parsing failed")

    # 3. build embedding text
    raw_text = build_resume_text(parsed)
    if not raw_text.strip():
        raise ValueError("No readable text found in resume")

    # 4. store DB
    resume = Resume(
        user_id=user_id,
        file_path=file_path,
        text=raw_text,
        parsed_data={
            "skills": parsed.get("skills"),
            "experience": parsed.get("experience"),
            "contact": parsed.get("contact")
        }
    )
    resume.embedding_vector = generate_embedding(raw_text)

    db.add(resume)
    db.commit()
    db.refresh(resume)
  

# trigger automatic matching
    match_resume_task.delay(resume.id)


    # 5. response data
    snippet = raw_text[:250].replace("\n", " ")

    experience_years = parsed.get("experience", {}).get("years_of_experience", 0)
    skills_found = parsed.get("skills", {}).get("count", 0)

    return {
        "resume_id": resume.id,
        "parse_status": "success",
        "skills_found": skills_found,
        "contact": parsed.get("contact"),
        "experience_years": experience_years,
        "text_snippet": snippet
    }
