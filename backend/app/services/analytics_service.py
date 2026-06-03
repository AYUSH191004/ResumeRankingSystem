from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.match import MatchResult
from app.models.job import Job


# =========================================================
# JOB LEVEL ANALYTICS
# =========================================================

def job_summary(db: Session, job_id: int):
    """
    High level recruiter insight:
    How strong is the applicant pool?
    """

    # ---- Validate job ----
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise ValueError(f"Job {job_id} does not exist")

    # ---- Single aggregated query (fast) ----
    stats = db.query(
        func.count(MatchResult.id),
        func.avg(MatchResult.final_score),
        func.max(MatchResult.final_score),
        func.min(MatchResult.final_score)
    ).filter(
        MatchResult.job_id == job_id
    ).one()

    total, avg_score, top_score, min_score = stats

    return {
        "total_candidates": total or 0,
        "average_score": round(avg_score or 0, 3),
        "top_score": round(top_score or 0, 3),
        "lowest_score": round(min_score or 0, 3),
        "pool_quality": interpret_pool_quality(avg_score or 0)
    }


# =========================================================
# POOL QUALITY INTERPRETATION
# =========================================================

def interpret_pool_quality(avg_score: float) -> str:
    """
    Converts math → recruiter insight
    """

    if avg_score >= 0.75:
        return "excellent applicants"
    if avg_score >= 0.55:
        return "strong applicants"
    if avg_score >= 0.35:
        return "average applicants"
    if avg_score >= 0.2:
        return "weak applicants"
    return "very weak applicants"
