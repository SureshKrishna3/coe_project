from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.domain import Student
from app.schemas.api_schemas import StudentDetail, StudentCreate
from app.engines.prerequisite_engine import PrerequisiteEngine
from app.engines.schedule_engine import ScheduleEngine

router = APIRouter(prefix="/api/students", tags=["Students"])

@router.get("", response_model=List[StudentDetail])
def get_students(db: Session = Depends(get_db), limit: int = Query(250, le=500)):
    students = db.query(Student).limit(limit).all()
    return students

@router.get("/{student_id}", response_model=StudentDetail)
def get_student(student_id: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail=f"Student {student_id} not found.")
    return student

@router.post("", response_model=StudentDetail)
def create_or_update_student(student_data: StudentCreate, db: Session = Depends(get_db)):
    existing = db.query(Student).filter(Student.student_id == student_data.student_id).first()
    if existing:
        existing.name = student_data.name
        existing.semester = student_data.semester
        existing.completed_courses = student_data.completed_courses
        existing.skills = student_data.skills
        existing.career_goal = student_data.career_goal
        existing.preferred_schedule = student_data.preferred_schedule
        existing.availability = student_data.availability
        db.commit()
        db.refresh(existing)
        return existing
    else:
        new_student = Student(**student_data.dict())
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        return new_student

@router.get("/{student_id}/prerequisites")
def get_student_prerequisites_summary(student_id: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")
    
    completed = [c.strip() for c in (student.completed_courses or "").split(";") if c.strip()]
    engine = PrerequisiteEngine(db)
    return {
        "student_id": student.student_id,
        "completed_courses": completed,
        "completed_count": len(completed)
    }

@router.get("/{student_id}/conflicts")
def get_student_schedule_conflicts(student_id: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")

    completed = [c.strip() for c in (student.completed_courses or "").split(";") if c.strip()]
    engine = ScheduleEngine(db)
    
    conflicts = []
    for c in completed:
        res = engine.check_conflict(c, completed)
        if res["has_conflict"]:
            conflicts.append(res)

    return {
        "student_id": student.student_id,
        "has_conflicts": len(conflicts) > 0,
        "conflict_details": conflicts
    }
