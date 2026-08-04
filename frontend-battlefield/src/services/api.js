const BASE_URL = "http://127.0.0.1:8000";

async function handleResponse(response) {
  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}));
    throw new Error(errorBody.detail || `Request failed: ${response.status}`);
  }
  return response.json();
}

export async function getStatus() {
  const response = await fetch(`${BASE_URL}/`);
  return handleResponse(response);
}

export async function runSimulation() {
  const response = await fetch(`${BASE_URL}/simulate`);
  return handleResponse(response);
}

export async function runCustomSimulation({ tanks, uavs, isr_delay, tank_speed }) {
  const response = await fetch(`${BASE_URL}/custom_simulation`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ tanks, uavs, isr_delay, tank_speed }),
  });
  return handleResponse(response);
}

export async function generateDataset() {
  const response = await fetch(`${BASE_URL}/generate_dataset`);
  return handleResponse(response);
}

export async function startTraining() {
  const response = await fetch(`${BASE_URL}/ml/train`, { method: "POST" });
  return handleResponse(response);
}

export async function getTrainingStatus(jobId) {
  const response = await fetch(`${BASE_URL}/ml/train/${jobId}`);
  return handleResponse(response);
}

export async function predictMission(features) {
  const response = await fetch(`${BASE_URL}/ml/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(features),
  });
  return handleResponse(response);
}