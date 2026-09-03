from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.domain import Course, Student, CourseOutcome
from app.engines.prerequisite_engine import PrerequisiteEngine
from app.engines.schedule_engine import ScheduleEngine
from app.engines.career_engine import CareerEngine
from app.engines.explanation_engine import ExplanationEngine

class RecommendationEngine:
    def __init__(self, db: Session):
        self.db = db
        self.prereq_engine = PrerequisiteEngine(db)
        self.schedule_engine = ScheduleEngine(db)
        self.career_engine = CareerEngine(db)
        self.explanation_engine = ExplanationEngine(db)

    def evaluate_course(
        self,
        course_id: str,
        student: Student,
        other_selected_courses: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Evaluates a single course for a student using rule-based explainable weights:
          - Career Goal Alignment: max 50 pts (dominant factor for career suitability)
          - Prerequisite Readiness: max 20 pts (20 if satisfied, 0 if missing mandatory prereq)
          - Learning Outcome / Skill Overlap: max 15 pts (overlap ratio between student skills & course outcomes)
          - Career Pathway Depth Value: max 10 pts
          - Schedule Feasibility: max 5 pts (Hard conflict = 0, Soft warning = 2.5, Perfect fit = 5)
        Total max = 100 pts.
        """
        course = self.db.query(Course).filter(Course.course_id == course_id).first()
        if not course:
            raise ValueError(f"Course {course_id} not found.")

        completed_courses = [c.strip() for c in (student.completed_courses or "").split(";") if c.strip()]
        selected_courses = (other_selected_courses or []) + completed_courses
        student_skills = set(s.strip().lower() for s in (student.skills or "").split(";") if s.strip())

        # 1. Prerequisite Engine evaluation
        prereq_eval = self.prereq_engine.evaluate_course_prerequisites(course_id, completed_courses)

        # 2. Schedule Engine evaluation (Hard conflict vs Soft warning)
        schedule_eval = self.schedule_engine.check_conflict(
            course_id,
            selected_courses,
            student_availability=student.availability
        )

        # 3. Career Engine evaluation
        career_eval = self.career_engine.evaluate_career_alignment(course_id, student.career_goal)

        # 4. Learning Outcome / Skill Overlap calculation
        outcomes = self.db.query(CourseOutcome).filter(CourseOutcome.course_id == course_id).all()
        course_outcome_skills = set()
        for o in outcomes:
            if o.skill_tags:
                for st in o.skill_tags.split(";"):
                    course_outcome_skills.add(st.strip().lower())

        matching_skills = list(student_skills & course_outcome_skills) if student_skills else []
        
        if course_outcome_skills:
            overlap_ratio = len(matching_skills) / len(course_outcome_skills)
        else:
            overlap_ratio = 0.5 if student_skills else 0.0

        # Outcome score (max 15 pts)
        score_outcome = round(min(overlap_ratio * 15.0 + (len(matching_skills) * 2.0), 15.0), 1)

        # 5. Weighted Score Calculation
        # Career Alignment: max 50 pts
        score_career = (career_eval["alignment_score"] / 100.0) * 50.0

        # Prerequisites Readiness: max 20 pts
        score_prereq = 20.0 if prereq_eval["is_satisfied"] else 0.0

        # Pathway Value: max 10 pts
        score_pathway = 10.0 if career_eval["is_required"] else (7.0 if career_eval["is_recommended"] else 3.0)

        # Schedule Feasibility: max 5 pts
        if schedule_eval["is_hard_conflict"]:
            score_schedule = 0.0
        elif schedule_eval["is_soft_warning"]:
            score_schedule = 2.5
        else:
            score_schedule = 5.0

        total_score = round(score_career + score_prereq + score_outcome + score_pathway + score_schedule, 1)

        # 6. Determine Eligibility & Status Override
        if not prereq_eval["is_satisfied"]:
            eligibility_status = "MISSING_PREREQUISITES"
        elif schedule_eval["is_hard_conflict"]:
            eligibility_status = "SCHEDULE_CONFLICT"
        elif course_id in completed_courses:
            eligibility_status = "ALREADY_COMPLETED"
        else:
            eligibility_status = "ELIGIBLE"

        # Categorize
        if eligibility_status == "ALREADY_COMPLETED":
            category_rating = "Completed"
        elif eligibility_status == "MISSING_PREREQUISITES":
            category_rating = "Not Eligible (Prerequisites Missing)"
        elif eligibility_status == "SCHEDULE_CONFLICT":
            category_rating = "Conditional (Schedule Conflict)"
        elif schedule_eval["is_soft_warning"] and total_score >= 60:
            category_rating = "Recommended (Schedule Soft Warning)"
        elif total_score >= 80:
            category_rating = "Highly Recommended"
        elif total_score >= 60:
            category_rating = "Recommended"
        elif total_score >= 40:
            category_rating = "Consider"
        elif total_score >= 20:
            category_rating = "Low Priority"
        else:
            category_rating = "Not Recommended"

        # 7. Generate Alternative Catch-up Pathway if ineligible
        alt_pathway = []
        if not prereq_eval["is_satisfied"]:
            alt_pathway = self.prereq_engine.get_alternative_prerequisite_pathway(course_id, completed_courses)

        # 8. Explanation Engine
        explanation = self.explanation_engine.generate_explanation(
            course=course,
            student=student,
            prereq_eval=prereq_eval,
            schedule_eval=schedule_eval,
            career_eval=career_eval,
            matching_skills=matching_skills,
            total_score=total_score,
            category_rating=category_rating,
            eligibility_status=eligibility_status,
            alt_pathway=alt_pathway
        )

        return {
            "course_id": course.course_id,
            "course_name": course.course_name,
            "category": course.category,
            "difficulty": course.difficulty,
            "credits": course.credits,
            "duration": course.duration,
            "score": total_score,
            "category_rating": category_rating,
            "eligibility_status": eligibility_status,
            "prerequisite_status": prereq_eval,
            "schedule_status": schedule_eval,
            "career_alignment": career_eval,
            "matching_skills": matching_skills,
            "explanation": explanation,
            "alternative_pathway": alt_pathway
        }

    def recommend_electives(
        self,
        student_id: Optional[str] = None,
        student: Optional[Student] = None
    ) -> List[Dict[str, Any]]:
        target_student = student
        if target_student is None:
            if not student_id:
                raise ValueError("Either student_id or student object must be provided.")
            target_student = self.db.query(Student).filter(Student.student_id == student_id).first()
            if not target_student:
                raise ValueError(f"Student {student_id} not found.")

        all_courses = self.db.query(Course).all()
        results = []

        for course in all_courses:
            res = self.evaluate_course(course.course_id, target_student)
            results.append(res)

        def sort_key(item):
            status_priority = {
                "ELIGIBLE": 1,
                "SCHEDULE_CONFLICT": 2,
                "MISSING_PREREQUISITES": 3,
                "ALREADY_COMPLETED": 4
            }
            return (status_priority.get(item["eligibility_status"], 5), -item["score"])

        results.sort(key=sort_key)
        return results
