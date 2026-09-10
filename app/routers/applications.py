from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, auth, database

router = APIRouter(prefix="/applications", tags=["Applications"])


@router.post("/", response_model=schemas.ApplicationResponse)
def apply_job(app: schemas.ApplicationCreate, db: Session = Depends(database.get_db),
              current_user: models.User = Depends(auth.get_current_user)):
    job = db.query(models.Job).filter(models.Job.id == app.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    existing = db.query(models.Application).filter(
        models.Application.job_id == app.job_id,
        models.Application.candidate_id == current_user.id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already applied to this job")

    new_app = models.Application(job_id=app.job_id, candidate_id=current_user.id)
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    return new_app