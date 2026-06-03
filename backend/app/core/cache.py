from functools import lru_cache

@lru_cache(maxsize=10000)
def cached_skill_embeddings(skill_tuple):
    return skill_tuple