from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, JSON
from sqlalchemy.sql import func
from app.core.database import Base


class MatchResult(Base):
    __tablename__ = "match_results"

    id = Column(Integer, primary_key=True, index=True)

    resume_id = Column(Integer, ForeignKey("resumes.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))

    semantic_score = Column(Float)
    skill_score = Column(Float)
    experience_score = Column(Float)
    final_score = Column(Float)

    explanation = Column(JSON)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())           
    def __repr__(self):
        return (f"<MatchResult id={self.id} resume_id={self.resume_id} "
                f"job_id={self.job_id} final_score={self.final_score}>")
    