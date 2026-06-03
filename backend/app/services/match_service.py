from app.core.database import SessionLocal
from app.core.logging import logger
from app.core.log_events import *
from app.models.match import MatchResult
from app.models.resume import Resume
from app.models.job import Job
import time
from app.ml.matcher.pipeline import run_matching


# ----------------------------------------
# Core Compute
# ----------------------------------------
def compute_match(resume, job):
    return run_matching(resume, job)


# ----------------------------------------
# Single Match (optional API use)
# ----------------------------------------
def match_resume_to_job(resume_id: int, job_id: int):
    db = SessionLocal()
    try:
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        job = db.query(Job).filter(Job.id == job_id).first()

        if not resume or not job:
            raise ValueError("Resume or Job not found")

        semantic, skills, experience, final, explanation = compute_match(resume, job)

        match = db.query(MatchResult).filter(
            MatchResult.resume_id == resume_id,
            MatchResult.job_id == job_id
        ).first()

        if match:
            match.semantic_score = semantic
            match.skill_score = skills
            match.experience_score = experience
            match.final_score = final
            match.explanation = explanation
        else:
            match = MatchResult(
                resume_id=resume_id,
                job_id=job_id,
                semantic_score=semantic,
                skill_score=skills,
                experience_score=experience,
                final_score=final,
                explanation=explanation
            )
            db.add(match)

        db.commit()
        db.refresh(match)

        return match
    except Exception:
        db.rollback()
        logger.exception(
            DATABASE_ROLLBACK,
            extra={
                "resume_id": resume_id,
                "job_id": job_id
            }
        )

    finally:
        db.close()
# ----------------------------------------
# Resume → All Jobs (Celery safe)
# ----------------------------------------

def match_resume_against_all_jobs(resume_id: int):
    db = SessionLocal()
    logger.info(MATCH_STARTED,extra={"resume_id": resume_id})
    start_time = time.perf_counter()
    try:
        
        resume = db.query(Resume).filter(
            Resume.id == resume_id
        ).first()

        if not resume:
         logger.warning("RESUME_NOT_FOUND",extra={"resume_id": resume_id} )
        return
    
        jobs = db.query(Job).filter(
            Job.status == "open"
        ).all()
        # remove old results
        logger.info("OPEN_JOBS_FETCHED",extra={"resume_id": resume_id,"job_count": len(jobs)} )
        

        db.query(MatchResult).filter(
            MatchResult.resume_id == resume_id
        ).delete()

        db.commit()

        matches = []

        for job in jobs:
            semantic, skills, experience, final, explanation = compute_match(
                resume,
                job
            )

            matches.append(
                MatchResult(
                    resume_id=resume.id,
                    job_id=job.id,
                    semantic_score=semantic,
                    skill_score=skills,
                    experience_score=experience,
                    final_score=final,
                    explanation=explanation
                )
            )
            logger.info("MATCHES_PREPARED",extra={"resume_id": resume_id, "match_count": len(matches)})

        db.bulk_save_objects(matches)
        db.commit()
        duration_ms = round((time.perf_counter() - start_time) * 1000,2)
        logger.info(MATCH_COMPLETED,extra={ "resume_id": resume_id,"matches_created": len(matches),"duration_ms": duration_ms})
   
    except Exception:
        duration_ms = round((time.perf_counter() - start_time) * 1000,2)
        db.rollback()
        logger.exception(
            DATABASE_ROLLBACK,
            extra={
                "resume_id": resume_id,
                "duration_ms": duration_ms
            }        )
        
        logger.exception(
        MATCH_FAILED,
        extra={
            "resume_id": resume_id,
            "duration_ms": duration_ms
        }
    )
        raise


    
    finally:
     db.close()

# ----------------------------------------
# Job → All Resumes (Celery safe)
# ----------------------------------------
def match_job_against_all_resumes(job_id: int):
    db = SessionLocal()
    logger.info(MATCH_STARTED,extra={"job_id": job_id})
    start_time = time.perf_counter()
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            logger.warning("JOB_NOT_FOUND", extra={"job_id": job_id})
            return

        resumes = db.query(Resume).all()

        logger.info("RESUMES_FETCHED",extra={"job_id": job_id,"resume_count": len(resumes)})

        # remove old results
        db.query(MatchResult).filter(
            MatchResult.job_id == job_id
        ).delete()
        db.commit()

        matches = []

        for resume in resumes:
            semantic, skills, experience, final, explanation = compute_match(resume, job)

            matches.append(
                MatchResult(
                    resume_id=resume.id,
                    job_id=job.id,
                    semantic_score=semantic,
                    skill_score=skills,
                    experience_score=experience,
                    final_score=final,
                    explanation=explanation
                )
            )
        logger.info("MATCHES_PREPARED",extra={ "job_id": job_id,"match_count": len(matches) })  

        db.bulk_save_objects(matches)
        db.commit()
        duration_ms = round((time.perf_counter() - start_time) * 1000,2)
        logger.info(MATCH_COMPLETED,extra={"job_id": job_id,"matches_created": len(matches),"duration_ms": duration_ms})
    except Exception:
        duration_ms = round((time.perf_counter() - start_time) * 1000,2)
        db.rollback()
        logger.exception(
            DATABASE_ROLLBACK,
            extra={
                "job_id": job_id,
                "duration_ms": duration_ms
            }
        )
        logger.exception(
            MATCH_FAILED,
            extra={
                "job_id": job_id,
                "duration_ms": duration_ms
            }
        )
        raise

    finally:
        db.close()