from pydantic import BaseModel
from typing import Dict


class MatchBreakdown(BaseModel):
    semantic: float
    skills: float
    experience: float


class MatchResponse(BaseModel):
    resume_id: int
    job_id: int
    final_score: float
    breakdown: MatchBreakdown
    explanation: Dict
    class Config:
       from_attributes = True
class ResumeMatchResponse(BaseModel):
    resume_id: int
    job_id: int
    semantic_score: float
    skill_score: float
    experience_score: float
    final_score: float
    explanation: Dict

    class Config:from_attributes = True