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

@router.get("/", response_model=List[schemas.JobResponse])
def search_jobs(
    title: Optional[str] = None,
    location: Optional[str] = None,
    min_salary: Optional[float] = None,
    db: Session = Depends(database.get_db)
):
    query = db.query(models.Job)
    if title:
        query = query.filter(models.Job.title.ilike(f"%{title}%"))
    if location:
        query = query.filter(models.Job.location.ilike(f"%{location}%"))
    if min_salary:
        query = query.filter(models.Job.salary >= min_salary)
    return query.all()