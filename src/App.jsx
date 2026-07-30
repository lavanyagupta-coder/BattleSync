import { BrowserRouter, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";

import Home from "./pages/Home";
import Simulation from "./pages/Simulation";
import Analytics from "./pages/Analytics";
import Prediction from "./pages/Prediction";
import Reports from "./pages/Reports";

function App() {

    return (

        <BrowserRouter>

            <Navbar />

            <Routes>

                <Route path="/" element={<Home />} />

                <Route path="/simulation" element={<Simulation />} />

                <Route path="/analytics" element={<Analytics />} />

                <Route path="/prediction" element={<Prediction />} />

                <Route path="/reports" element={<Reports />} />

            </Routes>

        </BrowserRouter>

    )

}

export default App;