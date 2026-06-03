from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)

    required_skills = Column(Text, nullable=False, default="")
    min_experience = Column(Integer, nullable=False, default=0)

    recruiter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recruiter = relationship("User", backref="jobs")

    status = Column(String(20), nullable=False, default="open")

    # ⭐ NEW — persistent semantic embedding
    embedding_vector = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
