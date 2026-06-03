from fastapi import FastAPI

from app.api.routes import resume, jobs, match, analytics

app = FastAPI(
    title="Resume Matcher API",
    version="1.0.0"
)

# register routers
app.include_router(resume.router)
app.include_router(jobs.router)
app.include_router(match.router)
app.include_router(analytics.router)
