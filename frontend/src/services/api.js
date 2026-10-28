
import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL
  || (import.meta.env.DEV
    ? "http://127.0.0.1:8000"
    : "https://multispectral-paddy-api.onrender.com");

const API = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000,
});

export const uploadImage = async (file) => {
  const form = new FormData();
  form.append("file", file);
  form.append("objectives", "classification");

  const response = await API.post("/analyze", form);
  return response.data;
};

export const analyzeObjectives = async (file, obj) => {
  const form = new FormData();
  form.append("file", file);
  form.append("objectives", obj);

  const response = await API.post("/analyze", form);
  return response.data;
};

export default API;
