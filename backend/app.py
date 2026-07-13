from fastapi import FastAPI
from pydantic import BaseModel, Field

from simulator import run_once
from dataset import generate_dataset

app = FastAPI(
    title="Battlefield Simulation API",
    version="1.0",
    description="ISR Delay & Monte Carlo Battlefield Simulator",
)


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