from typing import List, Dict, Any
from sqlalchemy.orm import Session
from evaluation.ground_truth import IndependentGroundTruth

class EvaluationMetrics:
    @staticmethod
    def evaluate_recommendations_against_ground_truth(
        recommendations: List[Dict[str, Any]],
        student: Any,
        ground_truth: IndependentGroundTruth,
        k: int = 5
    ) -> Dict[str, Any]:
        """
        Evaluates top-K recommendations objectively against independent ground truth engines.
        Calculates:
          - Precision@K (Course Choice Quality %): Percentage of top-K recommendations that are ground-truth suitable
          - Prerequisite Conflict Count (#): Number of top-K recommendations with missing prerequisites
          - Schedule Conflict Count (#): Number of top-K recommendations with hard timetable clashes
          - Career Pathway Alignment Score (%): Objective career alignment score across top-K recommendations
        """
        if not recommendations:
            return {
                "precision_at_k": 0.0,
                "prereq_conflict_count": 0,
                "prereq_conflict_rate": 0.0,
                "sched_conflict_count": 0,
                "sched_conflict_rate": 0.0,
                "career_alignment": 0.0
            }

        top_k = recommendations[:k]
        suitable_count = 0
        prereq_conflicts = 0
        sched_conflicts = 0
        career_scores = []

        completed_courses = [c.strip() for c in (student.completed_courses or "").split(";") if c.strip()]

        for r in top_k:
            c_id = r["course_id"]
            gt_res = ground_truth.is_course_suitable(c_id, student)
            
            if gt_res["is_suitable"]:
                suitable_count += 1
            
            # Check objective prerequisite satisfaction using PrerequisiteEngine
            prereq_eval = ground_truth.prereq_engine.evaluate_course_prerequisites(c_id, completed_courses)
            if not prereq_eval["is_satisfied"]:
                prereq_conflicts += 1

            # Check objective schedule conflict using ScheduleEngine
            sched_eval = ground_truth.schedule_engine.check_conflict(c_id, completed_courses, student_availability=student.availability)
            if sched_eval["has_conflict"] or sched_eval["is_hard_conflict"]:
                sched_conflicts += 1

            # Calculate objective career alignment using CareerEngine
            career_eval = ground_truth.schedule_engine.db.query if False else ground_truth.schedule_engine
            # Use ground_truth's CareerEngine if available, or query directly
            from app.engines.career_engine import CareerEngine
            c_engine = CareerEngine(ground_truth.db)
            c_eval = c_engine.evaluate_career_alignment(c_id, student.career_goal)
            career_scores.append(c_eval["alignment_score"])

        precision = round((suitable_count / len(top_k)) * 100.0, 2)
        prereq_rate = round((prereq_conflicts / len(top_k)) * 100.0, 2)
        sched_rate = round((sched_conflicts / len(top_k)) * 100.0, 2)
        avg_career = round(sum(career_scores) / len(career_scores), 2) if career_scores else 0.0

        return {
            "precision_at_k": precision,
            "prereq_conflict_count": prereq_conflicts,
            "prereq_conflict_rate": prereq_rate,
            "sched_conflict_count": sched_conflicts,
            "sched_conflict_rate": sched_rate,
            "career_alignment": avg_career
        }
