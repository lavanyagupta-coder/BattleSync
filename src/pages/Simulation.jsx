import BattlefieldMap from "../components/BattlefieldMap";
import SimulationControls from "../components/SimulationControls";

function Simulation(){

    return(

        <div
            style={{
                display:"flex",
                gap:"30px",
                padding:"30px",
                background:"#101820",
                minHeight:"100vh"
            }}
        >

            <SimulationControls/>

            <BattlefieldMap/>

        </div>

    )

}

export default Simulation;