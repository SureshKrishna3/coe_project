from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.domain import CareerPathway
from app.schemas.api_schemas import CareerPathwaySchema
from app.engines.career_engine import CareerEngine

router = APIRouter(prefix="/api/careers", tags=["Careers"])

@router.get("", response_model=List[CareerPathwaySchema])
def get_careers(db: Session = Depends(get_db)):
    careers = db.query(CareerPathway).all()
    return careers

@router.get("/{career_id}", response_model=CareerPathwaySchema)
def get_career_detail(career_id: str, db: Session = Depends(get_db)):
    career = db.query(CareerPathway).filter(
        (CareerPathway.career_id == career_id) | (CareerPathway.career_name.ilike(career_id))
    ).first()
    if not career:
        raise HTTPException(status_code=404, detail=f"Career {career_id} not found.")
    return career
