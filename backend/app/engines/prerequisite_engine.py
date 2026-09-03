import networkx as nx
from typing import List, Dict, Set, Any, Tuple
from sqlalchemy.orm import Session
from app.models.domain import Prerequisite, Course

class PrerequisiteEngine:
    def __init__(self, db: Session):
        self.db = db
        self.prereq_graph = nx.DiGraph()
        self._build_graph()

    def _build_graph(self):
        """Build a directed graph of course dependencies: prereq -> course."""
        prereqs = self.db.query(Prerequisite).all()
        for p in prereqs:
            self.prereq_graph.add_edge(p.prerequisite_course_id, p.course_id, type=p.prerequisite_type, group=p.group_id)

    def evaluate_course_prerequisites(self, course_id: str, completed_courses: List[str]) -> Dict[str, Any]:
        """
        Evaluates whether a student with completed_courses satisfies the prerequisites of course_id.
        Supports AND/OR logic grouped by group_id.
        Returns:
            - is_satisfied: bool
            - missing_direct: List[str]
            - satisfied_direct: List[str]
            - full_prereq_chain: List[str]
            - missing_chain: List[str]
            - circular_detected: bool
        """
        completed_set = set(completed_courses)

        # 1. Fetch direct prerequisites from DB
        direct_prereqs = self.db.query(Prerequisite).filter(Prerequisite.course_id == course_id).all()
        if not direct_prereqs:
            return {
                "is_satisfied": True,
                "missing_direct": [],
                "satisfied_direct": [],
                "full_prereq_chain": [],
                "missing_chain": [],
                "circular_detected": False,
                "summary": "No prerequisites required for this course."
            }

        # 2. Check circular dependencies
        circular = False
        try:
            cycles = list(nx.simple_cycles(self.prereq_graph))
            if any(course_id in cycle for cycle in cycles):
                circular = True
        except Exception:
            pass

        # 3. Group by group_id and prerequisite_type
        # If group has AND: all prereqs in group must be completed
        # If group has OR: at least one prereq in group must be completed
        groups: Dict[int, Dict[str, Any]] = {}
        for p in direct_prereqs:
            gid = p.group_id
            if gid not in groups:
                groups[gid] = {
                    "type": p.prerequisite_type,
                    "courses": []
                }
            groups[gid]["courses"].append(p.prerequisite_course_id)

        satisfied_direct = []
        missing_direct = []
        is_satisfied = True

        for gid, gdata in groups.items():
            gtype = gdata["type"]
            gcourses = gdata["courses"]
            
            if gtype == "OR":
                # At least one course must be in completed_set
                satisfied_in_group = [c for c in gcourses if c in completed_set]
                if satisfied_in_group:
                    satisfied_direct.extend(satisfied_in_group)
                else:
                    is_satisfied = False
                    # Mention missing option
                    missing_direct.append(f"({' OR '.join(gcourses)})")
            else:  # AND
                for c in gcourses:
                    if c in completed_set:
                        satisfied_direct.append(c)
                    else:
                        is_satisfied = False
                        missing_direct.append(c)

        # 4. Get full prerequisite chain (ancestors)
        full_chain = self.get_full_dependency_chain(course_id)
        missing_chain = [c for c in full_chain if c not in completed_set]

        summary = "All prerequisites satisfied." if is_satisfied else f"Missing prerequisites: {', '.join(missing_direct)}"

        return {
            "is_satisfied": is_satisfied,
            "missing_direct": missing_direct,
            "satisfied_direct": list(set(satisfied_direct)),
            "full_prereq_chain": full_chain,
            "missing_chain": missing_chain,
            "circular_detected": circular,
            "summary": summary
        }

    def get_full_dependency_chain(self, course_id: str) -> List[str]:
        """Returns ordered list of all upstream prerequisite courses recursively."""
        if course_id not in self.prereq_graph:
            return []
        try:
            ancestors = nx.ancestors(self.prereq_graph, course_id)
            return list(ancestors)
        except Exception:
            return []

    def get_alternative_prerequisite_pathway(self, course_id: str, completed_courses: List[str]) -> List[str]:
        """
        Generates a recommended step-by-step sequence of courses for a student to take
        to unlock target course_id.
        """
        eval_res = self.evaluate_course_prerequisites(course_id, completed_courses)
        if eval_res["is_satisfied"]:
            return [course_id]

        missing = eval_res["missing_chain"]
        # Order missing courses by dependency depth
        def get_depth(c):
            try:
                return len(nx.ancestors(self.prereq_graph, c))
            except Exception:
                return 0

        sorted_missing = sorted(missing, key=get_depth)
        return sorted_missing + [course_id]
