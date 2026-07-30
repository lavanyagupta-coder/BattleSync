import { Stage, Layer, Circle, Rect, Text } from "react-konva";
import { useEffect, useState } from "react";

function BattlefieldMap() {

    const [tanks, setTanks] = useState([
        {x:100,y:100},
        {x:220,y:250},
        {x:450,y:180}
    ]);

    const [uavs, setUavs] = useState([
        {x:50,y:50},
        {x:600,y:80}
    ]);

    useEffect(()=>{

        const interval=setInterval(()=>{

            setTanks(old=>
                old.map(t=>({
                    ...t,
                    x:t.x+(Math.random()*10-5),
                    y:t.y+(Math.random()*10-5)
                }))
            )

            setUavs(old=>
                old.map(u=>({
                    ...u,
                    x:u.x+2,
                    y:u.y+1
                }))
            )

        },100)

        return ()=>clearInterval(interval)

    },[])

    return(

        <Stage width={900} height={600}>

            <Layer>

                <Rect
                    x={0}
                    y={0}
                    width={900}
                    height={600}
                    fill="#202830"
                />

                {uavs.map((u,index)=>

                    <Circle
                        key={index}
                        x={u.x}
                        y={u.y}
                        radius={10}
                        fill="cyan"
                    />

                )}

                {tanks.map((t,index)=>

                    <Rect
                        key={index}
                        x={t.x}
                        y={t.y}
                        width={20}
                        height={20}
                        fill="red"
                    />

                )}

                <Text
                    text="Battlefield"
                    x={10}
                    y={10}
                    fill="white"
                />

            </Layer>

        </Stage>

    )

}

export default BattlefieldMap;