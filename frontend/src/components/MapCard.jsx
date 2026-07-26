function MapCard({title,img}){

return(

<div className="map-card">

<h3>{title}</h3>

<img
src={`http://127.0.0.1:8000${img}`}
className="map-img"
/>

</div>

)

}

export default MapCard