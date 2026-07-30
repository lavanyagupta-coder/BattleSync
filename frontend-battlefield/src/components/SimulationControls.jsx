import { useState } from "react";

function SimulationControls() {
  const [isrDelay, setIsrDelay] = useState(5);
  const [tanks, setTanks] = useState(50);
  const [uavs, setUavs] = useState(3);
  const [artilleryRange, setArtilleryRange] = useState(120);
  const [detectionProb, setDetectionProb] = useState(0.85);

  function runSimulation() {
    alert("Simulation Started!");
  }

  return (
    <div
      style={{
        background: "#1b2430",
        padding: "25px",
        borderRadius: "12px",
        width: "350px",
      }}
    >
      <h2>Simulation Controls</h2>

      <br />

      <label>ISR Delay (minutes)</label>

      <input
        type="range"
        min="0"
        max="20"
        value={isrDelay}
        onChange={(e) => setIsrDelay(e.target.value)}
      />

      <p>{isrDelay} minutes</p>

      <label>Number of Tanks</label>

      <input
        type="number"
        value={tanks}
        onChange={(e) => setTanks(e.target.value)}
      />

      <br />
      <br />

      <label>Number of UAVs</label>

      <input
        type="number"
        value={uavs}
        onChange={(e) => setUavs(e.target.value)}
      />

      <br />
      <br />

      <label>Artillery Range (km)</label>

      <input
        type="number"
        value={artilleryRange}
        onChange={(e) => setArtilleryRange(e.target.value)}
      />

      <br />
      <br />

      <label>Detection Probability</label>

      <input
        type="number"
        step="0.01"
        value={detectionProb}
        onChange={(e) => setDetectionProb(e.target.value)}
      />

      <br />
      <br />

      <button onClick={runSimulation}>
        Run Simulation
      </button>
    </div>
  );
}

export default SimulationControls;