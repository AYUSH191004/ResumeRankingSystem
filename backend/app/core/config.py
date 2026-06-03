from pydantic_settings import BaseSettings ,SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # App
    PROJECT_NAME: str = "Resume Matcher API"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # Paths
    UPLOAD_DIR: str = "data/uploads"
    PROCESSED_DIR: str = "data/processed"
    
    # Database (we'll use SQLite for now, PostgreSQL later)
    DATABASE_URL: str = "sqlite:///./resume_matcher.db"
    REDIS_URL :str = "redis://localhost:6380/0"
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024  # 5MB
    ALLOWED_EXTENSIONS: set = {".pdf", ".docx"}
    
    model_config = SettingsConfigDict(
        env_file = ".env",
        case_sensitive = True)

settings = Settings()
