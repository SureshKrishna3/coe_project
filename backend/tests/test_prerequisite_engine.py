import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.domain import Course, Prerequisite
from app.engines.prerequisite_engine import PrerequisiteEngine

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Seed test data
    c1 = Course(course_id="CS101", course_name="Python", category="Programming", difficulty="Beginner")
    c2 = Course(course_id="CS103", course_name="Discrete Math", category="Computer Science", difficulty="Beginner")
    c3 = Course(course_id="CS202", course_name="Data Structures", category="Programming", difficulty="Intermediate")
    c4 = Course(course_id="DS101", course_name="Data Analytics", category="Data", difficulty="Beginner")
    c5 = Course(course_id="DS102", course_name="Excel SQL", category="Data", difficulty="Beginner")

    session.add_all([c1, c2, c3, c4, c5])
    session.commit()

    # CS202 requires CS101 (AND) and CS103 (AND)
    p1 = Prerequisite(course_id="CS202", prerequisite_course_id="CS101", prerequisite_type="AND", group_id=1)
    p2 = Prerequisite(course_id="CS202", prerequisite_course_id="CS103", prerequisite_type="AND", group_id=2)

    # DS101 requires CS101 (OR) or DS102 (OR)
    p3 = Prerequisite(course_id="DS101", prerequisite_course_id="CS101", prerequisite_type="OR", group_id=1)
    p4 = Prerequisite(course_id="DS101", prerequisite_course_id="DS102", prerequisite_type="OR", group_id=1)

    session.add_all([p1, p2, p3, p4])
    session.commit()

    yield session
    session.close()

def test_prerequisite_satisfied_and_logic(db_session):
    engine = PrerequisiteEngine(db_session)
    res = engine.evaluate_course_prerequisites("CS202", ["CS101", "CS103"])
    assert res["is_satisfied"] == True
    assert len(res["missing_direct"]) == 0

def test_prerequisite_missing_and_logic(db_session):
    engine = PrerequisiteEngine(db_session)
    res = engine.evaluate_course_prerequisites("CS202", ["CS101"])
    assert res["is_satisfied"] == False
    assert "CS103" in res["missing_direct"]

def test_prerequisite_satisfied_or_logic(db_session):
    engine = PrerequisiteEngine(db_session)
    res = engine.evaluate_course_prerequisites("DS101", ["DS102"])
    assert res["is_satisfied"] == True
