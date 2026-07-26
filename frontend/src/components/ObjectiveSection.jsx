import {useState} from "react"
import {analyzeObjectives} from "../services/api"

const objectives = [
"All",
"Health",
"Water Stress",
"Chlorophyll",
"Disease Detection",
"Disease Localization",
"Growth Monitoring",
"Yield Estimation",
"Zone Mapping",
"Disease Prediction"
]

function ObjectiveSection({file,setResult,setMessage}){

const [selected,setSelected] = useState("All")
const [loading,setLoading] = useState(false)

const notImplemented = [
"Health",
"Disease Detection",
"Disease Localization",
"Growth Monitoring",
"Yield Estimation",
"Disease Prediction"
]

const handleAnalyze = async()=>{

if(!file)return

setLoading(true)

if(notImplemented.includes(selected)){

const res = await analyzeObjectives(file,"classification")

setResult(res)

setMessage("This will be implemented in the future.")

setLoading(false)

return

}

setMessage("")

const res = await analyzeObjectives(file,selected)

setResult(res)

setLoading(false)

}

return(

<div className="objective-box">

<select
className="objective-select"
value={selected}
onChange={(e)=>setSelected(e.target.value)}
>

{objectives.map(o=>(
<option key={o} value={o}>{o}</option>
))}

</select>

<button onClick={handleAnalyze} disabled={loading}>

{loading ? "Processing..." : "Analyze"}

</button>

</div>

)

}

export default ObjectiveSection