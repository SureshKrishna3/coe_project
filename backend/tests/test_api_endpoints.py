import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_get_courses():
    response = client.get("/api/courses")
    assert response.status_code == 200
    courses = response.json()
    assert isinstance(courses, list)
    assert len(courses) > 0

def test_get_students():
    response = client.get("/api/students")
    assert response.status_code == 200
    students = response.json()
    assert isinstance(students, list)

def test_get_careers():
    response = client.get("/api/careers")
    assert response.status_code == 200
    careers = response.json()
    assert isinstance(careers, list)

def test_get_recommendations():
    response = client.get("/api/recommendations/STU001")
    assert response.status_code == 200
    recs = response.json()
    assert isinstance(recs, list)
    assert len(recs) > 0

def test_stakeholder_stats():
    response = client.get("/api/stakeholder/stats")
    assert response.status_code == 200
    stats = response.json()
    assert "total_responses" in stats
