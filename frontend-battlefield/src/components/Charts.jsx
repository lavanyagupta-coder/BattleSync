import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const COLORS = ["#00ff88", "#ff5555", "#4db8ff", "#ffcc00", "#c084fc"];

export function MissionOutcomeChart({ destroyed = 0, survived = 0 }) {
  const data = [
    { name: "Destroyed", value: destroyed },
    { name: "Survived", value: survived },
  ];

  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie data={data} dataKey="value" nameKey="name" outerRadius={100} label>
          {data.map((entry, index) => (
            <Cell key={entry.name} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
}

export function ModelComparisonChart({ data = [] }) {
  return (
    <ResponsiveContainer width="100%" height={350}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="#2e303a" />
        <XAxis dataKey="Model" stroke="#bbb" />
        <YAxis stroke="#bbb" domain={[0, 1]} />
        <Tooltip />
        <Legend />
        <Bar dataKey="Accuracy" fill={COLORS[2]} />
        <Bar dataKey="F1 Score" fill={COLORS[0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}

export function FeatureImportanceChart({ data = [] }) {
  return (
    <ResponsiveContainer width="100%" height={350}>
      <BarChart data={data} layout="vertical">
        <CartesianGrid strokeDasharray="3 3" stroke="#2e303a" />
        <XAxis type="number" stroke="#bbb" />
        <YAxis type="category" dataKey="Feature" stroke="#bbb" width={140} />
        <Tooltip />
        <Bar dataKey="Importance" fill={COLORS[3]} />
      </BarChart>
    </ResponsiveContainer>
  );
}