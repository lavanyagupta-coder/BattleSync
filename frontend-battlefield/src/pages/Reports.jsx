import { useEffect, useRef, useState } from "react";
import { startTraining, getTrainingStatus } from "../services/api";

function Reports() {
  const [job, setJob] = useState(null);
  const [error, setError] = useState(null);
  const [starting, setStarting] = useState(false);
  const pollRef = useRef(null);

  useEffect(() => {
    return () => {
      if (pollRef.current) clearInterval(pollRef.current);
    };
  }, []);

  async function handleTrain() {
    setStarting(true);
    setError(null);
    setJob(null);

    try {
      const { job_id } = await startTraining();

      pollRef.current = setInterval(async () => {
        try {
          const status = await getTrainingStatus(job_id);
          setJob(status);

          if (status.status === "completed" || status.status === "failed") {
            clearInterval(pollRef.current);
          }
        } catch (err) {
          setError(err.message);
          clearInterval(pollRef.current);
        }
      }, 2000);
    } catch (err) {
      setError(err.message);
    } finally {
      setStarting(false);
    }
  }

  return (
    <div style={{ padding: "40px", background: "#101820", minHeight: "100vh", color: "white" }}>
      <h1>Reports</h1>

      <button onClick={handleTrain} disabled={starting || job?.status === "running" || job?.status === "queued"}>
        {starting ? "Starting..." : "Run Training & Generate Report"}
      </button>

      {job && (job.status === "queued" || job.status === "running") && (
        <p>Training in progress ({job.status})... this can take a few minutes.</p>
      )}

      {error && <p style={{ color: "#ff5555" }}>{error}</p>}
      {job?.status === "failed" && <p style={{ color: "#ff5555" }}>{job.error}</p>}

      {job?.status === "completed" && job.result && (
        <div style={{ marginTop: "30px" }}>
          <h2>Best Model: {job.result.model_name}</h2>

          <pre style={{ background: "#1b2430", padding: "15px", borderRadius: "8px" }}>
            {JSON.stringify(job.result.metrics, null, 2)}
          </pre>

          <p>Full report and plots saved to: {job.result.output}</p>
        </div>
      )}
    </div>
  );
}

export default Reports;