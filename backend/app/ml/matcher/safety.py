def clamp(score) -> float:
    """
    Guarantees score remains in [0,1]
    Prevents model noise from corrupting ranking.
    """
    if score is None:
        return 0.0

    try:
        score = float(score)
    except Exception:
        return 0.0

    if score < 0:
        return 0.0
    if score > 1:
        return 1.0
    return score


def safe_text(text):
    """Ensure embedding model never receives None"""
    if not text:
        return ""
    return str(text)
