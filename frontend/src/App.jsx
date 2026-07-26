import {useState} from "react"

import UploadSection from "./components/UploadSection"
import ObjectiveSection from "./components/ObjectiveSection"
import MapCard from "./components/MapCard"
import StatsCard from "./components/StatsCard"

import "./styles/dashboard.css"

function App(){

const [result,setResult] = useState(null)
const [file,setFile] = useState(null)
const [message,setMessage] = useState("")

return(

<div className="container">

<h1>Multispectral Crop Imaging Drone</h1>

<UploadSection setResult={setResult} setFile={setFile}/>

{result &&

<div className="map-card">

<h3>Uploaded Crop Image</h3>

<img
src={`http://127.0.0.1:8000${result.uploaded_image}`}
className="map-img"
/>

</div>

}

{result &&

<h2 className="status">

{result.crop === "Paddy"
? "Uploaded Image is Paddy"
: "Uploaded image is not Paddy"}

</h2>

}

{result?.crop === "Paddy" &&
<ObjectiveSection
file={file}
setResult={setResult}
setMessage={setMessage}
/>
}

{message && <h3>{message}</h3>}

{result?.crop === "Paddy" &&

<>

{/* ROW 1 */}

<div className="dashboard">

<MapCard title="NDVI Map" img={result.ndvi}/>
<MapCard title="NDWI Map" img={result.ndwi}/>
<MapCard title="NDRE Map" img={result.ndre}/>

</div>

{/* ROW 2 */}

<div className="dashboard">

{result.maps?.water_stress &&
<MapCard title="Water Stress Map" img={result.maps.water_stress}/>
}

{result.maps?.chlorophyll &&
<MapCard title="Chlorophyll Map" img={result.maps.chlorophyll}/>
}

{result.maps?.zone &&
<MapCard title="Management Zone Map" img={result.maps.zone}/>
}

</div>

{/* ROW 3 */}

<div className="dashboard">

{result.water_stress_stats &&
<StatsCard
title="Water Stress Statistics"
data={result.water_stress_stats}
/>
}

{result.chlorophyll_stats &&
<StatsCard
title="Chlorophyll Statistics"
data={result.chlorophyll_stats}
/>
}

{result.zone_stats &&
<StatsCard
title="Zone Statistics"
data={result.zone_stats}
/>
}

</div>

</>

}

</div>

)

}

export default App