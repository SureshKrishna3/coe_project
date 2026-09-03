from typing import List, Dict, Any
from app.models.domain import Course, Student

class ExplanationEngine:
    def __init__(self, db=None):
        self.db = db

    def generate_explanation(
        self,
        course: Course,
        student: Student,
        prereq_eval: Dict[str, Any],
        schedule_eval: Dict[str, Any],
        career_eval: Dict[str, Any],
        matching_skills: List[str],
        total_score: float,
        category_rating: str,
        eligibility_status: str,
        alt_pathway: List[str]
    ) -> Dict[str, Any]:
        """
        Generates clear, human-readable non-technical explanations for students and faculty.
        """
        reasons_pro = []
        reasons_con = []
        suggested_action = ""

        goal = student.career_goal or "General Technical Proficiency"

        # 1. Career & Skill Reasoning (Phase 6 & 10)
        if career_eval["is_required"]:
            reasons_pro.append(f"Essential mandatory course for your career goal of becoming a {goal}.")
        elif career_eval["is_recommended"]:
            reasons_pro.append(f"Highly aligned elective for your career goal of becoming a {goal}.")
        
        if matching_skills:
            skills_str = ", ".join(matching_skills[:3])
            reasons_pro.append(f"Develops key skills ({skills_str}) matching your current skill profile and goal.")
        elif not career_eval["is_required"] and not career_eval["is_recommended"]:
            reasons_con.append(f"Limited direct alignment with your career goal of {goal}.")

        # 2. Prerequisite Reasoning
        if prereq_eval["is_satisfied"]:
            if prereq_eval["satisfied_direct"]:
                reasons_pro.append(f"You have completed all prerequisite courses ({', '.join(prereq_eval['satisfied_direct'])}).")
            else:
                reasons_pro.append("No prerequisite courses required for enrollment.")
        else:
            reasons_con.append(f"Not ready yet: Missing mandatory prerequisite course(s): {', '.join(prereq_eval['missing_direct'])}.")

        # 3. Schedule & Availability Reasoning (Phase 8: Hard Conflict vs Soft Warning)
        if schedule_eval["is_hard_conflict"]:
            reasons_con.append(f"Hard timetable conflict: {schedule_eval['summary']}.")
        elif schedule_eval["is_soft_warning"]:
            reasons_con.append(f"Schedule warning: {schedule_eval['warnings'][0]}")
        else:
            reasons_pro.append("No timetable conflicts with your current schedule.")

        # 4. Actionable Next Steps (Phase 10)
        if eligibility_status == "ELIGIBLE":
            if total_score >= 80:
                suggested_action = f"Recommended choice. Supports your {goal} goal, builds relevant technical skills, and unlocks advanced pathway units."
            elif total_score >= 60:
                suggested_action = "Good elective option to consider for broadening your technical skill set."
            else:
                suggested_action = "Optional elective. Review learning outcomes to confirm personal interest."
        elif eligibility_status == "MISSING_PREREQUISITES":
            if alt_pathway and len(alt_pathway) > 1:
                first_step = alt_pathway[0]
                suggested_action = f"Enroll in prerequisite '{first_step}' first, then progress to '{course.course_name}'."
            else:
                suggested_action = f"Complete missing prerequisites ({', '.join(prereq_eval['missing_direct'])}) before enrolling."
        elif eligibility_status == "SCHEDULE_CONFLICT":
            suggested_action = "Consider selecting an alternate time slot or swapping conflicting course sessions."
        elif eligibility_status == "ALREADY_COMPLETED":
            suggested_action = "You have already completed this course in a previous semester."

        overall_summary = (
            f"Overall Score: {total_score}/100. "
            f"Status: {category_rating}. "
            f"{'Strong choice for your current career pathway.' if eligibility_status == 'ELIGIBLE' and total_score >= 70 else ''}"
        )

        return {
            "overall_summary": overall_summary,
            "reasons_pro": reasons_pro,
            "reasons_con": reasons_con,
            "suggested_action": suggested_action,
            "career_match_level": career_eval["match_level"],
            "prerequisite_satisfied": prereq_eval["is_satisfied"],
            "schedule_feasible": not schedule_eval["is_hard_conflict"]
        }
