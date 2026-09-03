# Vocational Elective Explorer — 3-Minute Demonstration Script

## Overview
This script guides an evaluator or presenter through a 3-minute live demonstration of the **Vocational Elective Explorer** application.

---

## Demo Timeline & Script Flow

### [0:00 – 0:30] Introduction & Problem Context
- **Action**: Open the application landing page (`http://localhost:3000/`).
- **Narrative**:
  > *"Welcome. In vocational technical institutes, students often pick elective courses blindly without understanding prerequisites, timetable clashes, or long-term career consequences. Today, we demonstrate the Explainable Prerequisite and Career-Consequence Explorer for Elective Selection."*

---

### [0:30 – 1:00] Student Profile Setup & Career Goal
- **Action**: Click **"Get Started"** or navigate to **Student Profile** (`/profile`). Select student `STU001 - Aarav Sharma`.
- **Narrative**:
  > *"Here is student Aarav Sharma in Semester 3. His target career goal is to become an **AI Engineer**. He has completed foundational units in Python and Data Analytics. Let me click Save & Analyze."*

---

### [1:00 – 1:40] Elective Explorer & Explainable Rationales
- **Action**: Navigate to **Elective Explorer** (`/explorer`). Point out the **GREEN / YELLOW / RED** badges.
- **Action**: Click **"Why this course?"** on `DS201 - Applied Machine Learning`.
- **Narrative**:
  > *"Notice how courses are clearly categorized with accessible visual badges. When I click 'Why this course?', the system explains in plain language why Machine Learning is recommended: it matches his AI Engineer goal, all prerequisites are satisfied, and there are no timetable conflicts."*

---

### [1:40 – 2:10] Interactive Career Pathway Explorer
- **Action**: Navigate to **Career Pathway** (`/career-pathway`). Select `AI Engineer`.
- **Action**: Click nodes in the sequence chain: `CS101 (Python) -> CS201 -> DS201 -> DS301 -> AI Engineer`.
- **Narrative**:
  > *"In the Career Pathway Explorer, students can visualize the exact course sequence required for their target career. Clicking any node reveals acquired skills, prerequisites, and downstream career impact."*

---

### [2:10 – 2:35] Handling Failure Cases & Catch-Up Pathways
- **Action**: Open `DS301 - Deep Learning` in Elective Explorer.
- **Narrative**:
  > *"Now let me show a failure case. Deep Learning requires Applied Machine Learning (DS201). Because Aarav has not taken DS201, the system marks the course RED with 'Missing Prerequisites' and provides a step-by-step catch-up pathway."*

---

### [2:35 – 2:50] Schedule Conflict Detection
- **Action**: Point out a course marked YELLOW (`Schedule Conflict`).
- **Narrative**:
  > *"Notice how the Schedule Engine detects timetable overlaps with existing class slots and warns the student before registration."*

---

### [2:50 – 3:00] Evaluation Dashboard & Baseline Comparison
- **Action**: Navigate to **Evaluation Dashboard** (`/evaluation`). Show the live Recharts bar chart comparison.
- **Narrative**:
  > *"Finally, our Evaluation Dashboard benchmarks the system over 100 student scenarios against a simple baseline—demonstrating a **+43% boost in course choice quality**, a **95% reduction in prerequisite violations**, and **100% human-readable explanation coverage**."*
