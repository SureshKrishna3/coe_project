from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models.domain import Course, Student, CareerPathway, CourseOutcome
from app.engines.prerequisite_engine import PrerequisiteEngine
from app.engines.schedule_engine import ScheduleEngine

class IndependentGroundTruth:
    """
    Independent ground-truth evaluation logic.
    Determines course suitability objectively WITHOUT using the recommendation engine's scoring function.
    """
    def __init__(self, db: Session):
        self.db = db
        self.prereq_engine = PrerequisiteEngine(db)
        self.schedule_engine = ScheduleEngine(db)

    def is_course_suitable(self, course_id: str, student: Student) -> Dict[str, Any]:
        course = self.db.query(Course).filter(Course.course_id == course_id).first()
        if not course:
            return {"is_suitable": False, "reason": "Course not found"}

        completed_courses = [c.strip() for c in (student.completed_courses or "").split(";") if c.strip()]
        if course_id in completed_courses:
            return {"is_suitable": False, "reason": "Already completed"}

        # 1. Prerequisite Compliance Check
        prereq_eval = self.prereq_engine.evaluate_course_prerequisites(course_id, completed_courses)
        if not prereq_eval["is_satisfied"]:
            return {"is_suitable": False, "reason": "Missing prerequisites", "details": prereq_eval}

        # 2. Hard Schedule Conflict Check
        schedule_eval = self.schedule_engine.check_conflict(course_id, completed_courses)
        if schedule_eval["has_conflict"]:
            return {"is_suitable": False, "reason": "Hard schedule conflict", "details": schedule_eval}

        # 3. Career & Skill Relevance Check
        career_goal = (student.career_goal or "").strip().lower()
        is_relevant = False

        if career_goal:
            pathway = self.db.query(CareerPathway).filter(CareerPathway.career_name.ilike(career_goal)).first()
            if pathway:
                reqs = [c.strip() for c in (pathway.required_courses or "").split(";")]
                recs = [c.strip() for c in (pathway.recommended_courses or "").split(";")]
                if course_id in reqs or course_id in recs:
                    is_relevant = True

            if not is_relevant and course.career_tags and career_goal in course.career_tags.lower():
                is_relevant = True

        # Skill overlap fallback
        if not is_relevant:
            student_skills = set(s.strip().lower() for s in (student.skills or "").split(";") if s.strip())
            outcomes = self.db.query(CourseOutcome).filter(CourseOutcome.course_id == course_id).all()
            course_skills = set()
            for o in outcomes:
                if o.skill_tags:
                    for st in o.skill_tags.split(";"):
                        course_skills.add(st.strip().lower())
            
            if student_skills and (student_skills & course_skills):
                is_relevant = True

        if not is_relevant and course.category.lower() in career_goal:
            is_relevant = True

        if not is_relevant:
            return {"is_suitable": False, "reason": "Unrelated to career goal or skills"}

        return {
            "is_suitable": True,
            "reason": "Ground truth suitable: Prereqs satisfied, schedule feasible, and career/skill aligned.",
            "prereq_satisfied": True,
            "schedule_feasible": True,
            "career_aligned": True
        }
