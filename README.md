# 🌾 Multispectral Crop Imaging Drone
### AI-Powered Paddy Crop Analysis Using Multispectral UAV Imagery

---

## 📖 Overview

**Multispectral Crop Imaging Drone** is an AI-powered web application that analyzes multispectral drone images of paddy fields to assess crop health, detect water stress, estimate chlorophyll levels, and classify vegetation zones.

The system processes multispectral UAV imagery using vegetation indices such as **NDVI**, **NDRE**, and **NDWI**, combined with machine learning techniques to provide accurate and easy-to-understand crop insights.

---

## ✨ Key Features

- 🌱 Paddy Crop Classification
- 📈 NDVI (Normalized Difference Vegetation Index)
- 🌿 NDRE (Normalized Difference Red Edge Index)
- 💧 NDWI (Normalized Difference Water Index)
- 🚰 Water Stress Detection
- 🍃 Chlorophyll Estimation
- 🗺️ Vegetation Zone Mapping
- 📊 Statistical Analysis Dashboard
- 📉 Interactive Charts
- ⚡ FastAPI REST API
- 💻 Modern React Frontend

---

# 📸 Application Workflow

```
Upload Multispectral Image
            │
            ▼
     Band Extraction
            │
            ▼
 Vegetation Index Calculation
 (NDVI • NDRE • NDWI)
            │
            ▼
 Crop Classification
            │
            ▼
 Health Analysis
            │
            ▼
Generate Maps & Statistics
            │
            ▼
 Display Results on Dashboard
```

---

# 🧠 Technologies Used

## Backend

- Python
- FastAPI
- Rasterio
- NumPy
- OpenCV
- Matplotlib
- Scikit-Learn
- Joblib

## Frontend

- React.js
- Vite
- JavaScript
- Axios
- CSS
- Recharts

---

# 🌱 Vegetation Indices

### NDVI
Measures vegetation health and greenness.

```
NDVI = (NIR - Red) / (NIR + Red)
```

---

### NDRE

Evaluates chlorophyll concentration and plant vigor.

```
NDRE = (NIR - RedEdge) / (NIR + RedEdge)
```

---

### NDWI

Measures crop water content.

```
NDWI = (NIR - Green) / (NIR + Green)
```

---

# 🛰 Input Data

Supported Input

- Multispectral TIFF Images
- Four Spectral Bands

| Band | Description |
|------|-------------|
| Green | Green Band |
| Red Edge | Red Edge Band |
| Red | Red Band |
| NIR | Near Infrared Band |

---

# 📊 Outputs

The system generates

- ✅ NDVI Map
- ✅ NDRE Map
- ✅ NDWI Map
- ✅ Water Stress Map
- ✅ Chlorophyll Map
- ✅ Vegetation Zone Map
- ✅ Crop Classification
- ✅ Water Stress Percentage
- ✅ Chlorophyll Percentage
- ✅ Zone Statistics

---

# 📂 Project Structure

```
multispectral_crop_imaging_drone
│
├── backend
│   ├── engine
│   ├── models
│   ├── outputs
│   ├── utils
│   ├── uploads
│   └── main.py
│
├── frontend
│   ├── src
│   ├── public
│   ├── package.json
│   └── vite.config.js
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# ⚙ Installation

## Clone Repository

```bash
git clone https://github.com/YourUsername/multispectral-crop-imaging-drone.git

cd multispectral-crop-imaging-drone
```

---

## Backend Setup

```bash
python -m venv crop_env

crop_env\Scripts\activate

pip install -r requirements.txt

python -m uvicorn backend.main:app --reload
```

Backend runs on

```
http://127.0.0.1:8000
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend runs on

```
http://localhost:5173
```

---

# 📷 Screenshots

Add screenshots of:

- Home Page
- Upload Page
- NDVI Map
- NDRE Map
- NDWI Map
- Water Stress Map
- Chlorophyll Map
- Zone Map
- Dashboard

---

# 🚀 Future Enhancements

- Multiple Image Analysis
- Time-Series Crop Monitoring
- Yield Prediction
- Disease Detection
- AI-Based Crop Recommendation
- Satellite Image Support
- Mobile Application
- Cloud Deployment

---

# 🎯 Applications

- Precision Agriculture
- Smart Farming
- Crop Monitoring
- Water Resource Management
- Agricultural Research
- Drone-Based Field Inspection

---

# 👨‍💻 Developed By

**Keerthana**

B.Tech – Artificial Intelligence & Data Science

---

# 📜 License

This project is developed for academic and research purposes.

---

## ⭐ If you found this project useful, don't forget to Star this repository!