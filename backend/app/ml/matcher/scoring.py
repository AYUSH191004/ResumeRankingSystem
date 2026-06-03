from app.ml.matcher import domain_detection


def compute_experience_score(candidate_exp: int, required_exp: int) -> float:
    """
    Continuous scoring instead of binary rejection.

    Behaviour:
    underqualified → proportional penalty
    matched → strong score
    overqualified → slight bonus but capped
    """

    if required_exp <= 0:
        return 1.0

    ratio = candidate_exp / required_exp
    ratio = min(ratio, 1.2)  # allow small bonus
    return round(ratio / 1.2, 3)

DOMAIN_KEYWORDS = {
    "backend": ["api", "fastapi", "django", "flask", "sql", "database"],
    "frontend": ["react", "html", "css", "javascript"],
    "data": ["pandas", "numpy", "sklearn", "machine learning", "analysis"],
    "devops": ["docker", "kubernetes", "ci/cd", "aws"],
    "qa": ["testing", "selenium", "automation test"]
}

def fuse_scores(semantic: float, skills: float, experience: float,
                resume_skills=None, job_skills=None) -> float:

    base = (
        0.6 * semantic +
        0.3 * skills +
        0.1 * experience
    )

    # -------- Experience penalty --------
    if experience < 0.2:
        base *= 0.75

    # -------- Domain alignment --------
    if resume_skills and job_skills:
        r_domain = domain_detection.detect_domain(resume_skills)
        j_domain = domain_detection.detect_domain(job_skills)

        if r_domain != j_domain and "unknown" not in (r_domain, j_domain):
            base *= 0.7

    # -------- strong candidate boost --------
    if skills > 0.7 and semantic > 0.7:
        base *= 1.05

    return round(min(base, 1.0), 4)

