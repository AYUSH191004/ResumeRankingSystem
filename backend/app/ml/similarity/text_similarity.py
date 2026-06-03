from app.utils import similarity

# =====================================================
# Semantic Text Match (PRODUCTION SAFE)
# =====================================================

def semantic_match(resume_embedding, job_embedding) -> float:
    """
    Compute similarity using precomputed embeddings.
    NO model calls here.
    """

    if not resume_embedding or not job_embedding:
        return 0.0

    return similarity.cosine_similarity(resume_embedding, job_embedding)