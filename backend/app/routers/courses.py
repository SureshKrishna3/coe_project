from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.domain import Course, Prerequisite, CourseOutcome, Schedule
from app.schemas.api_schemas import CourseDetail, CourseCreate

router = APIRouter(prefix="/api/courses", tags=["Courses"])

@router.get("", response_model=List[CourseDetail])
def get_courses(
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Course)
    if category:
        query = query.filter(Course.category.ilike(f"%{category}%"))
    if difficulty:
        query = query.filter(Course.difficulty.ilike(f"%{difficulty}%"))
    if search:
        query = query.filter(
            (Course.course_name.ilike(f"%{search}%")) |
            (Course.course_id.ilike(f"%{search}%")) |
            (Course.description.ilike(f"%{search}%"))
        )
    return query.all()

@router.get("/{course_id}", response_model=CourseDetail)
def get_course_detail(course_id: str, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.course_id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail=f"Course {course_id} not found.")
    return course

@router.post("", response_model=CourseDetail)
def create_course(course_data: CourseCreate, db: Session = Depends(get_db)):
    existing = db.query(Course).filter(Course.course_id == course_data.course_id).first()
    if existing:
        for k, v in course_data.dict().items():
            setattr(existing, k, v)
        db.commit()
        db.refresh(existing)
        return existing
    else:
        new_course = Course(**course_data.dict())
        db.add(new_course)
        db.commit()
        db.refresh(new_course)
        return new_course
