import os
import csv
from sqlalchemy.orm import Session
from app.database import engine, Base, SessionLocal
from app.models.domain import (
    Course, Student, Prerequisite, CourseOutcome, Schedule, CareerPathway, StudentGoal
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

def seed_db():
    print("Recreating database tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()

    try:
        # 1. Seed Courses
        courses_file = os.path.join(DATA_DIR, "courses.csv")
        if os.path.exists(courses_file):
            print(f"Seeding Courses from {courses_file}...")
            with open(courses_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    c = Course(
                        course_id=row["course_id"].strip(),
                        course_name=row["course_name"].strip(),
                        category=row["category"].strip(),
                        difficulty=row["difficulty"].strip(),
                        credits=int(row["credits"]),
                        duration=row["duration"].strip(),
                        description=row["description"].strip(),
                        career_tags=row["career_tags"].strip()
                    )
                    db.add(c)
            db.commit()

        # 2. Seed Prerequisites
        prereqs_file = os.path.join(DATA_DIR, "prerequisites.csv")
        if os.path.exists(prereqs_file):
            print(f"Seeding Prerequisites from {prereqs_file}...")
            with open(prereqs_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    p = Prerequisite(
                        course_id=row["course_id"].strip(),
                        prerequisite_course_id=row["prerequisite_course_id"].strip(),
                        prerequisite_type=row.get("prerequisite_type", "AND").strip(),
                        group_id=int(row.get("group_id", 1))
                    )
                    db.add(p)
            db.commit()

        # 3. Seed Course Outcomes
        outcomes_file = os.path.join(DATA_DIR, "course_outcomes.csv")
        if os.path.exists(outcomes_file):
            print(f"Seeding Course Outcomes from {outcomes_file}...")
            with open(outcomes_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    o = CourseOutcome(
                        outcome_id=row["outcome_id"].strip(),
                        course_id=row["course_id"].strip(),
                        outcome_description=row["outcome_description"].strip(),
                        skill_tags=row["skill_tags"].strip()
                    )
                    db.add(o)
            db.commit()

        # 4. Seed Schedules
        schedules_file = os.path.join(DATA_DIR, "schedules.csv")
        if os.path.exists(schedules_file):
            print(f"Seeding Schedules from {schedules_file}...")
            with open(schedules_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    s = Schedule(
                        course_id=row["course_id"].strip(),
                        day=row["day"].strip(),
                        start_time=row["start_time"].strip(),
                        end_time=row["end_time"].strip(),
                        location=row["location"].strip()
                    )
                    db.add(s)
            db.commit()

        # 5. Seed Career Pathways
        careers_file = os.path.join(DATA_DIR, "career_pathways.csv")
        if os.path.exists(careers_file):
            print(f"Seeding Career Pathways from {careers_file}...")
            with open(careers_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cp = CareerPathway(
                        career_id=row["career_id"].strip(),
                        career_name=row["career_name"].strip(),
                        description=row["description"].strip(),
                        required_courses=row["required_courses"].strip(),
                        recommended_courses=row["recommended_courses"].strip(),
                        skills=row["skills"].strip(),
                        pathway_sequence=row["pathway_sequence"].strip()
                    )
                    db.add(cp)
            db.commit()

        # 6. Seed Students
        students_file = os.path.join(DATA_DIR, "students.csv")
        if os.path.exists(students_file):
            print(f"Seeding Students from {students_file}...")
            with open(students_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    st = Student(
                        student_id=row["student_id"].strip(),
                        name=row["name"].strip(),
                        semester=int(row["semester"]),
                        completed_courses=row["completed_courses"].strip(),
                        skills=row["skills"].strip(),
                        career_goal=row["career_goal"].strip(),
                        preferred_schedule=row["preferred_schedule"].strip(),
                        availability=row["availability"].strip()
                    )
                    db.add(st)
            db.commit()

        # 7. Seed Student Goals
        goals_file = os.path.join(DATA_DIR, "student_goals.csv")
        if os.path.exists(goals_file):
            print(f"Seeding Student Goals from {goals_file}...")
            with open(goals_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    sg = StudentGoal(
                        student_id=row["student_id"].strip(),
                        career_goal=row["career_goal"].strip(),
                        priority_weight=row["priority_weight"].strip()
                    )
                    db.add(sg)
            db.commit()

        print("Database seed completed successfully!")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
