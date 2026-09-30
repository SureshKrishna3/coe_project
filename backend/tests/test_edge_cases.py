import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.database import Base
from app.models.domain import Course, Student, Prerequisite, CareerPathway, Schedule
from app.engines.prerequisite_engine import PrerequisiteEngine
from app.engines.schedule_engine import ScheduleEngine
from app.engines.recommendation_engine import RecommendationEngine
from app.main import app

client = TestClient(app)

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Seed edge case test data
    c1 = Course(course_id="CS101", course_name="Python", category="Programming", difficulty="Beginner", career_tags="AI, Software")
    c2 = Course(course_id="CS103", course_name="Discrete Math", category="Computer Science", difficulty="Beginner", career_tags="AI")
    c3 = Course(course_id="DS201", course_name="Machine Learning", category="Machine Learning", difficulty="Advanced", career_tags="AI")
    c4 = Course(course_id="ROB101", course_name="Robotics Basics", category="Robotics", difficulty="Beginner", career_tags="Robotics")
    c5 = Course(course_id="ELEC101", course_name="Circuit Theory", category="Electronics", difficulty="Beginner", career_tags="Robotics")
    c6 = Course(course_id="EMB101", course_name="Sensors", category="Embedded", difficulty="Beginner", career_tags="Robotics")

    # Multi-level chain: Level1 -> Level2 -> Level3
    c_lvl1 = Course(course_id="CHAIN1", course_name="Level 1 Intro", category="Chain", difficulty="Beginner")
    c_lvl2 = Course(course_id="CHAIN2", course_name="Level 2 Inter", category="Chain", difficulty="Intermediate")
    c_lvl3 = Course(course_id="CHAIN3", course_name="Level 3 Adv", category="Chain", difficulty="Advanced")

    session.add_all([c1, c2, c3, c4, c5, c6, c_lvl1, c_lvl2, c_lvl3])
    session.commit()

    # DS201 requires CS101 (AND) and CS103 (AND)
    p1 = Prerequisite(course_id="DS201", prerequisite_course_id="CS101", prerequisite_type="AND", group_id=1)
    p2 = Prerequisite(course_id="DS201", prerequisite_course_id="CS103", prerequisite_type="AND", group_id=2)

    # ROB101 requires ELEC101 (OR) or EMB101 (OR)
    p3 = Prerequisite(course_id="ROB101", prerequisite_course_id="ELEC101", prerequisite_type="OR", group_id=1)
    p4 = Prerequisite(course_id="ROB101", prerequisite_course_id="EMB101", prerequisite_type="OR", group_id=1)

    # Multi-level chain: CHAIN2 requires CHAIN1, CHAIN3 requires CHAIN2
    p_c1 = Prerequisite(course_id="CHAIN2", prerequisite_course_id="CHAIN1", prerequisite_type="AND", group_id=1)
    p_c2 = Prerequisite(course_id="CHAIN3", prerequisite_course_id="CHAIN2", prerequisite_type="AND", group_id=1)

    # Circular prereqs: CIRC1 requires CIRC2, CIRC2 requires CIRC1
    c7 = Course(course_id="CIRC1", course_name="Circular 1", category="Test", difficulty="Beginner")
    c8 = Course(course_id="CIRC2", course_name="Circular 2", category="Test", difficulty="Beginner")
    session.add_all([c7, c8])
    session.commit()

    p5 = Prerequisite(course_id="CIRC1", prerequisite_course_id="CIRC2", prerequisite_type="AND", group_id=1)
    p6 = Prerequisite(course_id="CIRC2", prerequisite_course_id="CIRC1", prerequisite_type="AND", group_id=1)

    # Full Schedule clash for CS101 and CS103
    s1 = Schedule(course_id="CS101", day="Monday", start_time="09:00", end_time="11:00", location="Lab 1")
    s2 = Schedule(course_id="CS103", day="Monday", start_time="09:00", end_time="11:00", location="Lab 2")

    # Partial Schedule overlap: OVERLAP1 (10:00-12:00) vs OVERLAP2 (11:30-13:30)
    c_ov1 = Course(course_id="OVL1", course_name="Overlap 1", category="Test", difficulty="Beginner")
    c_ov2 = Course(course_id="OVL2", course_name="Overlap 2", category="Test", difficulty="Beginner")
    session.add_all([c_ov1, c_ov2])
    session.commit()

    s_ov1 = Schedule(course_id="OVL1", day="Wednesday", start_time="10:00", end_time="12:00", location="Room A")
    s_ov2 = Schedule(course_id="OVL2", day="Wednesday", start_time="11:30", end_time="13:30", location="Room B")

    session.add_all([p1, p2, p3, p4, p_c1, p_c2, p5, p6, s1, s2, s_ov1, s_ov2])
    session.commit()

    yield session
    session.close()

# REQUIREMENT 5A: Missing prerequisite handling & catch-up sequence
def test_missing_prerequisite(db_session):
    rec_engine = RecommendationEngine(db_session)
    st = Student(student_id="S1", name="Test Student", semester=1, completed_courses="", career_goal="AI Engineer")
    res = rec_engine.evaluate_course("DS201", st)
    assert res["eligibility_status"] == "MISSING_PREREQUISITES"
    assert "Not Eligible" in res["category_rating"]

# REQUIREMENT 5B: Multi-level prerequisite chain (A -> B -> C)
def test_multilevel_prerequisite_chain(db_session):
    prereq_engine = PrerequisiteEngine(db_session)
    # Student completed nothing. CHAIN3 requires CHAIN2 which requires CHAIN1.
    res = prereq_engine.evaluate_course_prerequisites("CHAIN3", [])
    assert res["is_satisfied"] == False
    assert "CHAIN2" in res["missing_direct"] or "CHAIN2" in res["missing_chain"]
    assert "CHAIN1" in res["missing_chain"]

    # Student completed CHAIN1, but not CHAIN2
    res_part = prereq_engine.evaluate_course_prerequisites("CHAIN3", ["CHAIN1"])
    assert res_part["is_satisfied"] == False

    # Student completed both CHAIN1 and CHAIN2
    res_full = prereq_engine.evaluate_course_prerequisites("CHAIN3", ["CHAIN1", "CHAIN2"])
    assert res_full["is_satisfied"] == True

# REQUIREMENT 5C: Circular prerequisites (Cycle detection, no infinite loop)
def test_circular_prerequisite(db_session):
    prereq_engine = PrerequisiteEngine(db_session)
    res = prereq_engine.evaluate_course_prerequisites("CIRC1", [])
    assert res["circular_detected"] == True

# REQUIREMENT 5D: Hard schedule conflict
def test_schedule_conflict(db_session):
    sched_engine = ScheduleEngine(db_session)
    res = sched_engine.check_conflict("CS103", ["CS101"])
    assert res["has_conflict"] == True
    assert res["is_hard_conflict"] == True

# REQUIREMENT 5E: Partial schedule overlap detection
def test_partial_schedule_overlap(db_session):
    sched_engine = ScheduleEngine(db_session)
    res = sched_engine.check_conflict("OVL2", ["OVL1"])
    assert res["has_conflict"] == True

# REQUIREMENT 5F: Unknown career goal fallback
def test_unknown_career_goal(db_session):
    rec_engine = RecommendationEngine(db_session)
    st = Student(student_id="S2", name="Test Student", semester=1, completed_courses="CS101", career_goal="Quantum Computing Niche")
    res = rec_engine.evaluate_course("CS101", st)
    assert res["career_alignment"]["match_level"] in ["LOW", "NEUTRAL", "Direct Tag Match"]

# REQUIREMENT 5G: Empty student profile safe loading
def test_empty_student_profile(db_session):
    st = Student(student_id="S4", name="", semester=1, completed_courses="", career_goal="")
    assert st.completed_courses == ""
    assert st.career_goal == ""
    rec_engine = RecommendationEngine(db_session)
    res = rec_engine.evaluate_course("CS101", st)
    assert res["eligibility_status"] == "ELIGIBLE"

# REQUIREMENT 5H: Invalid course ID returns 404 HTTP Exception
def test_invalid_course_id_api():
    response = client.get("/api/courses/INVALID_COURSE_999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

# REQUIREMENT 5I: Duplicate course entry prevention in recommendations
def test_duplicate_course_recommendations(db_session):
    rec_engine = RecommendationEngine(db_session)
    st = Student(student_id="S_DUP", name="Duplicate Test", semester=1, completed_courses="", career_goal="AI Engineer")
    recs = rec_engine.recommend_electives(student=st)
    rec_ids = [r["course_id"] for r in recs]
    assert len(rec_ids) == len(set(rec_ids))

# REQUIREMENT 5J: Partial / Missing dataset fields safe handling
def test_partial_dataset_fields(db_session):
    c_partial = Course(course_id="PART1", course_name="Partial", category="General", difficulty="Beginner", description=None, career_tags=None)
    db_session.add(c_partial)
    db_session.commit()

    rec_engine = RecommendationEngine(db_session)
    st = Student(student_id="S5", name="Test", semester=1, completed_courses="")
    res = rec_engine.evaluate_course("PART1", st)
    assert res["eligibility_status"] == "ELIGIBLE"
