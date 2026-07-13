# Battlefield Simulation using Monte Carlo & ISR Delay

## Overview

This project simulates a battlefield environment to analyze the impact of Intelligence, Surveillance, and Reconnaissance (ISR) delays on mission outcomes. The simulator models UAV detection, enemy tank movement, artillery strikes, and mission statistics using Monte Carlo simulations.

The backend also provides REST APIs for running simulations and generating synthetic datasets, which can later be used for machine learning and visualization.

---

## Features

- 400 × 400 km battlefield simulation
- Random generation of enemy tanks
- Random generation of UAVs
- Random tank movement
- UAV detection based on detection radius
- ISR delay simulation (0–20 minutes)
- Tank movement during ISR delay
- Artillery strike simulation
- Mission statistics generation
- Monte Carlo simulation engine
- Synthetic dataset generation (CSV)
- FastAPI REST APIs
- Interactive Swagger API documentation

---

## Project Structure

```
battlefield-simulator/
│
├── backend/
│   ├── app.py
│   ├── agents.py
│   ├── artillery.py
│   ├── config.py
│   ├── dataset.py
│   ├── isr.py
│   ├── montecarlo.py
│   ├── simulator.py
│   ├── utils.py
│   └── requirements.txt
│
├── datasets/
│
├── outputs/
│
├── .gitignore
└── README.md
```

---

## Technologies Used

- Python
- FastAPI
- NumPy
- Pandas
- Pydantic

---

## Simulation Workflow

1. Generate enemy tanks at random battlefield locations.
2. Generate UAVs at random positions.
3. UAVs scan the battlefield.
4. Tanks within the UAV detection radius are detected.
5. Introduce a random ISR delay (0–20 minutes).
6. Tanks continue moving during the ISR delay.
7. Artillery strikes the previously detected tank location.
8. Determine whether the strike is successful.
9. Record mission statistics.

---

## Monte Carlo Simulation

The simulator supports running thousands of independent battlefield simulations.

Example:

```
10000 simulations

↓

Mission Statistics

↓

Average Tanks Destroyed

↓

Average Tanks Survived
```

---

## Dataset Generation

A synthetic dataset is generated from multiple battlefield simulations.

Generated features include:

- ISR_Delay
- Num_Tanks
- Num_UAVs
- Tank_Speed
- Detection_Probability
- Destroyed
- Survived
- Mission_Success

Output location:

```
datasets/battlefield_dataset.csv
```

---

## API Endpoints

### GET /

Returns the API status.

---

### GET /simulate

Runs a single battlefield simulation.

Example Response

```json
{
  "total_tanks": 20,
  "destroyed": 13,
  "survived": 7
}
```

---

### GET /generate_dataset

Generates a synthetic dataset from multiple simulations.

---

### POST /custom_simulation

Runs a simulation using user-provided parameters.

Example Request

```json
{
    "tanks": 30,
    "uavs": 5,
    "isr_delay": 10,
    "tank_speed": 4
}
```

---

## Installation

Clone the repository

```bash
git clone <repository-url>
```

Navigate to the backend directory

```bash
cd backend
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Project

Start the FastAPI server

```bash
uvicorn app:app --reload
```

The server will start at

```
http://127.0.0.1:8000
```

Interactive API documentation is available at

```
http://127.0.0.1:8000/docs
```

---

## Current Status

### Completed

- Battlefield simulation engine
- Tank movement algorithm
- UAV detection system
- ISR delay implementation
- Artillery strike simulation
- Mission statistics generation
- Monte Carlo simulation engine
- Synthetic dataset generation
- FastAPI backend APIs
- Swagger API documentation

---

## Future Enhancements

- Interactive React dashboard
- Live battlefield visualization
- Configurable battlefield parameters
- Machine learning prediction models
- Analytics dashboard
- Simulation reports and exports
