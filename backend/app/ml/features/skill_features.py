from app.ml.embeddings.Embedding_generator import generate_embedding


def build_skill_embeddings(skills: list[str]) -> list[list[float]]:
    """
    Generate embeddings for list of skills.
    Runs ONLY during ingestion.
    """
    if not skills:
        return []

    return [generate_embedding(skill.lower()) for skill in skills]