# Vocational Elective Explorer: Explainable Prerequisite & Career-Consequence Navigator

> **An Explainable Prerequisite and Career-Consequence Explorer for Elective Selection in Vocational Institutes.**

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React_18-61DAFB?logo=react)](https://reactjs.org/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite)](https://www.sqlite.org/)
[![Pytest](https://img.shields.io/badge/Tests-Pytest-0A9EDC?logo=pytest)](https://docs.pytest.org/)

---

## 1. Project Title
**Vocational Elective Explorer — Explainable Prerequisite & Career-Consequence Navigator**

---

## 2. Problem Statement
Vocational institutes focus on developing technical skills and hands-on competencies. However, students frequently struggle to select elective courses that align with their long-term career goals. Key challenges include:
- Selecting electives without satisfying mandatory prerequisite courses.
- Encountering schedule clashes and timetable overlaps during course registration.
- Misunderstanding how entry-level courses act as prerequisite stepping stones for advanced career pathways.
- Lack of transparent, human-understandable explanations for course recommendations.

---

## 3. Objectives
1. Provide an interactive, explainable elective course recommendation system for vocational students.
2. Automate AND/OR prerequisite graph verification, cycle detection, and catch-up sequence generation.
3. Detect hard and partial timetable schedule conflicts dynamically.
4. Align elective course selection with 18 distinct career pathways.
5. Provide robust offline/low-bandwidth client caching with seamless online/offline status detection.
6. Benchmark system performance against an unconstrained baseline using executable inferential statistics.

---

## 4. Main Features
- **Explainable Recommendation Engine**: Multi-factor scoring (Career Alignment 50%, Prerequisite Readiness 20%, Skill Overlap 15%, Pathway Value 10%, Schedule Feasibility 5%).
- **AND/OR Prerequisite Tree Engine**: Graph-based prerequisite graph traversal (`NetworkX`) supporting AND/OR groups, multi-level chains, and circular dependency safety.
- **Schedule Conflict Engine**: Minute-level timetable overlap calculation preventing registration clashes.
- **Career Pathway Explorer**: Visual career progression maps detailing prerequisite stepping stone units.
- **Human-Readable Explanations**: Plain-language non-technical explanations explaining *why* courses are recommended or blocked.
- **Offline & Low-Bandwidth Mode**: Browser `localStorage` fallback caching with fallback seed dataset and dynamic network status badge (`Online` / `Offline Mode`).
- **Student Profile & Field Capture**: Interface allowing students/instructors to specify completed courses, career goals, schedule preferences, and availability.
- **Evaluation Dashboard**: Live inferential statistical analysis ($N=150$, seed=42) featuring paired t-tests, Wilcoxon signed-rank tests, 95% CIs, and Cohen's d effect sizes.

---

## 5. System Architecture

```text
                               +-----------------------------+
                               |     Student / Instructor    |
                               +--------------+--------------+
                                              |
                                              v
                               +-----------------------------+
                               |    React + Vite Web App     |
                               |    (Tailwind CSS + Recharts)|
                               +--------------+--------------+
                                              | (Offline Fallback: LocalStorage)
                                              v
                               +-----------------------------+
                               |     FastAPI REST Server     |
                               +--------------+--------------+
                                              |
               +------------------------------+------------------------------+
               |                              |                              |
               v                              v                              v
  +--------------------------+  +--------------------------+  +--------------------------+
  |   Prerequisite Engine    |  |     Schedule Engine      |  |      Career Engine       |
  | (NetworkX Graph Traversal)|  | (Timetable Overlap Calc) |  | (Stepping Stone Mapping) |
  +------------+-------------+  +------------+-------------+  +------------+-------------+
               |                             |                             |
               +-----------------------------+-----------------------------+
                                             |
                                             v
                               +-----------------------------+
                               |    Recommendation Engine    |
                               +--------------+--------------+
                                              |
                                              v
                               +-----------------------------+
                               |     Explanation Engine      |
                               +--------------+--------------+
                                              |
                                              v
                               +-----------------------------+
                               |      SQLite Database        |
                               +-----------------------------+
```

---

## 6. Technology Stack
- **Frontend**: React 18, Vite, Tailwind CSS, Lucide Icons, Recharts, Axios.
- **Backend**: Python 3.11, FastAPI, SQLAlchemy, NetworkX, SciPy, NumPy, Pytest.
- **Database**: SQLite (`vocational.db`).

---

## 7. Folder Structure
```text
.
├── backend/
│   ├── app/
│   │   ├── engines/           # Core rule & evaluation engines
│   │   │   ├── career_engine.py
│   │   │   ├── explanation_engine.py
│   │   │   ├── prerequisite_engine.py
│   │   │   ├── recommendation_engine.py
│   │   │   └── schedule_engine.py
│   │   ├── models/            # SQLAlchemy domain models
│   │   ├── routers/           # FastAPI REST API endpoints
│   │   └── main.py            # FastAPI entry point
│   ├── seed_database.py       # DB seeder script
│   ├── requirements.txt       # Python dependencies
│   └── tests/                 # 26 automated unit & API tests
├── frontend/
│   ├── src/
│   │   ├── components/        # Navbar, CourseCards, Modals
│   │   ├── pages/             # Profile, Explorer, Pathways, Evaluation Dashboard
│   │   └── services/          # API client & offline LocalStorage cache
│   ├── package.json
│   └── vite.config.js
├── evaluation/
│   ├── baseline.py            # Naive unconstrained baseline
│   ├── dataset_generator.py   # Synthetic student profile generator (N=150, seed=42)
│   ├── experiment.py          # Reproducible experiment runner
│   ├── ground_truth.py        # Independent suitability function
│   ├── metrics.py             # Precision@K & violation metrics
│   └── statistical_analysis.py# Inferential testing (t-test/Wilcoxon, CIs, Cohen's d)
├── docs/                      # Academic reports and architecture docs
├── run.py                     # Single-command launcher
└── README.md
```

---

## 8. How to Install

```bash
# 1. Clone repository
git clone https://github.com/SureshKrishna3/coe_project.git
cd coe_project

# 2. Install backend dependencies
pip install -r backend/requirements.txt

# 3. Install frontend dependencies
cd frontend
npm install
cd ..
```

---

## 9. How to Run Backend
```bash
python backend/seed_database.py
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```
API Documentation will be available at `http://localhost:8000/docs`.

---

## 10. How to Run Frontend
```bash
cd frontend
npm run dev
```
Web application will be accessible at `http://localhost:5173`.

> **Single-Command Launch**: You can also launch both frontend and backend together using:
> `python run.py`

---

## 11. Dataset Description
*Note: All student data used for evaluation is synthetic.*
- **60 Vocational Courses**: Spanning IT, Data Science, AI, Robotics, Electronics, Embedded Systems, CAD, Cloud, and Cybersecurity.
- **18 Career Pathways**: Step-by-step career tracks with explicit prerequisite stepping stone units.
- **150 Synthetic Student Profiles**: Generated deterministically (`seed=42`) with varied semesters, completed courses, and career goals.

---

## 12. Baseline Description
**Naive / Unconstrained Course Recommendation Baseline**:
- Ranks courses purely by tag overlap with student interests and career keywords.
- Does NOT enforce prerequisite constraints.
- Does NOT enforce schedule conflict constraints.
- Does NOT provide explainable rationales.

---

## 13. Proposed System Description
**Explainable Prerequisite & Career-Consequence System**:
- Enforces strict prerequisite compliance via directed graph traversal (`NetworkX`).
- Prevents schedule clashes using timetable interval checking.
- Awards stepping-stone points for foundational prerequisites of target career goals.
- Generates transparent, human-readable explanations.

---

## 14. Evaluation Methodology
- **Sample Size**: 150 unique synthetic student profiles ($N=150$, `seed=42`).
- **Ground Truth**: Evaluated against an independent suitability check (`ground_truth.py`) operating without self-referential engine scores.
- **Statistical Tests**: Shapiro-Wilk test for normality, paired t-tests (or Wilcoxon signed-rank tests), 95% Confidence Intervals of mean differences, and Cohen's d effect sizes.

---

## 15. Metrics & Results ($N=150$, `seed=42`)

| Evaluation Metric | Baseline System | Proposed System | Statistical Result | Effect Size (Cohen's d) |
| :--- | :--- | :--- | :--- | :--- |
| **Course Choice Quality** | 7.20% | **85.07%** | $p < 0.001$ | $d = 4.19$ (Large) |
| **Prerequisite Violations** | 515 clashes | **0 clashes** (-100%) | $p < 0.001$ | $d = -2.14$ (Large) |
| **Schedule Violations** | 205 clashes | **0 clashes** (-100%) | $p < 0.001$ | $d = -1.58$ (Large) |
| **Career Pathway Alignment** | 78.17% | **88.53%** | $p < 0.001$ | $d = 0.88$ (Large) |
| **Explanation Coverage** | 0.0% | **100.0%** | $p < 0.001$ | $N/A$ |

---

## 16. Edge Cases Handled
1. **Missing Prerequisites**: Rejects ineligible courses and suggests catch-up sequences.
2. **Multi-level Prerequisite Chains**: Correctly identifies upstream dependencies ($A \rightarrow B \rightarrow C$).
3. **Circular Prerequisites**: Detects cycles ($A \leftrightarrow B$) and prevents infinite graph loops.
4. **Schedule Conflicts**: Rejects overlapping timetable schedules.
5. **Partial Schedule Overlaps**: Detects intersecting class times.
6. **Unknown Career Goal**: Falls back gracefully to general tag matching without crashing.
7. **Empty Student Profile**: Provides general beginner recommendations safely.
8. **Missing/Invalid Course Data**: Returns standard 404 HTTP errors.
9. **Duplicate Course Entries**: Deduplicates output recommendation lists.
10. **Unavailable Backend**: Uses client-side LocalStorage cache seamlessly.

---

## 17. Offline / Low-Bandwidth Support
- Automatic offline detection via `window.onoffline` / `window.ononline`.
- Essential course catalog, prerequisites, career pathways, and active student profile cached in `localStorage`.
- Default fallback dataset provided if `localStorage` is empty on first visit offline.
- Visible UI indicator (`Online` vs `Offline Mode`).

---

## 18. Testing Instructions
Run the automated test suite (26 unit tests):
```bash
pytest backend/tests
```
Build the frontend for production:
```bash
cd frontend && npm run build
```

---

## 19. Limitations
- Synthetic student profiles are used for benchmark evaluation.
- Prerequisite graph updates currently require instructor/admin role access.

---

## 20. Future Improvements
- Integration with real-world institutional Student Information Systems (SIS).
- Machine learning model fine-tuning based on historical student course pass rates.
- Multi-language support for regional vocational institutes.
