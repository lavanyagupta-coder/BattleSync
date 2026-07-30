import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav>
      <Link to="/">Home</Link> |{" "}
      <Link to="/simulation">Simulation</Link> |{" "}
      <Link to="/analytics">Analytics</Link> |{" "}
      <Link to="/prediction">Prediction</Link> |{" "}
      <Link to="/reports">Reports</Link>
    </nav>
  );
}

export default Navbar;