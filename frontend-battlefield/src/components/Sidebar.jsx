import { Link } from "react-router-dom";

function Navbar() {
    return (
        <nav style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            padding: "15px 40px",
            backgroundColor: "#101820",
            color: "white"
        }}>

            <h2>ISR Battlefield Simulator</h2>

            <div style={{display:"flex",gap:"20px"}}>

                <Link to="/">Home</Link>

                <Link to="/simulation">Simulation</Link>

                <Link to="/analytics">Analytics</Link>

                <Link to="/prediction">Prediction</Link>

                <Link to="/reports">Reports</Link>

            </div>

        </nav>
    )
}

export default Navbar;