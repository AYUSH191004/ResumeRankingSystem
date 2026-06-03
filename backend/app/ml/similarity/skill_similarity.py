import numpy as np
from app.utils.similarity import cosine_similarity

def skill_match(resume_skill_vecs: list, job_skill_vecs: list) -> float:
    """
    For each job skill vector, find best matching resume skill vector.
    Pure mathematical — no ML calls.
    """

    if not job_skill_vecs:
        return 1.0
    if not resume_skill_vecs:
        return 0.0

    scores = []

    for job_vec in job_skill_vecs:
        best = 0.0

        for r_vec in resume_skill_vecs:
            sim = cosine_similarity(job_vec, r_vec)
            if sim > best:
                best = sim

        scores.append(best)

    return float(np.mean(scores))
