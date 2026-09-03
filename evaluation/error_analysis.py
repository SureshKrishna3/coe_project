from typing import List, Dict, Any

class ErrorAnalysisModule:
    @staticmethod
    def analyze_experiment_errors(evaluation_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Categorizes failures and calculates failure rates across evaluation runs.
        """
        total = len(evaluation_records)
        if total == 0:
            return {
                "total_cases": 0,
                "successful_cases": 0,
                "failed_cases": 0,
                "failure_rate_pct": 0.0,
                "categories": []
            }

        category_counts = {
            "Missing Prerequisite Data": 0,
            "Schedule Conflict": 0,
            "Unknown / Unregistered Career": 0,
            "Weak Career Mapping": 0,
            "Missing Student Skills": 0,
            "Empty Profile Input": 0,
            "Multi-level Dependency Delay": 0
        }

        failed_count = 0

        for r in evaluation_records:
            st_type = r.get("scenario_type", "")
            if "missing" in st_type:
                category_counts["Missing Prerequisite Data"] += 1
                failed_count += 1
            elif "conflict" in st_type:
                category_counts["Schedule Conflict"] += 1
                failed_count += 1
            elif "unknown" in st_type:
                category_counts["Unknown / Unregistered Career"] += 1
                failed_count += 1
            elif "weak" in st_type:
                category_counts["Weak Career Mapping"] += 1
            elif "empty" in st_type:
                category_counts["Empty Profile Input"] += 1
                failed_count += 1

        successful_cases = total - failed_count

        taxonomy = [
            {
                "error": "Missing Prerequisites",
                "count": category_counts["Missing Prerequisite Data"],
                "cause": "Student has not completed required foundational units.",
                "system_behavior": "Prerequisite Engine overrides eligibility to `MISSING_PREREQUISITES`.",
                "recovery_strategy": "Displays step-by-step catch-up pathway sequence."
            },
            {
                "error": "Schedule Conflict",
                "count": category_counts["Schedule Conflict"],
                "cause": "Selected elective clashes with existing course session.",
                "system_behavior": "Schedule Engine flags hard clash and penalizes score.",
                "recovery_strategy": "Displays timetable warning badge and suggests non-overlapping session."
            },
            {
                "error": "Unknown Career Goal",
                "count": category_counts["Unknown / Unregistered Career"],
                "cause": "Student selects a niche career not in database registry.",
                "system_behavior": "Engine falls back to keyword matching across course tags.",
                "recovery_strategy": "Suggests closest standard career pathways."
            },
            {
                "error": "Empty Profile Input",
                "count": category_counts["Empty Profile Input"],
                "cause": "Profile created without completed courses or skills.",
                "system_behavior": "System prompts user to complete academic history.",
                "recovery_strategy": "Shows introductory foundational electives."
            }
        ]

        return {
            "total_cases": total,
            "successful_cases": successful_cases,
            "failed_cases": failed_count,
            "failure_rate_pct": round((failed_count / total) * 100.0, 1),
            "categories": taxonomy
        }
