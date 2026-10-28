
import { getAssetUrl } from "../services/api";

function MapCard({ title, img }) {
  if (!img) return null;

  return (
    <div className="map-card">
      <h3>{title}</h3>
      <img
        src={getAssetUrl(img)}
        className="map-img"
        alt={title}
        loading="lazy"
      />
    </div>
  );
}

export default MapCard;
