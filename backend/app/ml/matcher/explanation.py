
def interpret(score: float) -> str:
    if score >= 0.75:
        return "strong"
    if score >= 0.45:
        return "moderate"
    if score >= 0.2:
        return "weak"
    return "poor"


# ----------------------------------------------------
# Skill classification
# ----------------------------------------------------
# ----------------------------------------------------
# Skill classification (DETERMINISTIC)
# ----------------------------------------------------
def classify_skill_matches(resume_skills, job_skills):
    resume_set = set(resume_skills)
    job_set = set(job_skills)

    strong = list(resume_set & job_set)
    missing = list(job_set - resume_set)

    # simple heuristic for partial (optional)
    partial = []

    return strong, partial, missing

# ----------------------------------------------------
# Main explanation builder
# ----------------------------------------------------
def build_explanation(semantic, skills, experience,
                      resume_skills, job_skills,
                      candidate_exp, required_exp):

    strong, partial, missing = classify_skill_matches(resume_skills, job_skills)

    explanation = {
        "scores": {
            "semantic": semantic,
            "skills": skills,
            "experience": experience
        },
        "interpretation": {
            "semantic_fit": interpret(semantic),
            "skill_alignment": interpret(skills),
            "seniority_match": interpret(experience)
        },
        "details": {
            "strong_matches": strong,
            "partial_matches": partial,
            "missing_skills": missing,
            "candidate_experience_years": candidate_exp,
            "required_experience_years": required_exp
        },
        "weights": {
            "semantic": 0.6,
            "skills": 0.3,
            "experience": 0.1
        }
    }

    return explanation
