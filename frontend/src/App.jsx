
import { useState } from "react";
import UploadSection from "./components/UploadSection";
import ObjectiveSection from "./components/ObjectiveSection";
import MapCard from "./components/MapCard";
import StatsCard from "./components/StatsCard";
import { getAssetUrl } from "./services/api";
import "./styles/dashboard.css";

function getNumericValue(data, key) {
  if (!data || data[key] === null || data[key] === undefined || data[key] === "") {
    return null;
  }

  const value = Number(data[key]);
  return Number.isFinite(value) ? value : null;
}

function formatPercent(value) {
  return value === null ? "Not available" : `${value.toFixed(2)}%`;
}

function getDominantZone(zoneStats) {
  if (!zoneStats) return null;

  const zones = Object.entries(zoneStats)
    .filter(([key, value]) => /^zone_\d+_percent$/.test(key) && Number.isFinite(Number(value)))
    .map(([key, value]) => ({
      name: key.replace("_percent", "").replace("_", " "),
      percentage: Number(value),
    }));

  if (!zones.length) return null;

  return zones.reduce((largest, zone) =>
    zone.percentage > largest.percentage ? zone : largest
  );
}

function OverallAnalysisSummary({ result }) {
  const water = result.water_stress_stats ?? {};
  const chlorophyll = result.chlorophyll_stats ?? {};
  const zones = result.zone_stats ?? {};

  const highStress = getNumericValue(water, "high_stress_percent");
  const moderateStress = getNumericValue(water, "moderate_stress_percent");
  const lowStress = getNumericValue(water, "low_stress_percent");

  const lowChlorophyll = getNumericValue(chlorophyll, "low_chlorophyll_percent");
  const moderateChlorophyll = getNumericValue(chlorophyll, "moderate_chlorophyll_percent");
  const highChlorophyll = getNumericValue(chlorophyll, "high_chlorophyll_percent");

  const dominantZone = getDominantZone(zones);

  const priorities = [];

  if (highStress !== null && highStress > 0) {
    priorities.push(
      `Inspect areas marked as high water stress (${formatPercent(highStress)}) on the water stress map.`
    );
  }

  if (lowChlorophyll !== null && lowChlorophyll > 0) {
    priorities.push(
      `Review areas classified as low chlorophyll (${formatPercent(lowChlorophyll)}) on the chlorophyll map.`
    );
  }

  const zone1 = getNumericValue(zones, "zone_1_percent");
  const zone2 = getNumericValue(zones, "zone_2_percent");

  if ((zone1 !== null && zone1 > 0) || (zone2 !== null && zone2 > 0)) {
    priorities.push(
      "Inspect the smaller management zones in the zone map to determine whether they require field-level attention."
    );
  }

  if (!priorities.length) {
    priorities.push(
      "Review the generated maps and available statistics before deciding whether field inspection is required."
    );
  }

  const hasWaterStats =
    highStress !== null || moderateStress !== null || lowStress !== null;

  const hasChlorophyllStats =
    lowChlorophyll !== null ||
    moderateChlorophyll !== null ||
    highChlorophyll !== null;

  const hasZoneStats = Boolean(dominantZone);

  return (
    <section className="overall-summary" aria-labelledby="overall-summary-title">
      <div className="summary-header">
        <div>
          <p className="summary-eyebrow">FIELD ANALYSIS REPORT</p>
          <h2 id="overall-summary-title">Overall Analysis Summary</h2>
          <p className="summary-subtitle">
            A summary of the current multispectral image analysis results.
          </p>
        </div>

        <span className="crop-badge">
          {result.crop === "Paddy" ? "Paddy Detected" : result.crop}
        </span>
      </div>

      <div className="summary-grid">
        <article className="summary-panel key-metrics">
          <h3>Key Metrics</h3>

          <div className="metric-row">
            <span>Crop classification</span>
            <strong>{result.crop || "Not available"}</strong>
          </div>

          <div className="metric-row">
            <span>Vegetation index maps</span>
            <strong>
              {[result.ndvi, result.ndwi, result.ndre].filter(Boolean).length} / 3
            </strong>
          </div>

          <div className="metric-row">
            <span>High water stress</span>
            <strong>{formatPercent(highStress)}</strong>
          </div>

          <div className="metric-row">
            <span>Low chlorophyll</span>
            <strong>{formatPercent(lowChlorophyll)}</strong>
          </div>

          <div className="metric-row">
            <span>Largest management zone</span>
            <strong>
              {dominantZone
                ? `${dominantZone.name} (${formatPercent(dominantZone.percentage)})`
                : "Not available"}
            </strong>
          </div>
        </article>

        <article className="summary-panel analysis-overview">
          <h3>Analysis Overview</h3>

          <p>
            The uploaded image was classified as{" "}
            <strong>{result.crop || "unknown"}</strong>.
            {result.ndvi && result.ndwi && result.ndre
              ? " NDVI, NDWI, and NDRE maps are available for visual inspection."
              : " Some vegetation index maps are unavailable in this response."}
          </p>

          {hasWaterStats && (
            <div className="overview-group">
              <h4>Water stress distribution</h4>
              <p>
                Low: {formatPercent(lowStress)} · Moderate:{" "}
                {formatPercent(moderateStress)} · High:{" "}
                {formatPercent(highStress)}
              </p>
            </div>
          )}

          {hasChlorophyllStats && (
            <div className="overview-group">
              <h4>Chlorophyll distribution</h4>
              <p>
                Low: {formatPercent(lowChlorophyll)} · Moderate:{" "}
                {formatPercent(moderateChlorophyll)} · High:{" "}
                {formatPercent(highChlorophyll)}
              </p>
            </div>
          )}

          {hasZoneStats && (
            <div className="overview-group">
              <h4>Management zones</h4>
              <p>
                {dominantZone.name} is the largest zone in the current model output.
                Use the zone map to locate the classified areas.
              </p>
            </div>
          )}

          <p className="summary-disclaimer">
            These results are model outputs and should be interpreted alongside
            field observations. They do not independently confirm actual crop
            health or determine irrigation requirements.
          </p>
        </article>

        <article className="summary-panel inspection-priority">
          <h3>Field Inspection Priority</h3>

          <ol>
            {priorities.map((priority, index) => (
              <li key={`${index}-${priority}`}>{priority}</li>
            ))}
          </ol>
        </article>
      </div>

      <div className="summary-footer">
        <strong>Recommended next step</strong>
        <p>
          Use the water stress, chlorophyll, and management zone maps to locate
          areas for closer inspection. Make crop-management decisions only after
          checking the field conditions.
        </p>
      </div>
    </section>
  );
}

function App() {
  const [result, setResult] = useState(null);
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  return (
    <div className="container">
      <h1>Multispectral Paddy Crop Analysis System</h1>

      <UploadSection
        setResult={setResult}
        setFile={setFile}
        setMessage={setMessage}
      />

      {result?.uploaded_image && (
        <div className="map-card">
          <h3>Uploaded Crop Image</h3>
          <img
            src={getAssetUrl(result.uploaded_image)}
            className="map-img"
            alt="Uploaded multispectral crop preview"
          />
        </div>
      )}

      {result && (
        <h2 className="status">
          {result.crop === "Paddy"
            ? "Uploaded Image is Paddy"
            : "Uploaded image is not Paddy"}
        </h2>
      )}

      {result?.crop === "Paddy" && (
        <ObjectiveSection
          file={file}
          setResult={setResult}
          setMessage={setMessage}
        />
      )}

      {message && <p role="alert" className="app-message">{message}</p>}

      {result?.crop === "Paddy" && (
        <>
          <div className="dashboard">
            <MapCard title="NDVI Map" img={result.ndvi} />
            <MapCard title="NDWI Map" img={result.ndwi} />
            <MapCard title="NDRE Map" img={result.ndre} />
          </div>

          <div className="dashboard">
            {result.maps?.water_stress && (
              <MapCard
                title="Water Stress Map"
                img={result.maps.water_stress}
              />
            )}

            {result.maps?.chlorophyll && (
              <MapCard
                title="Chlorophyll Map"
                img={result.maps.chlorophyll}
              />
            )}

            {result.maps?.zone && (
              <MapCard
                title="Management Zone Map"
                img={result.maps.zone}
              />
            )}
          </div>

          <div className="dashboard">
            {result.water_stress_stats && (
              <StatsCard
                title="Water Stress Statistics"
                data={result.water_stress_stats}
              />
            )}

            {result.chlorophyll_stats && (
              <StatsCard
                title="Chlorophyll Statistics"
                data={result.chlorophyll_stats}
              />
            )}

            {result.zone_stats && (
              <StatsCard
                title="Zone Statistics"
                data={result.zone_stats}
              />
            )}
          </div>

          <OverallAnalysisSummary result={result} />
        </>
      )}
    </div>
  );
}

export default App;
