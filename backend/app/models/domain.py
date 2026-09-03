from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Course(Base):
    __tablename__ = "courses"

    course_id = Column(String, primary_key=True, index=True)
    course_name = Column(String, nullable=False, index=True)
    category = Column(String, nullable=False, index=True)
    difficulty = Column(String, nullable=False)  # Beginner, Intermediate, Advanced
    credits = Column(Integer, default=3)
    duration = Column(String, default="12 weeks")
    description = Column(Text, nullable=True)
    career_tags = Column(String, nullable=True)  # Semicolon separated

    prerequisites = relationship("Prerequisite", foreign_keys="Prerequisite.course_id", back_populates="course", cascade="all, delete-orphan")
    outcomes = relationship("CourseOutcome", back_populates="course", cascade="all, delete-orphan")
    schedules = relationship("Schedule", back_populates="course", cascade="all, delete-orphan")

class Student(Base):
    __tablename__ = "students"

    student_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    semester = Column(Integer, default=1)
    completed_courses = Column(Text, default="")  # Semicolon separated course_ids
    skills = Column(Text, default="")  # Semicolon separated
    career_goal = Column(String, nullable=True)
    preferred_schedule = Column(String, nullable=True)
    availability = Column(String, nullable=True)

class Prerequisite(Base):
    __tablename__ = "prerequisites"

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(String, ForeignKey("courses.course_id"), nullable=False, index=True)
    prerequisite_course_id = Column(String, nullable=False)
    prerequisite_type = Column(String, default="AND")  # AND, OR
    group_id = Column(Integer, default=1)  # Used to group OR conditions

    course = relationship("Course", foreign_keys=[course_id], back_populates="prerequisites")

class CourseOutcome(Base):
    __tablename__ = "course_outcomes"

    outcome_id = Column(String, primary_key=True, index=True)
    course_id = Column(String, ForeignKey("courses.course_id"), nullable=False, index=True)
    outcome_description = Column(Text, nullable=False)
    skill_tags = Column(String, nullable=True)  # Semicolon separated

    course = relationship("Course", back_populates="outcomes")

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(String, ForeignKey("courses.course_id"), nullable=False, index=True)
    day = Column(String, nullable=False)  # Monday, Tuesday, etc.
    start_time = Column(String, nullable=False)  # HH:MM format
    end_time = Column(String, nullable=False)    # HH:MM format
    location = Column(String, nullable=True)

    course = relationship("Course", back_populates="schedules")

class CareerPathway(Base):
    __tablename__ = "career_pathways"

    career_id = Column(String, primary_key=True, index=True)
    career_name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    required_courses = Column(Text, nullable=True)     # Semicolon separated course_ids
    recommended_courses = Column(Text, nullable=True)  # Semicolon separated course_ids
    skills = Column(Text, nullable=True)               # Semicolon separated
    pathway_sequence = Column(Text, nullable=True)     # e.g., CS101 -> CS201 -> DS201 -> AI Engineer

class StudentGoal(Base):
    __tablename__ = "student_goals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String, ForeignKey("students.student_id"), nullable=False)
    career_goal = Column(String, nullable=False)
    priority_weight = Column(String, default="High")

class StakeholderFeedback(Base):
    __tablename__ = "stakeholder_feedback"

    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(String, nullable=False)  # Student, Instructor, Academic Advisor
    understandable_recommendations = Column(Boolean, default=True)
    useful_prerequisites = Column(Boolean, default=True)
    useful_pathway = Column(Boolean, default=True)
    easy_to_use = Column(Boolean, default=True)
    would_use_system = Column(Boolean, default=True)
    comments = Column(Text, nullable=True)
