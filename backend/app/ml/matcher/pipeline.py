from app.ml.similarity.text_similarity import semantic_match
from app.ml.embeddings.Embedding_generator import generate_embedding
from app.ml.similarity.skill_similarity import skill_match
from app.utils.similarity import cosine_similarity
from app.api.routes import resume

from .safety import clamp, safe_text
from .normalization import (
    normalize_resume_skills,
    normalize_job_skills,
    normalize_experience
)
from .scoring import compute_experience_score, fuse_scores
from .explanation import build_explanation



def run_matching(resume, job):
    """
    Main ATS decision engine
    This function must NEVER crash.
    """

    # ---------- Safe Input ----------
    parsed = resume.parsed_data or {}

    resume_text = safe_text(resume.text)
    job_text = safe_text(job.description)

    # ---------- Normalize ----------
    resume_skills = normalize_resume_skills(parsed)
    job_skills = normalize_job_skills(job.required_skills)

    candidate_exp = normalize_experience(parsed)
    required_exp = job.min_experience or 0

    # ---------- Similarity Signals ----------
    semantic_raw = semantic_match( resume.embedding_vector,job.embedding_vector)
# ---------- Skill (deterministic fallback) ----------
    resume_vecs = parsed.get("skill_embeddings", [])
    job_vecs = job.embedding_vector or []

    if resume_vecs and job_vecs:
        skill_raw = skill_match(resume_vecs, job_vecs)
    else:
        # fallback
        resume_set = set(resume_skills)
        job_set = set(job_skills)

        if not job_set:
            skill_raw = 1.0
        else:
            skill_raw = len(resume_set & job_set) / len(job_set)

    # ---------- Lazy Embedding Backfill ----------
    if not resume.embedding_vector and resume.text:
     resume.embedding_vector = generate_embedding(resume.text)

    if not job.embedding_vector:
     job.embedding_vector = generate_embedding(job.description)

    # ---------- Stabilize ----------
    semantic = clamp(semantic_raw)
    skills = clamp(skill_raw)

    # ---------- Policy Scoring ----------
    experience = compute_experience_score(candidate_exp, required_exp)

    # ---------- Final Decision ----------
    final_score = fuse_scores(semantic, skills, experience, resume_skills, job_skills)


    # ---------- Explanation ----------
    explanation = build_explanation(
        semantic, skills, experience,
        resume_skills, job_skills,
        candidate_exp, required_exp
    )
    return semantic, skills, experience, final_score, explanation


    
