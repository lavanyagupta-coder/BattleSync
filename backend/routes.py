import threading
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field

from ml import BattleSyncPipeline, BattlefieldPredictor

router = APIRouter(prefix="/ml", tags=["Machine Learning"])

_predictor = None
_predictor_lock = threading.Lock()

_jobs = {}
_jobs_lock = threading.Lock()


def get_predictor():
    global _predictor

    if _predictor is None:
        with _predictor_lock:
            if _predictor is None:
                _predictor = BattlefieldPredictor()

    return _predictor


def invalidate_predictor():
    global _predictor

    with _predictor_lock:
        _predictor = None


class PredictionRequest(BaseModel):
    ISR_Delay: float = Field(..., ge=0)
    Num_Tanks: float = Field(..., gt=0)
    Num_UAVs: float = Field(..., gt=0)
    Tank_Speed: float = Field(..., gt=0)
    Detection_Probability: float = Field(..., ge=0, le=1)


@router.post("/predict")
def predict(data: PredictionRequest):
    try:
        predictor = get_predictor()
    except FileNotFoundError as error:
        raise HTTPException(
            status_code=503,
            detail=f"No trained model available yet: {error}",
        )

    try:
        return predictor.predict(data.model_dump())
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


def _run_training_job(job_id):
    with _jobs_lock:
        _jobs[job_id]["status"] = "running"
        _jobs[job_id]["started_at"] = datetime.now(timezone.utc).isoformat()

    pipeline = BattleSyncPipeline()

    try:
        result = pipeline.train()
    except FileNotFoundError as error:
        with _jobs_lock:
            _jobs[job_id]["status"] = "failed"
            _jobs[job_id]["error"] = (
                f"{error}. Generate a dataset first via /generate_dataset."
            )
        return
    except Exception as error:  # noqa: BLE001 - surface any training failure to the client
        with _jobs_lock:
            _jobs[job_id]["status"] = "failed"
            _jobs[job_id]["error"] = str(error)
        return

    invalidate_predictor()

    with _jobs_lock:
        _jobs[job_id]["status"] = "completed"
        _jobs[job_id]["finished_at"] = datetime.now(timezone.utc).isoformat()
        _jobs[job_id]["result"] = {
            "model_name": result["model_name"],
            "metrics": result["metrics"],
            "parameters": result["parameters"],
            "output": str(result["output"]),
        }


@router.post("/train")
def train(background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())

    with _jobs_lock:
        _jobs[job_id] = {
            "status": "queued",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

    background_tasks.add_task(_run_training_job, job_id)

    return {"job_id": job_id, "status": "queued"}


@router.get("/train/{job_id}")
def train_status(job_id: str):
    with _jobs_lock:
        job = _jobs.get(job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Unknown job id")

    return {"job_id": job_id, **job}