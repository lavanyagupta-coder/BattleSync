Replace: `README.md`

```markdown
# ISR Battlefield Simulation & ML Dashboard

## Overview

This project simulates a battlefield environment to analyze the impact of Intelligence, Surveillance, and Reconnaissance (ISR) delays on mission outcomes. A Monte Carlo simulation engine models UAV detection, enemy tank movement, artillery strikes, and mission statistics. A machine learning pipeline trains classifiers on simulated data to predict mission success, and a React dashboard ties both together with live visualizations.

The project has three parts:

1. **Simulation engine** (`backend/`) — Monte Carlo battlefield simulation exposed via FastAPI.
2. **ML pipeline** (`backend/ml/`) — trains and compares Random Forest, Gradient Boosting, and XGBoost classifiers on simulated data, with SHAP/LIME explainability, and serves predictions via the same API.
3. **Frontend** (`frontend-battlefield/`) — React + Vite dashboard with a live animated battlefield map, simulation controls, analytics, prediction, and training reports.

---

## Features

- 400 × 400 km battlefield simulation
- Random tank/UAV generation and movement
- UAV detection based on detection radius
- ISR delay simulation (0–20 minutes)
- Artillery strike simulation
- Mission success percentage calculation
- Monte Carlo simulation engine (`montecarlo.py`)
- Synthetic dataset generation (CSV)
- ML training pipeline (Random Forest / Gradient Boosting / XGBoost) with hyperparameter tuning, cross-validation, SHAP/LIME explainability, and auto-generated training reports
- Background (non-blocking) model training with job status polling
- Mission outcome prediction endpoint
- FastAPI REST API with Swagger docs, CORS enabled for the frontend
- React dashboard: live battlefield map, simulation controls, analytics, prediction UI, training reports

---

## Project Structure

```
battlefield-simulator/
│
├── backend/
│   ├── app.py                 # FastAPI app, CORS, route registration
│   ├── routes.py               # ML endpoints: /ml/train, /ml/train/{job_id}, /ml/predict
│   ├── agents.py               # Tank / UAV / Artillery classes
│   ├── artillery.py
│   ├── config.py                # Simulation constants
│   ├── dataset.py               # Synthetic dataset generator
│   ├── isr.py
│   ├── montecarlo.py            # Standalone Monte Carlo runner
│   ├── simulator.py             # Core run_once() simulation logic
│   ├── utils.py
│   ├── requirements.txt
│   │
│   └── ml/
│       ├── __init__.py
│       ├── config.py             # Paths, RANDOM_STATE, CV settings
│       ├── constants.py          # Feature/target column definitions
│       ├── data_loader.py        # Loads + validates the dataset
│       ├── feature_engineering.py
│       ├── preprocessing.py      # Train/test split
│       ├── models.py             # ModelRegistry (RF, GB, XGBoost)
│       ├── tuning.py             # RandomizedSearchCV per model
│       ├── evaluation.py         # Metrics + model comparison
│       ├── explainability.py     # Feature importance, SHAP, LIME
│       ├── save_model.py         # ModelSaver — persists model + metadata, updates "latest"
│       ├── predictor.py          # BattlefieldPredictor — loads latest model, predicts
│       ├── pipeline.py           # BattleSyncPipeline — orchestrates the full training run
│       ├── train.py              # CLI entry point (python -m ml.train)
│       └── utils.py              # JSON/pickle helpers, experiment directories
│
├── frontend-battlefield/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── index.css
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── BattlefieldMap.jsx      # Live animated map (react-konva)
│   │   │   ├── SimulationControls.jsx  # Calls /custom_simulation
│   │   │   ├── StatsCard.jsx
│   │   │   └── Charts.jsx              # Recharts: outcome, model comparison, feature importance
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── Simulation.jsx
│   │   │   ├── Analytics.jsx
│   │   │   ├── Prediction.jsx
│   │   │   └── Reports.jsx
│   │   └── services/
│   │       └── api.js                  # All backend fetch calls
│   └── package.json
│
├── datasets/                   # Generated battlefield_dataset.csv lands here
├── models/                     # Trained model artifacts (backend/models, git-ignored)
├── outputs/                    # Training experiment outputs (plots, reports)
├── .gitignore
└── README.md
```

---

## Technologies Used

**Backend:** Python, FastAPI, NumPy, Pandas, Pydantic, scikit-learn, XGBoost, SHAP, LIME, Matplotlib, joblib

**Frontend:** React, Vite, react-router-dom, react-konva, Recharts

---

## Simulation Workflow

1. Generate enemy tanks at random battlefield locations.
2. Generate UAVs at random positions.
3. UAVs scan the battlefield for tanks within detection radius.
4. Introduce a random/configured ISR delay (0–20 minutes).
5. Tanks continue moving during the ISR delay.
6. Artillery strikes the previously detected tank location.
7. Determine whether the strike destroys the tank (based on how far it moved).
8. Record mission statistics, including success percentage.

## Machine Learning Workflow

1. Generate a synthetic dataset from many simulation runs (`/generate_dataset`).
2. Engineer additional features (UAV/tank ratio, delay per tank, detection efficiency).
3. Train and tune Random Forest, Gradient Boosting, and XGBoost classifiers via `RandomizedSearchCV`.
4. Evaluate and compare all three on accuracy, precision, recall, F1, ROC AUC.
5. Persist the best-performing model, its metadata, comparison table, confusion matrix / ROC / precision-recall plots, SHAP and LIME explainability outputs, and a full markdown training report.
6. Serve predictions from the latest trained model via `/ml/predict`.

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd battlefield-simulator
```

### Backend setup

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend setup

```bash
cd frontend-battlefield
npm install
npm install recharts
```

---

## Running the Project

You need two terminals running simultaneously.

### 1. Backend

```bash
cd backend
source venv/bin/activate

# generate a dataset (only needed once, or whenever you want fresh data)
python dataset.py

# start the API
uvicorn app:app --reload
```

- API: `http://127.0.0.1:8000`
- Interactive docs (Swagger): `http://127.0.0.1:8000/docs`

> **Important:** the backend scripts use flat imports (`from config import ...`), so `uvicorn` and any standalone script (`dataset.py`, `montecarlo.py`, `simulator.py`) must be run from **inside `backend/`**, not the repo root.

### 2. Frontend

```bash
cd frontend-battlefield
npm run dev
```

- App: `http://localhost:5173`

CORS is already configured on the backend to allow requests from `http://localhost:5173`.

---

## API Endpoints

### `GET /`
Returns API status.

### `GET /simulate`
Runs a single battlefield simulation with default parameters.

```json
{
  "total_tanks": 20,
  "destroyed": 13,
  "survived": 7,
  "success_percentage": 65.0
}
```

### `POST /custom_simulation`
Runs a simulation with user-provided parameters.

Request:
```json
{
    "tanks": 30,
    "uavs": 5,
    "isr_delay": 10,
    "tank_speed": 4
}
```

### `GET /generate_dataset`
Generates a synthetic dataset (10,000 records) at `datasets/battlefield_dataset.csv`.

### `POST /ml/train`
Starts model training as a **background job** and returns immediately.

```json
{ "job_id": "a1b2c3d4-...", "status": "queued" }
```

### `GET /ml/train/{job_id}`
Poll for training status/result.

```json
{
  "job_id": "a1b2c3d4-...",
  "status": "completed",
  "result": {
    "model_name": "XGBoost",
    "metrics": { "...": "..." },
    "output": "backend/models/experiments/20260805_120000"
  }
}
```

Possible `status` values: `queued`, `running`, `completed`, `failed`.

### `POST /ml/predict`
Predicts mission success from battlefield parameters, using the most recently trained model.

Request:
```json
{
  "ISR_Delay": 10,
  "Num_Tanks": 20,
  "Num_UAVs": 4,
  "Tank_Speed": 3,
  "Detection_Probability": 0.85
}
```

Response:
```json
{
  "prediction": 1,
  "mission": "Mission Success",
  "confidence": 0.87,
  "probability": { "failure": 0.13, "success": 0.87 }
}
```

Returns `503` if no model has been trained yet — run `/ml/train` first.

---

## Frontend Pages

| Page | Route | What it does |
|---|---|---|
| Home | `/` | Project overview |
| Simulation | `/simulation` | Live animated battlefield map + configurable simulation, calls `/custom_simulation` |
| Analytics | `/analytics` | Dataset generation + default simulation results, charted |
| Prediction | `/prediction` | Train model (background job w/ live status) + run predictions |
| Reports | `/reports` | Trigger training, view metrics and output location once complete |

---

## Typical First Run

```bash
# terminal 1
cd backend
source venv/bin/activate
pip install -r requirements.txt
python dataset.py
uvicorn app:app --reload

# terminal 2
cd frontend-battlefield
npm install
npm install recharts
npm run dev
```

Then in the browser:
1. Go to `/prediction` or `/reports` and click **Train Model** — wait for status to reach `completed`.
2. Go to `/prediction`, fill in the form, click **Predict**.
3. Go to `/simulation` or `/analytics` to run live simulations and see charts.

---

## Current Status

### Completed
- Battlefield simulation engine with success percentage
- UAV detection, ISR delay, artillery strike simulation
- Monte Carlo simulation engine
- Synthetic dataset generation
- Full ML pipeline: training, tuning, evaluation, explainability, model persistence
- Non-blocking background training with job polling
- FastAPI REST API with CORS + Swagger docs
- React dashboard fully wired to live backend data (map, controls, analytics, prediction, reports)

### Known Limitations
- Training job state is stored in memory — restarting the backend clears in-flight/completed job history (trained models on disk are unaffected).
- `/ml/train` runs synchronously within a single background thread; only one training job should be run at a time.
- No authentication — intended for local/demo use.

### Future Enhancements
- Persist training job history (e.g. SQLite) instead of in-memory
- Environment-based API base URL instead of hardcoded `127.0.0.1:8000`
- Deployment configuration (Docker, hosted frontend/backend)
```