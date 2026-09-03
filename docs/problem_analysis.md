# Vocational Elective Explorer — Problem Analysis

## 1. Problem Statement & Background
Vocational and technical institutes evaluate hands-on practical competencies across diverse engineering and technology tracks (e.g., Programming, Data Science, AI, Robotics, Electronics, CAD, Automation, Cloud, Cybersecurity). 

When selecting elective courses, students frequently struggle with multi-dimensional decision complexity:
- **Unclear Prerequisite Dependencies**: Students register for advanced courses (e.g., *Deep Learning* or *Autonomous Mobile Robots*) without realizing they lack mandatory foundational units (*Python*, *Linear Algebra*, *ROS2*).
- **Timetable & Schedule Overlaps**: Students select courses whose laboratory or lecture sessions clash with existing compulsory classes.
- **Unclear Learning Outcomes**: Course descriptions lack clear mapping to tangible hands-on skills acquired upon completion.
- **Career Goal Misalignment**: Electives are chosen based on peer trends rather than their direct alignment with specific industry job titles (e.g., *AI Engineer*, *PLC Engineer*, *Cloud Solutions Architect*).
- **Lack of Explanation**: Traditional course portals present static lists or opaque black-box recommendations without explaining *why* a course is suitable or why a student is ineligible.

---

## 2. Target Users & Stakeholders

| Stakeholder Persona | Key Pain Points | System Solution |
| :--- | :--- | :--- |
| **Vocational Student** | Confused by complex course rules, schedule clashes, and long-term career impact. | Transparent scoring (0–100), visual status badges (GREEN/YELLOW/RED), and plain-language explanations. |
| **Academic Advisor / Instructor** | Spends hours manually auditing student eligibility and resolving timetable conflicts. | Automated prerequisite AND/OR checking, schedule conflict detection, and cohort roster insights. |
| **Institute Administrator** | High student drop-out and failure rates due to missing prerequisites. | Enforces strict rule overrides and provides alternative prerequisite progression pathways. |

---

## 3. Current Manual Workflow vs. Proposed Explainable System

```text
CURRENT MANUAL WORKFLOW:
Student reads printed catalog -> Selects course blindly -> Registers on portal -> Course clash / fail prerequisite -> Drop out or re-register late

PROPOSED EXPLAINABLE WORKFLOW:
Student Profile & Career Goal -> Prerequisite Engine (AND/OR trees) -> Schedule Engine (Timetable overlap check) -> Career Engine (Pathway alignment) -> Explainable Recommendation (Score + Rationales + Step-by-step Alternatives)
```

---

## 4. Key Functional Requirements

1. **Explainable Deterministic Scoring**: Configurable weights for Career Match (+40), Prerequisite Compliance (+30), Outcomes (+15), Pathway Value (+10), and Schedule Feasibility (+5).
2. **Prerequisite Enforcement**: Supports AND and OR logic trees, multi-level dependency chains, and circular dependency safety.
3. **Schedule Conflict Detection**: Identifies time-range overlaps across days and locations.
4. **Interactive Pathway Graph**: Visualizes step-by-step course sequences leading to professional career outcomes.
5. **Offline & Low-Bandwidth Support**: Local SQLite database and client-side caching for reliable field operation.
