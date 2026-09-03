import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.database import engine, Base
from app.routers import students, courses, careers, recommendations, evaluation, stakeholder

# Create database tables if they do not exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Vocational Elective Explorer API",
    description="Explainable Prerequisite and Career-Consequence Explorer for Elective Selection",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for frontend client
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(students.router)
app.include_router(courses.router)
app.include_router(careers.router)
app.include_router(recommendations.router)
app.include_router(evaluation.router)
app.include_router(stakeholder.router)

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Vocational Elective Explorer Backend API",
        "offline_ready": True
    }

# Serve built frontend static files if present (Production Unified Single-Port Mode)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DIST_DIR = os.path.join(BASE_DIR, "frontend", "dist")

if os.path.exists(DIST_DIR):
    assets_dir = os.path.join(DIST_DIR, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/")
    async def serve_root():
        return FileResponse(os.path.join(DIST_DIR, "index.html"))

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # Allow API calls to pass through if unmatched
        if full_path.startswith("api/"):
            return {"detail": "Not Found"}
        
        file_path = os.path.join(DIST_DIR, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(DIST_DIR, "index.html"))
