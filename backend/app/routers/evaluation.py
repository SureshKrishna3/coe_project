import os
import sys

# Ensure root folder is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from evaluation.experiment import run_evaluation_experiment

router = APIRouter(prefix="/api/evaluation", tags=["Evaluation"])

_cached_results = None

@router.post("/run")
def run_evaluation(num_samples: int = 100, db: Session = Depends(get_db)):
    global _cached_results
    results = run_evaluation_experiment(db, num_samples=num_samples)
    _cached_results = results
    return results

@router.get("/results")
def get_evaluation_results(num_samples: int = 100, db: Session = Depends(get_db)):
    global _cached_results
    if _cached_results is None:
        _cached_results = run_evaluation_experiment(db, num_samples=num_samples)
    return _cached_results
