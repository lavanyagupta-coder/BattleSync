import { useEffect, useRef, useState } from "react";
import { predictMission, startTraining, getTrainingStatus } from "../services/api";

function Prediction() {
  const [form, setForm] = useState({
    ISR_Delay: 10,
    Num_Tanks: 20,
    Num_UAVs: 4,
    Tank_Speed: 3,
    Detection_Probability: 0.85,
  });
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [trainingStatus, setTrainingStatus] = useState(null);
  const pollRef = useRef(null);

  useEffect(() => {
    return () => {
      if (pollRef.current) clearInterval(pollRef.current);
    };
  }, []);

  function update(field, value) {
    setForm((prev) => ({ ...prev, [field]: Number(value) }));
  }

  async function handlePredict() {
    setLoading(true);
    setError(null);
    try {
      const response = await predictMission(form);
      setResult(response);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleTrain() {
    setError(null);
    setTrainingStatus("starting");

    try {
      const { job_id } = await startTraining();
      setTrainingStatus("queued");

      pollRef.current = setInterval(async () => {
        try {
          const status = await getTrainingStatus(job_id);
          setTrainingStatus(status.status);

          if (status.status === "completed" || status.status === "failed") {
            clearInterval(pollRef.current);
            if (status.status === "failed") setError(status.error);
          }
        } catch (err) {
          setError(err.message);
          clearInterval(pollRef.current);
        }
      }, 2000);
    } catch (err) {
      setError(err.message);
      setTrainingStatus(null);
    }
  }

  const isTraining = trainingStatus === "starting" || trainingStatus === "queued" || trainingStatus === "running";

  return (
    <div style={{ padding: "40px", background: "#101820", minHeight: "100vh", color: "white" }}>
      <h1>Mission Prediction</h1>

      <button onClick={handleTrain} disabled={isTraining} style={{ marginBottom: "10px" }}>
        {isTraining ? `Training (${trainingStatus})...` : "Train Model"}
      </button>

      <div style={{ display: "flex", flexDirection: "column", gap: "10px", maxWidth: "300px", marginTop: "20px" }}>
        <label>ISR Delay (min)</label>
        <input type="number" value={form.ISR_Delay} onChange={(e) => update("ISR_Delay", e.target.value)} />

        <label>Number of Tanks</label>
        <input type="number" value={form.Num_Tanks} onChange={(e) => update("Num_Tanks", e.target.value)} />

        <label>Number of UAVs</label>
        <input type="number" value={form.Num_UAVs} onChange={(e) => update("Num_UAVs", e.target.value)} />

        <label>Tank Speed</label>
        <input type="number" value={form.Tank_Speed} onChange={(e) => update("Tank_Speed", e.target.value)} />

        <label>Detection Probability</label>
        <input
          type="number"
          step="0.01"
          min="0"
          max="1"
          value={form.Detection_Probability}
          onChange={(e) => update("Detection_Probability", e.target.value)}
        />

        <button onClick={handlePredict} disabled={loading}>
          {loading ? "Predicting..." : "Predict"}
        </button>
      </div>

      {error && <p style={{ color: "#ff5555", marginTop: "20px" }}>{error}</p>}

      {result && (
        <div style={{ marginTop: "30px", background: "#1b2430", padding: "20px", borderRadius: "12px", maxWidth: "300px" }}>
          <h2>{result.mission}</h2>
          <p>Confidence: {(result.confidence * 100).toFixed(1)}%</p>
          <p>Success Probability: {(result.probability.success * 100).toFixed(1)}%</p>
          <p>Failure Probability: {(result.probability.failure * 100).toFixed(1)}%</p>
        </div>
      )}
    </div>
  );
}

export default Prediction;