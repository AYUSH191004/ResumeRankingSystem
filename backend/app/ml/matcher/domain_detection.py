DOMAIN_KEYWORDS = {
    "backend": ["api", "fastapi", "django", "flask", "sql", "database"],
    "frontend": ["react", "html", "css", "javascript"],
    "data": ["pandas", "numpy", "sklearn", "machine learning", "analysis"],
    "devops": ["docker", "kubernetes", "ci/cd", "aws"],
    "qa": ["testing", "selenium", "automation test"]
}


def detect_domain(skills):
    text = " ".join(skills).lower()

    scores = {}
    for domain, words in DOMAIN_KEYWORDS.items():
        scores[domain] = sum(w in text for w in words)

    return max(scores, key=scores.get) if max(scores.values()) > 0 else "unknown"
