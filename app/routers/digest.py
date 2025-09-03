from fastapi import APIRouter, BackgroundTasks, Depends
from app.services.digest import generate_weekly_digest
from app.dependencies import db_dep
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/digest",
    tags=["Digest"]
)


@router.get("/generate")
def generate_digest(
    background_tasks: BackgroundTasks,
    db: Session = Depends(db_dep)
):
    """
    Weekly digest JSON fayl yaratish uchun background task.
    """
    background_tasks.add_task(generate_weekly_digest, db)
    return {"message": "Weekly digest generation started"}
