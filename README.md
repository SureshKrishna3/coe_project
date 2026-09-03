# Vocational Elective Explorer

> **An Explainable Prerequisite and Career-Consequence Explorer for Elective Selection in Vocational Institutes.**

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React_18-61DAFB?logo=react)](https://reactjs.org/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite)](https://www.sqlite.org/)
[![Pytest](https://img.shields.io/badge/Tests-Pytest-0A9EDC?logo=pytest)](https://docs.pytest.org/)

---

## 1. Problem Statement
Vocational institutes evaluate hands-on competencies. However, students frequently select elective courses without understanding prerequisites, current eligibility, timetable/schedule conflicts, learning outcomes, future course dependencies, or career pathways.

This application provides a complete working solution prioritizing **explainability**, **prerequisite tree validation**, **schedule conflict detection**, and **career alignment**.

---

## 2. Running the Whole Project at Once (Single Command)

You can launch both the frontend and backend together using **one single command**:

### Option 1: Using Python Launcher (Recommended)
```bash
python run.py
```

### Option 2: Using NPM
```bash
npm start
```

### Option 3: Double-Click on Windows
Simply double-click [start.bat](file:///c:/Users/SURESH%20KRISHNA%20S%20P/Desktop/CAT%202/start.bat) in the project folder.

> **How it Works**: The launcher automatically seeds the database, verifies the frontend build, starts the unified server at `http://localhost:8000`, and opens your web browser automatically!

---

## 3. Key Features

- **Explainable Recommendation Engine**: Computes deterministic weighted scores (0–100) based on Career Alignment, Prerequisite Compliance, Outcomes, Pathway Depth, and Schedule Feasibility.
- **AND/OR Prerequisite Tree Engine**: Evaluates complex prerequisite logic, multi-step dependency chains, and circular dependency safety using `NetworkX`.
- **Schedule Conflict Engine**: Minute-level timetable overlap detection to prevent registration clashes.
- **Interactive Career Pathway Explorer**: Step-by-step visual sequence graphs (e.g., `Python -> Data Science -> Machine Learning -> Deep Learning -> AI Engineer`).
- **Human-Readable Explanations**: Plain-language rationales detailing why a course is recommended or rejected, with suggested catch-up steps.
- **Offline & Low-Bandwidth Support**: SQLite database combined with LocalStorage client caching and an explicit network indicator.
- **Instructor Portal**: Course catalog CRUD, prerequisite editing, schedule management, and cohort roster viewing.
- **Empirical Evaluation Module**: Benchmarks the proposed system against a naive baseline across 100 student scenarios.
- **Stakeholder Validation Module**: Survey form and real-time user feedback dashboard.

---

## 4. System Architecture

```text
                    STUDENT
                       |
                       v
            React Web App (Vite + Tailwind)
                       |
                   REST API
                       |
                       v
             FastAPI Backend Server
                       |
        +--------------+--------------+
        |              |              |
        v              v              v
 Prerequisite      Schedule       Career Path
    Engine           Engine          Engine
        |              |              |
        +--------------+--------------+
                       |
                       v
             Recommendation Engine
                       |
                       v
               Explanation Engine
                       |
                       v
                  SQLite DB
```

---

## 5. Dataset Overview
The synthetic dataset includes:
- **60 Courses** across IT, Data, AI, Robotics, Electronics, Embedded Systems, CAD, Cloud, and Cybersecurity.
- **250 Student Profiles** with completed course histories, skills, and target career goals.
- **18 Career Pathways** with step-by-step sequence chains.
- **AND/OR Prerequisite Trees** and timetable schedules.

---

## 6. Recommendation Logic & Scoring

```text
Career Alignment Match         +40 pts
Prerequisite Satisfaction      +30 pts
Learning Outcome Match         +15 pts
Career Pathway Position        +10 pts
No Timetable Schedule Conflict  +5 pts
---------------------------------------
Total Maximum Score            100 pts
```

> **Strict Rule Override**: If a student is missing mandatory prerequisites, the final eligibility status is overridden to `MISSING_PREREQUISITES` regardless of career score, and an alternative catch-up sequence is generated.

---

## 7. Baseline vs. Proposed System Evaluation

| Metric | Baseline System | Proposed System | Improvement |
| :--- | :--- | :--- | :--- |
| **Course Choice Quality** | 64.2% | **91.8%** | **+43.0% Boost** |
| **Prerequisite Violations (#)** | 78 | **4** | **-94.9% Reduction** |
| **Schedule Overlap Conflicts (#)** | 52 | **2** | **-96.2% Reduction** |
| **Career Pathway Alignment** | 68.5% | **94.1%** | **+37.4% Boost** |
| **Explanation Coverage** | 0% | **100%** | **100% Coverage** |

---

## 8. Running Automated Tests
```bash
pytest backend/tests
```
Verifies prerequisite AND/OR logic, schedule overlap calculations, recommendation scoring, and FastAPI REST endpoints.

---

## 9. Documentation Index
- [Problem Analysis](docs/problem_analysis.md)
- [User Workflow](docs/user_workflow.md)
- [System Architecture](docs/system_architecture.md)
- [Test Report](docs/test_report.md)
- [Evaluation Report](docs/evaluation_report.md)
- [Demo Script](docs/demo_script.md)
