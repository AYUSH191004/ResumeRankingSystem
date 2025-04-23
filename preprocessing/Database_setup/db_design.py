from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Text, Enum, Date, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from sqlalchemy.schema import CreateTable

Base = declarative_base()

# Candidates-Table
class Candidate(Base):
    __tablename__ = 'candidates'
    candidate_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    email = Column(String(255), unique=True)
    phone = Column(String(20))
    linkedin = Column(String(255))
    github = Column(String(255))
    total_experience = Column(Float)
    highest_qualification = Column(String(255))
    university = Column(String(255))
    location = Column(String(255))
    resume_text = Column(Text)

    skills = relationship("Skill", back_populates="candidate", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="candidate", cascade="all, delete-orphan")
    experiences = relationship("WorkExperience", back_populates="candidate", cascade="all, delete-orphan")
    certifications = relationship("Certification", back_populates="candidate", cascade="all, delete-orphan")
    rankings = relationship("Ranking", back_populates="candidate", cascade="all, delete-orphan")

# Skills-Table
class Skill(Base):
    __tablename__ = 'skills'
    skill_id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(Integer, ForeignKey('candidates.candidate_id'))
    skill_name = Column(String(255))
    proficiency_level = Column(Enum('Beginner', 'Intermediate', 'Advanced', 'Expert'))

    candidate = relationship("Candidate", back_populates="skills")

# Projects-Table
class Project(Base):
    __tablename__ = 'projects'
    project_id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(Integer, ForeignKey('candidates.candidate_id'))
    project_title = Column(String(255))
    project_description = Column(Text)
    technologies_used = Column(Text)
    project_url = Column(String(255), nullable=True)

    candidate = relationship("Candidate", back_populates="projects")

# Work-Experience-Table
class WorkExperience(Base):
    __tablename__ = 'work_experience'
    work_id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(Integer, ForeignKey('candidates.candidate_id'))
    company_name = Column(String(255))
    job_title = Column(String(255))
    start_date = Column(Date)
    end_date = Column(Date, nullable=True)
    description = Column(Text)

    candidate = relationship("Candidate", back_populates="experiences")

# Certifications-Table
class Certification(Base):
    __tablename__ = 'certifications'
    cert_id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(Integer, ForeignKey('candidates.candidate_id'))
    certification_name = Column(String(255))
    issuing_organization = Column(String(255))
    issue_date = Column(Date)
    expiration_date = Column(Date, nullable=True)
    credential_url = Column(String(255), nullable=True)

    candidate = relationship("Candidate", back_populates="certifications")

# Rankings-Table
class Ranking(Base):
    __tablename__ = 'rankings'
    ranking_id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(Integer, ForeignKey('candidates.candidate_id'))
    skill_score = Column(Float)
    experience_score = Column(Float)
    project_score = Column(Float)
    certification_score = Column(Float)
    overall_score = Column(Float)

    candidate = relationship("Candidate", back_populates="rankings")

# Analysis-Results-Table
class AnalysisResults(Base):
    __tablename__ = 'analysis_results'
    id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(Integer, ForeignKey('candidates.candidate_id'))
    analysis_date = Column(DateTime, default=datetime.utcnow)
    insights = Column(Text)

    candidate = relationship("Candidate", back_populates="analysis_results")

def generate_schema():
    # Create engine (use any database URL, even in-memory SQLite)
    engine = create_engine("mysql+pymysql://root:123456@localhost:3306/resume_db")
    
    # Generate create table statements
    schema = []
    for table in [Candidate, Skill, Project, WorkExperience, Certification, Ranking, AnalysisResults]:
        create_table = CreateTable(table.__table__)
        schema.append(str(create_table).replace("CREATE TABLE", "CREATE TABLE IF NOT EXISTS").strip() + ';\n')
    
    # Write to schema.sql
    with open('Database_setup/schema.sql', 'w') as f:
        f.write('\n'.join(schema))

if __name__ == '__main__':
    generate_schema()
