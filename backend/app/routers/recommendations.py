from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.domain import Student
from app.schemas.api_schemas import RecommendationRequest, RecommendationResult
from app.engines.recommendation_engine import RecommendationEngine

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])

@router.get("/{student_id}", response_model=List[RecommendationResult])
def get_recommendations_for_student(student_id: str, db: Session = Depends(get_db)):
    rec_engine = RecommendationEngine(db)
    try:
        results = rec_engine.recommend_electives(student_id)
        return results
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation evaluation error: {str(e)}")

@router.post("", response_model=List[RecommendationResult])
def post_recommendations(req: RecommendationRequest, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == req.student_id).first()
    if not student:
        # Create temporary transient student object for evaluation
        student = Student(
            student_id=req.student_id,
            name="Guest Student",
            semester=1,
            completed_courses=";".join(req.completed_courses or []),
            skills="",
            career_goal=req.career_goal or "Software Engineer",
            preferred_schedule=req.schedule_preference or ""
        )
    else:
        if req.career_goal:
            student.career_goal = req.career_goal
        if req.completed_courses is not None:
            student.completed_courses = ";".join(req.completed_courses)

    rec_engine = RecommendationEngine(db)
    all_courses = db.query(Student).all()  # dummy fetch to ensure DB active
    
    courses = rec_engine.recommend_electives(student=student)
    return courses
