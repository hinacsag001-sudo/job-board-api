import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.database import Base, engine
from app import models  # noqa: F401  (registers models on Base.metadata before create_all)

Base.metadata.create_all(bind=engine)

from app.database import engine, SessionLocal, Base
from sqlalchemy import Column, Integer, String, Text

# Ensure tables are created
Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def seed_initial_data():
    db = SessionLocal()
    try:
        # Check if jobs already exist
        from app.models import Job # Replace with your actual Job model import
        if db.query(Job).count() == 0:
            job1 = Job(
                title="Backend Python Developer",
                description="Build REST APIs using FastAPI and SQLite.",
                company="Tech Solutions Ltd",
                location="Remote",
                salary="$70,000 - $90,000"
            )
            job2 = Job(
                title="Frontend React Engineer",
                description="Develop responsive UI for enterprise applications.",
                company="DevStudio Inc",
                location="Hybrid",
                salary="$65,000 - $80,000"
            )
            db.add_all([job1, job2])
            db.commit()
    except Exception as e:
        print(f"Seeding error: {e}")
    finally:
        db.close()

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(
    title="Job Listings REST API",
    description="Production REST API for job postings, candidate applications, and platform analytics.",
    version="1.0.0"
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

from app.routers import auth, jobs, applications, analytics

app.include_router(auth.router)
app.include_router(jobs.router)
app.include_router(applications.router)
app.include_router(analytics.router)

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", include_in_schema=False)
def serve_home():
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return {"message": "Job Listings API is running", "docs": "/docs"}