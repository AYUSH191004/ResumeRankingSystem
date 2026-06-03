from pydantic import BaseModel, field_validator, Field
from typing import List
from datetime import datetime


class JobCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=20)
    required_skills: List[str] = []
    min_experience: int = Field(ge=0, le=50)

    @field_validator("required_skills")
    @classmethod
    def clean_skills(cls, v):
        cleaned = []
        for skill in v:
            s = skill.strip().lower()
            if s and s not in cleaned:
                cleaned.append(s)
        return cleaned


class JobResponse(BaseModel):
    id: int
    title: str
    description: str
    required_skills: List[str]
    min_experience: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
