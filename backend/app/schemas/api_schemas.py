from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class PrerequisiteSchema(BaseModel):
    id: Optional[int] = None
    course_id: str
    prerequisite_course_id: str
    prerequisite_type: str = "AND"
    group_id: int = 1

    class Config:
        from_attributes = True

class OutcomeSchema(BaseModel):
    outcome_id: str
    course_id: str
    outcome_description: str
    skill_tags: Optional[str] = ""

    class Config:
        from_attributes = True

class ScheduleSchema(BaseModel):
    id: Optional[int] = None
    course_id: str
    day: str
    start_time: str
    end_time: str
    location: Optional[str] = ""

    class Config:
        from_attributes = True

class CourseBase(BaseModel):
    course_id: str
    course_name: str
    category: str
    difficulty: str
    credits: int = 3
    duration: str = "12 weeks"
    description: Optional[str] = ""
    career_tags: Optional[str] = ""

class CourseCreate(CourseBase):
    pass

class CourseDetail(CourseBase):
    prerequisites: List[PrerequisiteSchema] = []
    outcomes: List[OutcomeSchema] = []
    schedules: List[ScheduleSchema] = []

    class Config:
        from_attributes = True

class StudentBase(BaseModel):
    student_id: str
    name: str
    semester: int = 1
    completed_courses: Optional[str] = ""
    skills: Optional[str] = ""
    career_goal: Optional[str] = ""
    preferred_schedule: Optional[str] = ""
    availability: Optional[str] = ""

class StudentCreate(StudentBase):
    pass

class StudentDetail(StudentBase):
    class Config:
        from_attributes = True

class CareerPathwaySchema(BaseModel):
    career_id: str
    career_name: str
    description: Optional[str] = ""
    required_courses: Optional[str] = ""
    recommended_courses: Optional[str] = ""
    skills: Optional[str] = ""
    pathway_sequence: Optional[str] = ""

    class Config:
        from_attributes = True

class RecommendationRequest(BaseModel):
    student_id: str
    career_goal: Optional[str] = None
    completed_courses: Optional[List[str]] = None
    schedule_preference: Optional[str] = None

class RecommendationResult(BaseModel):
    course_id: str
    course_name: str
    category: str
    difficulty: str
    credits: int
    duration: str
    score: float
    category_rating: str  # Highly Recommended, Recommended, Consider, Low Priority, Not Recommended
    eligibility_status: str  # ELIGIBLE, MISSING_PREREQUISITES, SCHEDULE_CONFLICT, NOT_ELIGIBLE
    prerequisite_status: Dict[str, Any]
    schedule_status: Dict[str, Any]
    career_alignment: Dict[str, Any]
    explanation: Dict[str, Any]
    alternative_pathway: List[str] = []

class EvaluationRequest(BaseModel):
    num_samples: int = 100

class EvaluationSummary(BaseModel):
    total_samples: int
    baseline_metrics: Dict[str, float]
    proposed_metrics: Dict[str, float]
    percentage_improvement: Dict[str, float]
    error_analysis: List[Dict[str, Any]]
    confusion_data: Dict[str, Any]

class StakeholderFeedbackCreate(BaseModel):
    role: str
    understandable_recommendations: bool = True
    useful_prerequisites: bool = True
    useful_pathway: bool = True
    easy_to_use: bool = True
    would_use_system: bool = True
    comments: Optional[str] = ""
