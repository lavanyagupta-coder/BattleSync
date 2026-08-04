import { useState } from "react";
import { generateDataset, runSimulation } from "../services/api";
import { MissionOutcomeChart } from "../components/Charts";

function Analytics() {
  const [result, setResult] = useState(null);
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleGenerateDataset() {
    setLoading(true);
    setError(null);
    try {
      const response = await generateDataset();
      setStatus(response.status);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleRunSimulation() {
    setLoading(true);
    setError(null);
    try {
      const response = await runSimulation();
      setResult(response);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ padding: "40px", background: "#101820", minHeight: "100vh", color: "white" }}>
      <h1>Analytics Dashboard</h1>

      <div style={{ display: "flex", gap: "15px", marginTop: "20px" }}>
        <button onClick={handleGenerateDataset} disabled={loading}>
          Generate Dataset
        </button>
        <button onClick={handleRunSimulation} disabled={loading}>
          Run Default Simulation
        </button>
      </div>

      {status && <p>{status}</p>}
      {error && <p style={{ color: "#ff5555" }}>{error}</p>}

      {result && (
        <div style={{ marginTop: "30px", maxWidth: "500px" }}>
          <p>Total Tanks: {result.total_tanks}</p>
          <p>Destroyed: {result.destroyed}</p>
          <p>Survived: {result.survived}</p>
          <p>Success Rate: {result.success_percentage}%</p>

          <MissionOutcomeChart destroyed={result.destroyed} survived={result.survived} />
        </div>
      )}
    </div>
  );
}

export default Analytics;