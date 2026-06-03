from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    file_path = Column(String, nullable=False)

    text = Column(Text, nullable=True)

    # structured parsed data
    parsed_data = Column(JSON, nullable=True)

    # ⭐ NEW — persistent semantic embedding
    embedding_vector = Column(JSON, nullable=True)

    user = relationship("User", backref="resumes")
