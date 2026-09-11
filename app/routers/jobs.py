from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas, auth, database

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.post("/", response_model=schemas.JobResponse)
def create_job(job: schemas.JobCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    if current_user.role != "employer":
        raise HTTPException(status_code=403, detail="Only employers can post jobs")
    new_job = models.Job(**job.dict(), employer_id=current_user.id)
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

@router.get("/")
def get_jobs():
    return [
        {
            "id": 1,
            "title": "Backend Python Developer",
            "description": "Build REST APIs using FastAPI and SQLite.",
            "company": "Tech Solutions Ltd",
            "location": "Remote",
            "salary": "$70,000 - $90,000"
        },
        {
            "id": 2,
            "title": "Frontend React Engineer",
            "description": "Develop responsive UI for enterprise applications.",
            "company": "DevStudio Inc",
            "location": "Hybrid",
            "salary": "$65,000 - $80,000"
        }
    ]