import random
from typing import List, Dict, Any

RANDOM_SEED = 42

SCENARIO_DISTRIBUTION = {
    "valid_prereqs": 25,
    "missing_one_prereq": 20,
    "missing_multiple_prereqs": 20,
    "hard_schedule_conflict": 15,
    "soft_schedule_warning": 15,
    "strong_career_match": 15,
    "weak_career_match": 15,
    "unknown_career": 10,
    "empty_profile": 5,
    "multilevel_prereqs": 10
}

CAREERS = [
    "AI Engineer", "Data Scientist", "Data Analyst", "Software Engineer",
    "Fullstack Developer", "Backend Developer", "Frontend Developer",
    "Cybersecurity Specialist", "Embedded Systems Engineer", "Robotics Engineer",
    "IoT Specialist", "Industrial Automation Engineer", "PLC Engineer",
    "Cloud Solutions Architect", "DevOps Engineer", "CAD Design Engineer",
    "Smart Manufacturing Specialist", "VLSI Engineer"
]

SKILLS_POOL = [
    "Python", "C++", "Java", "SQL", "JavaScript", "React.js", "FastAPI", "Pandas",
    "NumPy", "PyTorch", "HTML/CSS", "Networking", "Linux", "Cybersecurity",
    "Circuit Design", "Embedded C", "Microcontrollers", "PLC Programming", "ROS2",
    "SolidWorks", "CAD", "CNC Machining", "Cloud Computing", "Docker", "DevOps", "Statistics"
]

FIRST_NAMES = ["Aarav", "Ananya", "Rohan", "Priya", "Vikram", "Sneha", "Aditya", "Kavya", "Rahul", "Neha",
               "Siddharth", "Pooja", "Arjun", "Divya", "Karthik", "Riya", "Manish", "Shreya", "Nitin", "Meera"]
LAST_NAMES = ["Sharma", "Verma", "Patel", "Rao", "Nair", "Gupta", "Singh", "Kumar", "Iyer", "Joshi"]

def generate_evaluation_dataset(seed: int = RANDOM_SEED) -> List[Dict[str, Any]]:
    """
    Generates a reproducible evaluation dataset of 150 synthetic student profiles
    covering 10 distinct scenario types.
    """
    random.seed(seed)
    dataset = []
    student_idx = 1

    for scenario_type, count in SCENARIO_DISTRIBUTION.items():
        for _ in range(count):
            s_id = f"EVAL_STU_{student_idx:03d}"
            name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
            semester = random.randint(1, 6)
            career_goal = random.choice(CAREERS)
            completed_courses = []
            skills = random.sample(SKILLS_POOL, k=random.randint(1, 4))
            preferred_schedule = "Monday 09:00-11:00"
            availability = "Morning"

            if scenario_type == "valid_prereqs":
                semester = 3
                career_goal = "AI Engineer"
                completed_courses = ["CS101", "CS201", "DS101"]
                skills = ["Python", "Pandas", "Data Analysis"]

            elif scenario_type == "missing_one_prereq":
                semester = 2
                career_goal = "Data Scientist"
                completed_courses = ["CS101"]  # Missing DS101 / DS203 for Applied ML

            elif scenario_type == "missing_multiple_prereqs":
                semester = 1
                career_goal = "AI Engineer"
                completed_courses = []  # Missing CS101, CS201, DS201

            elif scenario_type == "hard_schedule_conflict":
                semester = 3
                career_goal = "Software Engineer"
                completed_courses = ["CS101"]
                # CS102 is Monday 10:00-12:00, ROB101 is Monday 10:00-12:00
                completed_courses.append("ROB101")

            elif scenario_type == "soft_schedule_warning":
                semester = 2
                career_goal = "Fullstack Developer"
                completed_courses = ["WEB101"]
                availability = "Morning"
                preferred_schedule = "Morning 09:00-11:00"

            elif scenario_type == "strong_career_match":
                semester = 4
                career_goal = "Robotics Engineer"
                completed_courses = ["ELEC101", "ROB101"]
                skills = ["ROS2", "Robotics Basics", "Circuit Design"]

            elif scenario_type == "weak_career_match":
                semester = 3
                career_goal = "CAD Design Engineer"
                completed_courses = ["CS101", "WEB101"]  # Software courses for CAD goal

            elif scenario_type == "unknown_career":
                semester = 2
                career_goal = "Quantum Cryptography Specialist"  # Niche goal not in standard registry
                completed_courses = ["CS101", "NET101"]

            elif scenario_type == "empty_profile":
                semester = 1
                career_goal = ""
                completed_courses = []
                skills = []

            elif scenario_type == "multilevel_prereqs":
                semester = 4
                career_goal = "Deep Learning Specialist"
                completed_courses = ["CS101", "CS201"]  # Needs CS101 -> CS201 -> DS201 -> DS301

            dataset.append({
                "student_id": s_id,
                "name": name,
                "semester": semester,
                "completed_courses": ";".join(completed_courses),
                "skills": ";".join(skills),
                "career_goal": career_goal,
                "preferred_schedule": preferred_schedule,
                "availability": availability,
                "scenario_type": scenario_type
            })
            student_idx += 1

    return dataset
