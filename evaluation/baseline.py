from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.domain import Course, Student

class BaselineSystem:
    """
    Simple naive baseline system.
    Recommends courses based ONLY on matching: Career Goal -> Course Career Tags.
    Does NOT consider prerequisites, schedule conflicts, outcome overlaps, or multi-step pathway dependencies.
    """
    def __init__(self, db: Session):
        self.db = db

    def recommend(self, student: Student) -> List[Dict[str, Any]]:
        all_courses = self.db.query(Course).all()
        goal = (student.career_goal or "").lower()
        results = []

        for c in all_courses:
            tags = (c.career_tags or "").lower()
            if goal and goal in tags:
                score = 85.0
                category = "Recommended"
            elif goal and c.category.lower() in goal:
                score = 65.0
                category = "Consider"
            else:
                score = 30.0
                category = "Low Priority"

            # Naive baseline marks everything as ELIGIBLE regardless of prerequisites or schedule!
            results.append({
                "course_id": c.course_id,
                "course_name": c.course_name,
                "category": c.category,
                "score": score,
                "category_rating": category,
                "eligibility_status": "ELIGIBLE",  # Naive assumption
                "prerequisite_status": {"is_satisfied": True, "missing_direct": []},    # Naive assumption
                "schedule_status": {"has_conflict": False, "is_hard_conflict": False},  # Naive assumption
                "career_alignment_score": score
            })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results
