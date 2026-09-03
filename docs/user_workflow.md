# Vocational Elective Explorer — User Workflow Journey

## 1. End-to-End Student Journey

```text
+-----------------------+
|  1. Student Profile   |  --> Enter completed courses, current semester, and select target career goal.
+-----------------------+
            |
            v
+-----------------------+
| 2. Elective Explorer  |  --> View ranked course cards with visual status badges (GREEN / YELLOW / RED).
+-----------------------+
            |
            v
+-----------------------+
| 3. Recommendation Why |  --> Click "Why this course?" for plain-language non-technical explanations.
+-----------------------+
            |
            v
+-----------------------+
| 4. Career Pathway     |  --> Explore step-by-step course sequence graph (e.g. Python -> ML -> Deep Learning -> AI Engineer).
+-----------------------+
            |
            v
+-----------------------+
| 5. Action / Alt Step  |  --> Enroll in eligible course or follow suggested prerequisite path if currently ineligible.
+-----------------------+
```

---

## 2. Step-by-Step Workflow Walkthrough

### Step 1: Profile Initialization & Goal Selection
- The student opens the application and selects or creates their profile (e.g., `STU001 - Aarav Sharma`).
- Selects current semester (e.g., Semester 3).
- Checks off completed courses (`CS101 - Programming Fundamentals`, `CS201 - Python for Data Science`).
- Selects target career outcome: `AI Engineer`.

### Step 2: Exploring Electives & Status Badges
- Navigates to **Elective Explorer**.
- Each elective card displays clear, accessible badges:
  - **GREEN (Recommended / Eligible)**: All prerequisites met, no schedule clash, high career match.
  - **YELLOW (Schedule Conflict)**: High career match but clashes with existing class session.
  - **RED (Missing Prerequisites)**: Mandatory foundational unit missing.
  - **BLUE (Completed)**: Already taken in prior term.

### Step 3: Inspecting Explanations
- The student clicks **"Why this course?"** on `DS201 - Applied Machine Learning`.
- System displays:
  - `✓ Essential mandatory course for your career goal of becoming an AI Engineer.`
  - `✓ You have completed all prerequisite courses (CS101).`
  - `✓ No timetable conflicts with your current timetable schedule.`
  - `Suggested Next Step: Strongly recommended to enroll.`

### Step 4: Handling Ineligible Choice
- The student clicks **"Why this course?"** on `DS301 - Deep Learning & Neural Networks`.
- System displays:
  - `✗ Missing mandatory prerequisite course: DS201 (Applied Machine Learning).`
  - `Suggested Next Step: Enroll in prerequisite 'DS201' first, then progress to 'DS301'.`

### Step 5: Visualizing Career Pathway
- Navigates to **Career Pathway Explorer**.
- Clicks `AI Engineer` pathway sequence:
  `CS101 (Python) -> CS201 (Data Science) -> DS201 (Machine Learning) -> DS301 (Deep Learning) -> AI Engineer`
- Inspects node statuses and acquired skills at each milestone.
