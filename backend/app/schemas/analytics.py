from pydantic import BaseModel
from typing import List


class RankedCandidate(BaseModel):
    resume_id: int
    scores: dict


class JobAnalytics(BaseModel):
    total_candidates: int
    average_score: float
    top_score: float
    lowest_score: float
    pool_quality: str
