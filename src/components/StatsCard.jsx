function StatsCard({ title, value, color }) {
  return (
    <div
      style={{
        background: "#1b2430",
        padding: "20px",
        borderRadius: "12px",
        width: "220px",
        boxShadow: "0 0 10px rgba(0,0,0,0.3)",
      }}
    >
      <h3 style={{ color: "#bbb" }}>{title}</h3>

      <h1 style={{ color: color, marginTop: "10px" }}>{value}</h1>
    </div>
  );
}

export default StatsCard;