import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.domain import Schedule
from app.engines.schedule_engine import ScheduleEngine

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    s1 = Schedule(course_id="CS101", day="Monday", start_time="09:00", end_time="11:00", location="Lab 1")
    s2 = Schedule(course_id="CS102", day="Monday", start_time="10:00", end_time="12:00", location="Lab 2")
    s3 = Schedule(course_id="CS201", day="Monday", start_time="11:00", end_time="13:00", location="Lab 3")

    session.add_all([s1, s2, s3])
    session.commit()

    yield session
    session.close()

def test_time_overlap(db_session):
    engine = ScheduleEngine(db_session)
    assert engine.times_overlap("09:00", "11:00", "10:00", "12:00") == True
    assert engine.times_overlap("09:00", "11:00", "11:00", "13:00") == False  # Adjacent, no overlap

def test_schedule_conflict_detection(db_session):
    engine = ScheduleEngine(db_session)
    res = engine.check_conflict("CS102", ["CS101"])
    assert res["has_conflict"] == True
    assert len(res["conflicts"]) == 1

def test_no_schedule_conflict(db_session):
    engine = ScheduleEngine(db_session)
    res = engine.check_conflict("CS201", ["CS101"])
    assert res["has_conflict"] == False
