
import axios from "axios";

export const API_BASE_URL = (
  import.meta.env.VITE_API_URL ||
  (import.meta.env.DEV
    ? "http://127.0.0.1:8000"
    : "https://multispectral-paddy-api.onrender.com")
).replace(/\/+$/, "");

const API = axios.create({
  baseURL: API_BASE_URL,
  timeout: 300000,
});

export const getAssetUrl = (path) => {
  if (!path) return "";
  if (/^https?:\/\//i.test(path)) return path;
  return `${API_BASE_URL}/${path.replace(/^\/+/, "")}`;
};

const sendAnalysisRequest = async (formData) => {
  try {
    const response = await API.post("/analyze", formData);
    return response.data;
  } catch (error) {
    if (error.code === "ECONNABORTED" || error.code === "ETIMEDOUT") {
      throw new Error(
        "Analysis timed out. Check the Render logs for the request's processing stage."
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
        "No response from the backend. It may be restarting or unavailable. Check Render logs."
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
