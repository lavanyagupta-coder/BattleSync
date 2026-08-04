from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from simulator import run_once
from dataset import generate_dataset
from routes import router as ml_router

app = FastAPI(
    title="Battlefield Simulation API",
    version="1.0",
    description="ISR Delay & Monte Carlo Battlefield Simulator",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ml_router)


class SimulationRequest(BaseModel):
    tanks: int = Field(default=20, ge=1)
    uavs: int = Field(default=4, ge=1)
    isr_delay: int = Field(default=10, ge=0)
    tank_speed: int = Field(default=3, gt=0)


@app.get("/")
def home():
    return {
        "message": "Battlefield Simulation API Running"
    }


@app.get("/simulate")
def simulate():
    """
    Run simulation using default configuration.
    """
    return run_once()


@app.get("/generate_dataset")
def dataset():
    """
    Generate synthetic battlefield dataset.
    """
    generate_dataset(10000)

    return {
        "status": "Dataset Generated"
    }


@app.post("/custom_simulation")
def custom_simulation(data: SimulationRequest):
    """
    Run simulation with user-defined parameters.
    """

    result = run_once(
        num_tanks=data.tanks,
        num_uavs=data.uavs,
        tank_speed=data.tank_speed,
        isr_delay=data.isr_delay,
    )

    return {
        "Input": data.model_dump(),
        "Result": result,
    }