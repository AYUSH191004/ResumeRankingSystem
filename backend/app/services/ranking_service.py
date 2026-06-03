from sqlalchemy.orm import Session
from sqlalchemy import desc, asc

from app.models.match import MatchResult
from app.models.job import Job


def rank_candidates_for_job(
    db: Session,
    job_id: int,
    limit: int = 10,
    offset: int = 0
):
    """
    Deterministic recruiter-facing ranking.

    Rules:
    - Stable ordering (no random tie swaps)
    - Supports pagination
    - Fails loudly if job missing
    """

    # ---- Validate job exists ----
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise ValueError(f"Job {job_id} does not exist")

    # ---- Stable deterministic ordering ----
    # tie breaker: semantic > skills > experience > resume_id
    results = (
        db.query(MatchResult)
        .filter(MatchResult.job_id == job_id)
        .order_by(
            desc(MatchResult.final_score),
            desc(MatchResult.semantic_score),
            desc(MatchResult.skill_score),
            desc(MatchResult.experience_score),
            asc(MatchResult.resume_id)
        )
        .offset(offset)
        .limit(limit)
        .all()
    )

    return [serialize_match_result(r) for r in results]


# -----------------------------
# Serialization Layer
# -----------------------------
def serialize_match_result(r: MatchResult) -> dict:
    """
    Converts DB row → API safe response.
    Keeps API independent from DB schema changes.
    """

    return {
        "resume_id": r.resume_id,
        "scores": {
            "final": round(r.final_score, 4),
            "semantic": round(r.semantic_score, 4),
            "skills": round(r.skill_score, 4),
            "experience": round(r.experience_score, 4),
        }
    }
