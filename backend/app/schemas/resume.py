from pydantic import BaseModel
from typing import Optional, Dict


class ResumeUploadResponse(BaseModel):
    resume_id: int
    parse_status: str
    skills_found: int
    contact: Optional[Dict]
    experience_years: Optional[int]
    text_snippet: Optional[str]
    class Config:
       from_attributes = True

class ResumeParseRequest(BaseModel):
    resume_id: int
class ResumeParseResponse(BaseModel):
    resume_id: int
    parse_status: str
    skills_found: int
    contact: Optional[Dict]
    experience_years: Optional[int]
    text_snippet: Optional[str]

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

class ResumeMatchRequest(BaseModel):
    resume_id: int
    job_id: int
    class Config:
       from_attributes = True

class ResumeResponse(BaseModel):
    resume_id: int
    parse_status: str
    skills_found: int
    contact: Optional[Dict]
    experience_years: Optional[int]
    text_snippet: Optional[str]

    class Config:
     from_attributes = True

                 
