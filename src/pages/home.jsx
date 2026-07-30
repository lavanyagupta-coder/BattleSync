import StatsCard from "../components/StatsCard";

function Home() {
  return (
    <div
      style={{
        background: "#101820",
        minHeight: "100vh",
        color: "white",
        padding: "40px",
      }}
    >
      <h1>ISR Battlefield Simulation Dashboard</h1>

      <p>
        Monte Carlo Simulation + Machine Learning for Battlefield Decision
        Support
      </p>

      <div
        style={{
          display: "flex",
          gap: "20px",
          marginTop: "40px",
          flexWrap: "wrap",
        }}
      >
        <StatsCard
          title="Mission Success"
          value="92%"
          color="#00ff88"
        />

        <StatsCard
          title="Enemy Destroyed"
          value="37"
          color="#4db8ff"
        />

        <StatsCard
          title="ISR Delay"
          value="8.2 min"
          color="#ffcc00"
        />

        <StatsCard
          title="Friendly Casualties"
          value="4"
          color="#ff5555"
        />
      </div>

      <div
        style={{
          marginTop: "50px",
          background: "#1b2430",
          padding: "30px",
          borderRadius: "12px",
        }}
      >
        <h2>Project Overview</h2>

        <p>
          This dashboard demonstrates the impact of ISR delays on battlefield
          outcomes using Monte Carlo simulation and Machine Learning. Users can
          configure battlefield parameters, run simulations, analyze mission
          performance, and predict combat outcomes.
        </p>
      </div>
    </div>
  );
}

export default Home;