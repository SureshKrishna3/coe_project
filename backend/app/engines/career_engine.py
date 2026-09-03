from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.domain import CareerPathway, Course, CourseOutcome, Prerequisite

class CareerEngine:
    def __init__(self, db: Session):
        self.db = db

    def _get_career_prerequisite_courses(self, target_courses: List[str]) -> set:
        """
        Finds all direct and indirect prerequisite courses needed to unlock target_courses.
        """
        prereq_set = set()
        queue = list(target_courses)
        visited = set()

        while queue:
            curr = queue.pop(0)
            if curr in visited:
                continue
            visited.add(curr)
            
            prereqs = self.db.query(Prerequisite).filter(Prerequisite.course_id == curr).all()
            for p in prereqs:
                p_id = p.prerequisite_course_id
                prereq_set.add(p_id)
                if p_id not in visited:
                    queue.append(p_id)

        return prereq_set

    def evaluate_career_alignment(self, course_id: str, career_name: str) -> Dict[str, Any]:
        """
        Evaluates how strongly course_id supports target career_name.
        Considers:
          - Mandatory Required Core Courses (95 pts)
          - Career Prerequisite Stepping Stone Units (90 pts)
          - Recommended Career Electives (85 pts)
          - Direct Career Tag / Category Matches (80 pts)
          - Skill-Supporting Electives (60-85 pts)
          - Unrelated Domain Units (15 pts)
        """
        if not career_name:
            return {
                "alignment_score": 50.0,
                "match_level": "NEUTRAL",
                "is_required": False,
                "is_recommended": False,
                "matching_skills": [],
                "pathway_step": "N/A",
                "summary": "No career goal specified."
            }

        course = self.db.query(Course).filter(Course.course_id == course_id).first()
        pathway = self.db.query(CareerPathway).filter(CareerPathway.career_name.ilike(career_name)).first()

        req_courses = [c.strip() for c in (pathway.required_courses or "").split(";") if c.strip()] if pathway else []
        rec_courses = [c.strip() for c in (pathway.recommended_courses or "").split(";") if c.strip()] if pathway else []
        pathway_skills = set(s.strip().lower() for s in (pathway.skills or "").split(";") if s.strip()) if pathway else set()

        is_req = course_id in req_courses
        is_rec = course_id in rec_courses

        # Check if course is a prerequisite stepping stone for required/recommended career units
        target_career_units = req_courses + rec_courses
        career_prereq_units = self._get_career_prerequisite_courses(target_career_units) if target_career_units else set()
        is_prereq_stepping_stone = (course_id in career_prereq_units) and not is_req and not is_rec

        # Skill matching
        outcomes = self.db.query(CourseOutcome).filter(CourseOutcome.course_id == course_id).all()
        course_skills = set()
        for o in outcomes:
            if o.skill_tags:
                for st in o.skill_tags.split(";"):
                    course_skills.add(st.strip().lower())

        matching_skills = [s for s in course_skills if s in pathway_skills]

        # Tag & category matching
        has_tag_match = False
        if course and course.career_tags and career_name.lower() in course.career_tags.lower():
            has_tag_match = True
        elif course and course.category and course.category.lower() in career_name.lower():
            has_tag_match = True

        # Calculate alignment score
        if is_req:
            score = 95.0
            level = "VERY HIGH"
            step = "Mandatory Career Core"
        elif is_prereq_stepping_stone:
            score = 90.0
            level = "HIGH"
            step = "Career Prerequisite Stepping Stone"
        elif is_rec:
            score = 85.0
            level = "HIGH"
            step = "Recommended Career Elective"
        elif has_tag_match:
            score = 80.0
            level = "HIGH"
            step = "Direct Career Tag Match"
        elif matching_skills:
            score = 60.0 + min(len(matching_skills) * 10, 25.0)
            level = "MEDIUM"
            step = "Skill-Supporting Elective"
        else:
            score = 15.0
            level = "LOW"
            step = "Unrelated Domain"

        summary = (
            f"Required course for {career_name}." if is_req else
            f"Essential prerequisite stepping stone for {career_name}." if is_prereq_stepping_stone else
            f"Recommended elective for {career_name}." if is_rec else
            f"Tag/category match for {career_name}." if has_tag_match else
            f"Develops {len(matching_skills)} relevant skills for {career_name}."
        )

        return {
            "alignment_score": score,
            "match_level": level,
            "is_required": is_req,
            "is_recommended": is_rec or is_prereq_stepping_stone or has_tag_match,
            "matching_skills": matching_skills,
            "pathway_step": step,
            "summary": summary
        }

    def get_career_pathway_details(self, career_name: str) -> Optional[Dict[str, Any]]:
        pathway = self.db.query(CareerPathway).filter(CareerPathway.career_name.ilike(career_name)).first()
        if not pathway:
            return None
        return {
            "career_id": pathway.career_id,
            "career_name": pathway.career_name,
            "description": pathway.description,
            "required_courses": [c.strip() for c in (pathway.required_courses or "").split(";") if c.strip()],
            "recommended_courses": [c.strip() for c in (pathway.recommended_courses or "").split(";") if c.strip()],
            "skills": [s.strip() for s in (pathway.skills or "").split(";") if s.strip()],
            "pathway_sequence": pathway.pathway_sequence
        }
