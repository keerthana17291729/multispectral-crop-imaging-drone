
import { useState } from "react";
import { analyzeObjectives } from "../services/api";

const objectives = [
  "All",
  "Health",
  "Water Stress",
  "Chlorophyll"
];

function ObjectiveSection({ file, setResult, setMessage }) {
  const [selected, setSelected] = useState("All");
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!file || loading) {
      if (!file) {
        setMessage("Please upload an image first.");
      }
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      const response = await analyzeObjectives(file, selected);
      setResult(response);
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
