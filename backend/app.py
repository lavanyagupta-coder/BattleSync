from fastapi import FastAPI
from pydantic import BaseModel

from simulator import run_once
from dataset import generate_dataset

app = FastAPI(
    title="Battlefield Simulation API",
    version="1.0",
    description="ISR Delay & Monte Carlo Battlefield Simulator",
)


class SimulationRequest(BaseModel):

    tanks: int
    uavs: int
    isr_delay: int
    tank_speed: int


@app.get("/")
def home():

    return {
        "message": "Battlefield Simulation API Running"
    }


@app.get("/simulate")
def simulate():

    return run_once()


@app.get("/generate_dataset")
def dataset():

    generate_dataset(10000)

    return {
        "status": "Dataset Generated"
    }


@app.post("/custom_simulation")
def custom_simulation(data: SimulationRequest):

    # Currently using default simulator.
    # Later you'll pass these values into run_once()

    result = run_once()

    return {
        "Input": data.dict(),
        "Result": result,
    }