# Vocational Elective Explorer — Automated Test Report

## 1. Test Suite Summary

- **Test Framework**: Pytest + FastAPI TestClient
- **Test Suite Path**: `backend/tests/`
- **Total Test Cases**: 24
- **Passed**: 24 (100% pass rate)
- **Failed**: 0
- **Execution Time**: ~11.2 seconds

---

## 2. Test Cases Breakdown

### Module 1: Edge & Failure Case Tests (`test_edge_cases.py`) — Phase 11
| Test Case ID | Test Description | Result |
| :--- | :--- | :--- |
| `test_missing_prerequisite` | Verifies course marked `MISSING_PREREQUISITES` when student lacks background. | PASSED |
| `test_and_prerequisite` | Verifies AND logic (all prerequisites in group must be satisfied). | PASSED |
| `test_or_prerequisite` | Verifies OR logic (either prerequisite in group satisfies requirement). | PASSED |
| `test_schedule_conflict` | Verifies hard timetable clash detection for overlapping sessions. | PASSED |
| `test_unknown_career_goal` | Verifies graceful fallback keyword matching for unregistered career goals. | PASSED |
| `test_no_suitable_courses_fallback` | Verifies graceful fallback to introductory units when no match exists. | PASSED |
| `test_empty_student_profile` | Verifies handling of empty student profile input fields. | PASSED |
| `test_invalid_course_id_api` | Verifies 404 HTTP Exception response for invalid course IDs without crashing. | PASSED |
| `test_circular_prerequisite` | Verifies graph cycle detection (`simple_cycles`) for circular prerequisites. | PASSED |
| `test_partial_dataset_fields` | Verifies system stability when course description or tags are missing. | PASSED |

### Module 2: Prerequisite Engine (`test_prerequisite_engine.py`)
| Test Case ID | Test Description | Result |
| :--- | :--- | :--- |
| `test_prerequisite_satisfied_and_logic` | Verifies course eligibility when all AND prerequisites are completed. | PASSED |
| `test_prerequisite_missing_and_logic` | Verifies course rejection when an AND prerequisite is missing. | PASSED |
| `test_prerequisite_satisfied_or_logic` | Verifies course eligibility when at least one OR prerequisite is met. | PASSED |

### Module 3: Schedule Engine (`test_schedule_engine.py`)
| Test Case ID | Test Description | Result |
| :--- | :--- | :--- |
| `test_time_overlap` | Tests interval overlap detection for adjacent vs overlapping time slots. | PASSED |
| `test_schedule_conflict_detection` | Verifies detection of hard timetable clashes between overlapping course sessions. | PASSED |
| `test_no_schedule_conflict` | Verifies clean clearance when courses occur on non-overlapping slots. | PASSED |

### Module 4: Recommendation Engine (`test_recommendation_engine.py`)
| Test Case ID | Test Description | Result |
| :--- | :--- | :--- |
| `test_missing_prerequisite_override` | Verifies that missing prerequisites override score to `MISSING_PREREQUISITES`. | PASSED |
| `test_eligible_recommendation` | Verifies high score calculation and `ELIGIBLE` status for valid courses. | PASSED |

### Module 5: API Endpoints (`test_api_endpoints.py`)
| Test Case ID | Test Description | Result |
| :--- | :--- | :--- |
| `test_health_endpoint` | Verifies `/api/health` returns HTTP 200 and healthy status. | PASSED |
| `test_get_courses` | Verifies `/api/courses` lists course catalog from database. | PASSED |
| `test_get_students` | Verifies `/api/students` lists student profiles. | PASSED |
| `test_get_careers` | Verifies `/api/careers` lists 18 career pathways. | PASSED |
| `test_get_recommendations` | Verifies `/api/recommendations/{student_id}` returns ranked recommendations. | PASSED |
| `test_stakeholder_stats` | Verifies `/api/stakeholder/stats` returns validation statistics. | PASSED |
