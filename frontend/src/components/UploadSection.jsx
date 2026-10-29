
import { useState } from "react";
import { uploadImage } from "../services/api";

function UploadSection({ setResult, setFile, setMessage }) {
  const [selected, setSelected] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    const nextFile = event.target.files?.[0] || null;
    setSelected(nextFile);
    setMessage("");
  };

  const handleUpload = async () => {
    if (!selected || loading) {
      if (!selected) setMessage("Please select a TIFF or TIF file first.");
      return;
    }

    setLoading(true);
    setMessage("");
    setResult(null);
    setFile(selected);

    try {
      const response = await uploadImage(selected);
      setResult(response);

      if (response.crop !== "Paddy") {
        setMessage(response.message || "The uploaded image was not identified as Paddy.");
      }
    } catch (error) {
      setMessage(error.message || "Image upload or analysis failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-box">
      <h2>Upload 4-Band (Green, RE, Red, NIR) Multispectral Paddy Image</h2>

      <div className="upload-row">
        <input
          className="choose-file"
          type="file"
          accept=".tif,.tiff,image/tiff"
          onChange={handleFileChange}
          disabled={loading}
        />

        <button onClick={handleUpload} disabled={loading || !selected}>
          {loading ? "Processing..." : "Upload"}
        </button>
      </div>
    </div>
  );
}

export default UploadSection;
