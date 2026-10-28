
import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || (
  import.meta.env.DEV
    ? "http://127.0.0.1:8000"
    : "https://multispectral-paddy-api.onrender.com"
);

const API = axios.create({
  baseURL: API_BASE_URL,
  timeout: 300000,
});

const sendAnalysisRequest = async (formData) => {
  try {
    const response = await API.post("/analyze", formData);
    return response.data;
  } catch (error) {
    if (error.code === "ECONNABORTED" || error.code === "ETIMEDOUT") {
      throw new Error(
        "Analysis timed out after 5 minutes. Check the Render logs for the actual backend error."
      );
    }

    if (error.response) {
      const detail = error.response.data?.detail;

      throw new Error(
        typeof detail === "string"
          ? detail
          : `Backend returned HTTP ${error.response.status}.`
      );
    }

    if (error.request) {
      throw new Error(
        `No response from ${API_BASE_URL}. Check whether the Render backend is running and inspect its logs.`
      );
    }

    throw new Error(error.message || "Unexpected API error.");
  }
};

export const uploadImage = async (file) => {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("objectives", "classification");

  return sendAnalysisRequest(formData);
};

export const analyzeObjectives = async (file, objective) => {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("objectives", objective);

  return sendAnalysisRequest(formData);
};

export default API;
