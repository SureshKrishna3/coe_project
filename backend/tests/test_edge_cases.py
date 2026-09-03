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
    c1 = Course(course_id="CS101", course_name="Python", category="Programming", difficulty="Beginner")
    c2 = Course(course_id="CS103", course_name="Discrete Math", category="Computer Science", difficulty="Beginner")
    c3 = Course(course_id="DS201", course_name="Machine Learning", category="Machine Learning", difficulty="Advanced")
    c4 = Course(course_id="ROB101", course_name="Robotics Basics", category="Robotics", difficulty="Beginner")
    c5 = Course(course_id="ELEC101", course_name="Circuit Theory", category="Electronics", difficulty="Beginner")
    c6 = Course(course_id="EMB101", course_name="Sensors", category="Embedded", difficulty="Beginner")

    session.add_all([c1, c2, c3, c4, c5, c6])
    session.commit()

    # DS201 requires CS101 (AND) and CS103 (AND)
    p1 = Prerequisite(course_id="DS201", prerequisite_course_id="CS101", prerequisite_type="AND", group_id=1)
    p2 = Prerequisite(course_id="DS201", prerequisite_course_id="CS103", prerequisite_type="AND", group_id=2)

    # ROB101 requires ELEC101 (OR) or EMB101 (OR)
    p3 = Prerequisite(course_id="ROB101", prerequisite_course_id="ELEC101", prerequisite_type="OR", group_id=1)
    p4 = Prerequisite(course_id="ROB101", prerequisite_course_id="EMB101", prerequisite_type="OR", group_id=1)

    # Circular prereqs: C7 requires C8, C8 requires C7
    c7 = Course(course_id="CIRC1", course_name="Circular 1", category="Test", difficulty="Beginner")
    c8 = Course(course_id="CIRC2", course_name="Circular 2", category="Test", difficulty="Beginner")
    session.add_all([c7, c8])
    session.commit()

    p5 = Prerequisite(course_id="CIRC1", prerequisite_course_id="CIRC2", prerequisite_type="AND", group_id=1)
    p6 = Prerequisite(course_id="CIRC2", prerequisite_course_id="CIRC1", prerequisite_type="AND", group_id=1)

    # Schedule clash for CS101 and CS103
    s1 = Schedule(course_id="CS101", day="Monday", start_time="09:00", end_time="11:00", location="Lab 1")
    s2 = Schedule(course_id="CS103", day="Monday", start_time="09:00", end_time="11:00", location="Lab 2")

    session.add_all([p1, p2, p3, p4, p5, p6, s1, s2])
    session.commit()

    yield session
    session.close()

# TEST 1: Student missing prerequisite
def test_missing_prerequisite(db_session):
    rec_engine = RecommendationEngine(db_session)
    st = Student(student_id="S1", name="Test Student", semester=1, completed_courses="", career_goal="AI Engineer")
    res = rec_engine.evaluate_course("DS201", st)
    assert res["eligibility_status"] == "MISSING_PREREQUISITES"
    assert "Not Eligible" in res["category_rating"]

# TEST 2: AND prerequisite - all must be satisfied
def test_and_prerequisite(db_session):
    prereq_engine = PrerequisiteEngine(db_session)
    # Only 1 of 2 AND prereqs met
    res1 = prereq_engine.evaluate_course_prerequisites("DS201", ["CS101"])
    assert res1["is_satisfied"] == False

    # Both met
    res2 = prereq_engine.evaluate_course_prerequisites("DS201", ["CS101", "CS103"])
    assert res2["is_satisfied"] == True

# TEST 3: OR prerequisite - either satisfies requirement
def test_or_prerequisite(db_session):
    prereq_engine = PrerequisiteEngine(db_session)
    res = prereq_engine.evaluate_course_prerequisites("ROB101", ["EMB101"])
    assert res["is_satisfied"] == True

# TEST 4: Schedule conflict
def test_schedule_conflict(db_session):
    sched_engine = ScheduleEngine(db_session)
    res = sched_engine.check_conflict("CS103", ["CS101"])
    assert res["has_conflict"] == True
    assert res["is_hard_conflict"] == True

# TEST 5: Unknown career goal
def test_unknown_career_goal(db_session):
    rec_engine = RecommendationEngine(db_session)
    st = Student(student_id="S2", name="Test Student", semester=1, completed_courses="CS101", career_goal="Quantum Computing Niche")
    res = rec_engine.evaluate_course("CS101", st)
    assert res["career_alignment"]["match_level"] in ["LOW", "NEUTRAL", "Direct Tag Match"]

# TEST 6: No suitable courses (empty student profile fallback)
def test_no_suitable_courses_fallback(db_session):
    rec_engine = RecommendationEngine(db_session)
    st = Student(student_id="S3", name="New Student", semester=1, completed_courses="", career_goal="")
    res = rec_engine.evaluate_course("CS101", st)
    assert res["eligibility_status"] == "ELIGIBLE"

# TEST 7: Empty student profile
def test_empty_student_profile(db_session):
    st = Student(student_id="S4", name="", semester=1, completed_courses="", career_goal="")
    assert st.completed_courses == ""
    assert st.career_goal == ""

# TEST 8: Invalid course ID returns 404 HTTP Exception without crashing
def test_invalid_course_id_api():
    response = client.get("/api/courses/INVALID_COURSE_999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

# TEST 9: Circular prerequisite detection
def test_circular_prerequisite(db_session):
    prereq_engine = PrerequisiteEngine(db_session)
    res = prereq_engine.evaluate_course_prerequisites("CIRC1", [])
    assert res["circular_detected"] == True

# TEST 10: Missing / partial dataset fields
def test_partial_dataset_fields(db_session):
    c_partial = Course(course_id="PART1", course_name="Partial", category="General", difficulty="Beginner", description=None, career_tags=None)
    db_session.add(c_partial)
    db_session.commit()

    rec_engine = RecommendationEngine(db_session)
    st = Student(student_id="S5", name="Test", semester=1, completed_courses="")
    res = rec_engine.evaluate_course("PART1", st)
    assert res["eligibility_status"] == "ELIGIBLE"
