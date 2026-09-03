import csv
import random

CAREERS = [
    "AI Engineer", "Data Scientist", "Data Analyst", "Software Engineer",
    "Fullstack Developer", "Backend Developer", "Frontend Developer",
    "Cybersecurity Specialist", "Embedded Systems Engineer", "Robotics Engineer",
    "IoT Specialist", "Industrial Automation Engineer", "PLC Engineer",
    "Cloud Solutions Architect", "DevOps Engineer", "CAD Design Engineer",
    "Smart Manufacturing Specialist", "VLSI Engineer"
]

COURSE_POOL = [
    "CS101", "CS102", "CS201", "CS202", "CS301", "CS302", "DS101", "DS201", "DS301", "DS302",
    "WEB101", "WEB201", "WEB301", "WEB302", "NET101", "NET201", "CYBER101", "CYBER201", "CYBER301",
    "ELEC101", "ELEC201", "ELEC301", "EMB201", "EMB301", "ROB101", "ROB201", "ROB301",
    "AUTO101", "AUTO201", "CAD101", "CAD201", "MFG101", "MFG201", "CLOUD101", "CLOUD201", "CLOUD301",
    "ELEC202", "ELEC302", "CS203", "DS202", "DS203", "WEB202", "CYBER202", "ELEC102", "EMB101",
    "ROB202", "AUTO102", "CAD102", "MFG102", "CLOUD202", "CYBER102", "DS102", "ELEC303", "CS303",
    "CS204", "CS103", "CS205", "WEB102", "DS303", "ROB102"
]

SKILLS_POOL = [
    "Python", "C++", "Java", "SQL", "JavaScript", "React.js", "FastAPI", "Pandas",
    "NumPy", "PyTorch", "HTML/CSS", "Networking", "Linux", "Cybersecurity",
    "Circuit Design", "Embedded C", "Microcontrollers", "PLC Programming", "ROS2",
    "SolidWorks", "CAD", "CNC Machining", "Cloud Computing", "Docker", "DevOps", "Statistics"
]

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
TIMES = ["09:00-11:00", "10:00-12:00", "11:00-13:00", "14:00-16:00"]

FIRST_NAMES = ["Aarav", "Ananya", "Rohan", "Priya", "Vikram", "Sneha", "Aditya", "Kavya", "Rahul", "Neha",
               "Siddharth", "Pooja", "Arjun", "Divya", "Karthik", "Riya", "Manish", "Shreya", "Nitin", "Meera",
               "Alex", "Jordan", "Taylor", "Morgan", "Sam", "Chris", "Pat", "Riley", "Casey", "Dakota"]
LAST_NAMES = ["Sharma", "Verma", "Patel", "Rao", "Nair", "Gupta", "Singh", "Kumar", "Iyer", "Joshi",
              "Reddy", "Deshmukh", "Chowdhury", "Mehta", "Bhat", "Kulkarni", "Smith", "Johnson", "Williams", "Brown"]

random.seed(42)

students = []
student_goals = []

# Generate 250 student profiles
for i in range(1, 251):
    student_id = f"STU{i:03d}"
    name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    semester = random.randint(1, 6)
    career_goal = random.choice(CAREERS)
    
    # Pick completed courses based on semester level
    num_completed = min(random.randint(0, semester * 3), 15)
    completed_courses = random.sample(COURSE_POOL, k=num_completed)
    
    # Ensure foundational courses are more likely for higher semesters
    if semester >= 2 and "CS101" not in completed_courses and random.random() < 0.7:
        completed_courses.append("CS101")
    if semester >= 2 and "ELEC101" not in completed_courses and random.random() < 0.5:
        completed_courses.append("ELEC101")
    if semester >= 2 and "WEB101" not in completed_courses and random.random() < 0.5:
        completed_courses.append("WEB101")
        
    completed_str = ";".join(sorted(list(set(completed_courses))))
    
    num_skills = random.randint(1, 6)
    skills = ";".join(random.sample(SKILLS_POOL, k=num_skills))
    
    pref_day = random.choice(DAYS)
    pref_time = random.choice(TIMES)
    pref_sched = f"{pref_day} {pref_time}"
    availability = f"{random.choice(['Morning', 'Afternoon', 'Full-Day'])} (Available weekdays)"
    
    students.append({
        "student_id": student_id,
        "name": name,
        "semester": semester,
        "completed_courses": completed_str,
        "skills": skills,
        "career_goal": career_goal,
        "preferred_schedule": pref_sched,
        "availability": availability
    })
    
    student_goals.append({
        "student_id": student_id,
        "career_goal": career_goal,
        "priority_weight": random.choice(["High", "Medium", "Critical"])
    })

# Write students.csv
with open("data/students.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["student_id", "name", "semester", "completed_courses", "skills", "career_goal", "preferred_schedule", "availability"])
    writer.writeheader()
    writer.writerows(students)

# Write student_goals.csv
with open("data/student_goals.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["student_id", "career_goal", "priority_weight"])
    writer.writeheader()
    writer.writerows(student_goals)

print(f"Successfully generated {len(students)} student records in data/students.csv and data/student_goals.csv.")
