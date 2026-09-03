from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.domain import StakeholderFeedback
from app.schemas.api_schemas import StakeholderFeedbackCreate

router = APIRouter(prefix="/api/stakeholder", tags=["Stakeholder Validation"])

@router.post("/feedback")
def submit_feedback(data: StakeholderFeedbackCreate, db: Session = Depends(get_db)):
    fb = StakeholderFeedback(**data.dict())
    db.add(fb)
    db.commit()
    db.refresh(fb)
    return {"status": "success", "id": fb.id, "message": "Thank you for your feedback!"}

@router.get("/stats")
def get_feedback_stats(db: Session = Depends(get_db)):
    all_fb = db.query(StakeholderFeedback).all()
    total = len(all_fb)
    if total == 0:
        return {
            "total_responses": 0,
            "understandable_pct": 0.0,
            "useful_prereqs_pct": 0.0,
            "useful_pathway_pct": 0.0,
            "easy_to_use_pct": 0.0,
            "would_use_pct": 0.0,
            "recent_comments": []
        }

    understandable = sum(1 for f in all_fb if f.understandable_recommendations)
    useful_p = sum(1 for f in all_fb if f.useful_prerequisites)
    useful_pw = sum(1 for f in all_fb if f.useful_pathway)
    easy = sum(1 for f in all_fb if f.easy_to_use)
    would_use = sum(1 for f in all_fb if f.would_use_system)

    comments = [f.comments for f in all_fb if f.comments]

    return {
        "total_responses": total,
        "understandable_pct": round((understandable / total) * 100, 1),
        "useful_prereqs_pct": round((useful_p / total) * 100, 1),
        "useful_pathway_pct": round((useful_pw / total) * 100, 1),
        "easy_to_use_pct": round((easy / total) * 100, 1),
        "would_use_pct": round((would_use / total) * 100, 1),
        "recent_comments": comments[-5:]
    }
