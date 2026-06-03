from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.log_events import *
from app.core.logging import logger
from app.ml.embeddings.Embedding_generator import get_model

# routers
from app.api.routes import resume as resume_routes
from app.api.routes import jobs as jobs_routes
from app.api.routes import match as match_routes
from app.api.routes import analytics as analytics_routes
from app.api.routes import health as health_routes

# models (only for table creation)
from app.core.database import Base, engine
from app.models import job, resume, user, match

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🔥 startup
    logger.info("APPLICATION STARTUP", extra={"event": "app_startup"})
    logger.info("MODEL_LOADING_STARTED")
    get_model()   # warm up sentence-transformer
    logger.info("MODEL_LOADING_COMPLETED")
    logger.info("DATABASE_INIT_STARTED")
    Base.metadata.create_all(bind=engine)
    logger.info("DATABASE_INIT_COMPLETED")
    logger.info("APPLICATION STARTUP COMPLETED", extra={"event": "app_startup_completed"})  
    yield
    logger.info("APPLICATION SHUTDOWN", extra={"event": "app_shutdown"})





app = FastAPI(
    title="Resume Matcher API",
    version="1.0.0",
    lifespan=lifespan
)

# include routers
app.include_router(resume_routes.router)
app.include_router(jobs_routes.router)
app.include_router(match_routes.router)
app.include_router(analytics_routes.router)
app.include_router(health_routes.router)

