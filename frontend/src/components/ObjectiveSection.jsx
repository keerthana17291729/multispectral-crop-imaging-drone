
import { useState } from "react";
import { analyzeObjectives } from "../services/api";

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
];

function ObjectiveSection({ file, setResult, setMessage }) {
  const [selected, setSelected] = useState("All");
  const [loading, setLoading] = useState(false);

  const notImplemented = [
    "Health",
    "Disease Detection",
    "Disease Localization",
    "Growth Monitoring",
    "Yield Estimation",
    "Disease Prediction"
  ];

  const handleAnalyze = async () => {
    if (!file || loading) {
      if (!file) setMessage("Please upload an image first.");
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      const objective = notImplemented.includes(selected)
        ? "classification"
        : selected;

      const response = await analyzeObjectives(file, objective);
      setResult(response);

      if (notImplemented.includes(selected)) {
        setMessage(
          `${selected} is not implemented yet. The image was classified again instead.`
        );
      }
    } catch (error) {
      setMessage(error.message || "Analysis failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="objective-box">
      <select
        className="objective-select"
        value={selected}
        onChange={(event) => setSelected(event.target.value)}
        disabled={loading}
      >
        {objectives.map((objective) => (
          <option key={objective} value={objective}>
            {objective}
          </option>
        ))}
      </select>

      <button onClick={handleAnalyze} disabled={loading || !file}>
        {loading ? "Processing..." : "Analyze"}
      </button>
    </div>
  );
}

export default ObjectiveSection;
