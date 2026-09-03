# Vocational Elective Explorer — System Architecture

## 1. High-Level System Architecture Diagram

```text
                               +-----------------------------------+
                               |          STUDENT USER             |
                               +-----------------------------------+
                                                 |
                                                 v
                               +-----------------------------------+
                               |    React Web App (Vite + Tailwind) |
                               +-----------------------------------+
                                                 |
                                           REST API (HTTP)
                                                 v
                               +-----------------------------------+
                               |       FastAPI Backend Server      |
                               +-----------------------------------+
                                                 |
                  +------------------------------+------------------------------+
                  |                              |                              |
                  v                              v                              v
    +---------------------------+  +---------------------------+  +---------------------------+
    |    Prerequisite Engine    |  |      Schedule Engine      |  |       Career Engine       |
    |  (NetworkX Graph + AND/OR)|  |  (Time Overlap Detection) |  |   (Pathway & Skill Match) |
    +---------------------------+  +---------------------------+  +---------------------------+
                  |                              |                              |
                  +------------------------------+------------------------------+
                                                 |
                                                 v
                               +-----------------------------------+
                               |       Recommendation Engine       |
                               |    (Explainable Score 0-100)      |
                               +-----------------------------------+
                                                 |
                                                 v
                               +-----------------------------------+
                               |        Explanation Engine         |
                               |  (Human-Readable Rationales)      |
                               +-----------------------------------+
                                                 |
                                                 v
                               +-----------------------------------+
                               |       SQLite Local Database       |
                               |   (Cached via LocalStorage/PWA)   |
                               +-----------------------------------+
```

---

## 2. Engine Components & Responsibilities

### A. Prerequisite Engine (`prerequisite_engine.py`)
- Evaluates single and multi-step dependency trees using `NetworkX.DiGraph`.
- Supports **AND logic** (all courses in group must be completed) and **OR logic** (at least one course in group must be completed).
- Detects circular prerequisites (`simple_cycles`) safely without infinite loops.
- Computes full upstream prerequisite chains and returns recommended step-by-step catch-up pathways.

### B. Schedule Engine (`schedule_engine.py`)
- Parses timetable slots (e.g., `Monday 10:00-12:00`).
- Evaluates time range overlap using interval comparison `max(s1, s2) < min(e1, e2)`.
- Flags course-to-course timetable clashes and student availability conflicts.

### C. Career Engine (`career_engine.py`)
- Maps 18 vocational career pathways (*AI Engineer*, *Data Scientist*, *Embedded Systems Engineer*, *Robotics Engineer*, *Cybersecurity Specialist*, *Fullstack Developer*, *PLC Engineer*, etc.).
- Evaluates direct course matches (mandatory core vs. recommended elective), skill overlap between course outcomes and career skills, and downstream pathway position.

### D. Recommendation Engine (`recommendation_engine.py`)
- Computes explainable score out of 100:
  $$\text{Score} = \text{Career Alignment (40)} + \text{Prerequisites (30)} + \text{Outcomes (15)} + \text{Pathway Value (10)} + \text{Schedule (5)}$$
- Enforces strict rule overrides: Missing mandatory prerequisite sets status to `MISSING_PREREQUISITES` and overrides eligibility rating regardless of career score.

### E. Explanation Engine (`explanation_engine.py`)
- Converts evaluation objects into plain-language bullet points.
- Eliminates technical jargon like "weights", "probabilities", or "embeddings".
- Generates positive highlights (`✓`), warning alerts (`✗`), and suggested next steps.
