from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models, schemas, database

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/", response_model=schemas.AnalyticsResponse)
def get_analytics(db: Session = Depends(database.get_db)):
    total_jobs = db.query(models.Job).count()
    total_apps = db.query(models.Application).count()

    locations = db.query(models.Job.location, func.count(models.Job.id).label("count")) \
        .group_by(models.Job.location) \
        .order_by(func.count(models.Job.id).desc()) \
        .limit(5).all()

    top_locs = [{"location": loc, "count": count} for loc, count in locations]
    return {"total_jobs": total_jobs, "total_applications": total_apps, "top_locations": top_locs}