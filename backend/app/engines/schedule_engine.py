from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.domain import Schedule

class ScheduleEngine:
    def __init__(self, db: Session):
        self.db = db

    def _parse_time(self, time_str: str) -> int:
        """Converts HH:MM format into total minutes from midnight."""
        parts = time_str.strip().split(":")
        return int(parts[0]) * 60 + int(parts[1])

    def times_overlap(self, start1: str, end1: str, start2: str, end2: str) -> bool:
        """Checks if two time ranges overlap [start1, end1) and [start2, end2)."""
        s1 = self._parse_time(start1)
        e1 = self._parse_time(end1)
        s2 = self._parse_time(start2)
        e2 = self._parse_time(end2)
        return max(s1, s2) < min(e1, e2)

    def get_course_schedules(self, course_id: str) -> List[Dict[str, Any]]:
        schedules = self.db.query(Schedule).filter(Schedule.course_id == course_id).all()
        return [
            {
                "day": s.day,
                "start_time": s.start_time,
                "end_time": s.end_time,
                "location": s.location
            }
            for s in schedules
        ]

    def check_conflict(
        self,
        course_id: str,
        other_course_ids: List[str],
        student_availability: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Checks for:
        1. Hard Conflict: Course timetable session overlaps with another selected course session.
        2. Soft Warning: Course session falls outside student's preferred availability window (e.g. Morning vs Afternoon).
        """
        target_schedules = self.get_course_schedules(course_id)
        if not target_schedules:
            return {
                "has_conflict": False,
                "is_hard_conflict": False,
                "is_soft_warning": False,
                "conflicts": [],
                "warnings": [],
                "summary": "No schedule specified for this course."
            }

        hard_conflicts = []
        for other_id in other_course_ids:
            if other_id == course_id:
                continue
            other_schedules = self.get_course_schedules(other_id)
            for ts in target_schedules:
                for os in other_schedules:
                    if ts["day"].lower() == os["day"].lower():
                        if self.times_overlap(ts["start_time"], ts["end_time"], os["start_time"], os["end_time"]):
                            hard_conflicts.append({
                                "target_course": course_id,
                                "conflicting_course": other_id,
                                "day": ts["day"],
                                "target_time": f"{ts['start_time']}-{ts['end_time']}",
                                "conflicting_time": f"{os['start_time']}-{os['end_time']}",
                                "location": ts["location"]
                            })

        # Check soft availability preference mismatch
        soft_warnings = []
        if student_availability:
            pref = student_availability.lower()
            for ts in target_schedules:
                start_hour = int(ts["start_time"].split(":")[0])
                if "morning" in pref and start_hour >= 12:
                    soft_warnings.append(f"Course session ({ts['day']} {ts['start_time']}) is in the afternoon, but your preferred availability is Morning.")
                elif "afternoon" in pref and start_hour < 12:
                    soft_warnings.append(f"Course session ({ts['day']} {ts['start_time']}) is in the morning, but your preferred availability is Afternoon.")

        has_hard_conflict = len(hard_conflicts) > 0
        has_soft_warning = len(soft_warnings) > 0

        if has_hard_conflict:
            summary = f"HARD CONFLICT DETECTED on {hard_conflicts[0]['day']} ({hard_conflicts[0]['target_time']}) with {hard_conflicts[0]['conflicting_course']}."
        elif has_soft_warning:
            summary = f"Soft Warning: {soft_warnings[0]}"
        else:
            summary = "No timetable conflicts detected."

        return {
            "has_conflict": has_hard_conflict,
            "is_hard_conflict": has_hard_conflict,
            "is_soft_warning": has_soft_warning,
            "conflicts": hard_conflicts,
            "warnings": soft_warnings,
            "summary": summary
        }
