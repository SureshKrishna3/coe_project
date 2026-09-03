import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.domain import Course, Student, Prerequisite, CareerPathway, Schedule
from app.engines.recommendation_engine import RecommendationEngine

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    c1 = Course(course_id="CS101", course_name="Python", category="Programming", difficulty="Beginner", credits=4, career_tags="AI Engineer")
    c2 = Course(course_id="DS201", course_name="Machine Learning", category="Machine Learning", difficulty="Advanced", credits=4, career_tags="AI Engineer")
    st = Student(student_id="STU001", name="Test Student", semester=2, completed_courses="", career_goal="AI Engineer")
    p = Prerequisite(course_id="DS201", prerequisite_course_id="CS101", prerequisite_type="AND", group_id=1)
    cp = CareerPathway(career_id="CAR001", career_name="AI Engineer", required_courses="CS101;DS201", skills="Python;Machine Learning")

    session.add_all([c1, c2, st, p, cp])
    session.commit()

    yield session
    session.close()

def test_missing_prerequisite_override(db_session):
    rec_engine = RecommendationEngine(db_session)
    st = db_session.query(Student).filter(Student.student_id == "STU001").first()
    res = rec_engine.evaluate_course("DS201", st)
    
    assert res["eligibility_status"] == "MISSING_PREREQUISITES"
    assert "Not Eligible" in res["category_rating"]
    assert len(res["alternative_pathway"]) > 0

def test_eligible_recommendation(db_session):
    rec_engine = RecommendationEngine(db_session)
    st = db_session.query(Student).filter(Student.student_id == "STU001").first()
    res = rec_engine.evaluate_course("CS101", st)
    
    assert res["eligibility_status"] == "ELIGIBLE"
    assert res["score"] > 50.0

def test_recommend_electives_with_synthetic_student_object(db_session):
    """
    Verifies synthetic student EVAL_STU_001 passed directly as a Student object
    without requiring that student to exist in the database.
    """
    rec_engine = RecommendationEngine(db_session)
    synthetic_student = Student(
        student_id="EVAL_STU_001",
        name="Synthetic Eval Student",
        semester=3,
        completed_courses="CS101",
        skills="Python",
        career_goal="AI Engineer",
        preferred_schedule="Monday 09:00-11:00",
        availability="Morning"
    )

    # Must NOT raise ValueError and must evaluate recommendations cleanly
    recs = rec_engine.recommend_electives(student=synthetic_student)
    assert isinstance(recs, list)
    assert len(recs) == 2
    assert recs[0]["course_id"] in ["CS101", "DS201"]

def test_recommend_electives_with_real_student_id(db_session):
    """
    Verifies normal behavior querying DB by student_id string STU001.
    """
    rec_engine = RecommendationEngine(db_session)
    recs = rec_engine.recommend_electives(student_id="STU001")
    assert isinstance(recs, list)
    assert len(recs) == 2
