import { useState } from "react";
import BattlefieldMap from "../components/BattlefieldMap";
import SimulationControls from "../components/SimulationControls";
import { MissionOutcomeChart } from "../components/Charts";

function Simulation() {
  const [result, setResult] = useState(null);

  return (
    <div
      style={{
        display: "flex",
        flexWrap: "wrap",
        gap: "30px",
        padding: "30px",
        background: "#101820",
        minHeight: "100vh",
      }}
    >
      <SimulationControls onResult={setResult} />

      <BattlefieldMap />

      {result && (
        <div
          style={{
            background: "#1b2430",
            padding: "25px",
            borderRadius: "12px",
            color: "white",
            width: "350px",
          }}
        >
          <h2>Latest Result</h2>
          <p>Total Tanks: {result.total_tanks}</p>
          <p>Destroyed: {result.destroyed}</p>
          <p>Survived: {result.survived}</p>
          <p>Success Rate: {result.success_percentage}%</p>

          <MissionOutcomeChart
            destroyed={result.destroyed}
            survived={result.survived}
          />
        </div>
      )}
    </div>
  );
}

export default Simulation;