# 🌾 Multispectral Paddy Crop Analysis System
### AI-Powered Paddy Crop Analysis Using Multispectral UAV Imagery

An AI-powered web application for analyzing multispectral drone imagery of paddy fields to support crop classification, vegetation health assessment, water stress analysis, chlorophyll estimation, and vegetation zone mapping.

## 🔗 Live Demo & Project Links

| Resource | Link |
|---|---|
| 🌐 **Live Frontend** | https://multispectral-crop-imaging-drone.vercel.app/ |
| ⚙️ **Backend API** | https://multispectral-paddy-api.onrender.com |
| 📘 **API Documentation (Swagger UI)** | https://multispectral-paddy-api.onrender.com/docs |
| 💻 **GitHub Repository** | https://github.com/keerthana17291729/multispectral-crop-imaging-drone |

> **Note:** The frontend is hosted on Vercel, and the backend API is hosted on Render. The backend runs on a free instance, so the first request after inactivity may take longer to respond.

---

## 📖 Overview

The **Multispectral Paddy Crop Analysis System** processes multispectral UAV (Unmanned Aerial Vehicle) imagery to extract spectral information and generate crop-related insights.

The application uses vegetation indices such as NDVI, NDRE, and NDWI, along with machine learning models and image-processing techniques, to analyze vegetation characteristics and visualize the results through a web dashboard.

Users can upload a multispectral TIFF image, classify the crop, and view the generated maps and analysis results supported by the selected objective.

## ✨ Key Features

- 🌱 Paddy crop classification
- 📈 NDVI — Normalized Difference Vegetation Index
- 🌿 NDRE — Normalized Difference Red Edge Index
- 💧 NDWI — Normalized Difference Water Index
- 🚰 Water stress analysis
- 🍃 Chlorophyll estimation
- 🗺️ Vegetation zone mapping
- 📊 Statistical analysis and crop insights
- 🖼️ Multispectral TIFF upload and preview
- ⚙️ REST API built with FastAPI
- 💻 Interactive web interface built with React.js
- ☁️ Cloud deployment using Render and Vercel

## 🔄 Application Workflow

```text
Upload Multispectral TIFF Image
             |
             v
      Load Spectral Bands
             |
             v
  Calculate Vegetation Indices
       NDVI | NDRE | NDWI
             |
             v
      Crop Classification
             |
             v
    Crop Health Analysis
             |
             v
 Generate Maps and Statistics
             |
             v
 Display Results on Dashboard
```

## 🧠 Technologies Used

### Backend

- Python
- FastAPI
- Rasterio
- NumPy
- Matplotlib
- Scikit-learn
- Joblib
- OpenCV (where used by the processing pipeline)

### Frontend

- React.js
- Vite
- JavaScript
- Axios
- HTML5
- CSS3

### Machine Learning and Image Processing

- Random Forest classification
- K-Means clustering for vegetation zone analysis
- Multispectral raster processing
- Vegetation index calculation
- Image visualization and statistical analysis

### Deployment

- **Frontend:** Vercel
- **Backend:** Render
- **Version Control:** Git and GitHub

## 🌱 Vegetation Indices

### 1. NDVI — Normalized Difference Vegetation Index

NDVI is commonly used to assess vegetation greenness and vegetation conditions.

Formula:

\[
NDVI = \frac{NIR - Red}{NIR + Red}
\]

### 2. NDRE — Normalized Difference Red Edge Index

NDRE uses near-infrared and red-edge reflectance to assess vegetation characteristics associated with chlorophyll and plant vigor.

Formula:

\[
NDRE = \frac{NIR - RedEdge}{NIR + RedEdge}
\]

### 3. NDWI — Normalized Difference Water Index

This project uses the NIR–Green formulation to analyze water-related characteristics in vegetation and agricultural imagery.

Formula:

\[
NDWI = \frac{NIR - Green}{NIR + Green}
\]

**Note:** NDWI has multiple formulations. The formula above specifically refers to the NIR–Green version.

## 🛰️ Input Data

The application accepts supported multispectral TIFF (`.tif` or `.tiff`) imagery.

The expected four spectral bands are:

| Band | Description |
|---|---|
| Green | Green spectral reflectance |
| Red | Red spectral reflectance |
| Red Edge | Red-edge spectral reflectance |
| NIR | Near-infrared spectral reflectance |

The input image must contain the expected bands in the order and format supported by the backend processing pipeline.

## 📊 Analysis Outputs

Depending on the selected analysis objective and successful processing, the application can generate:

- NDVI map
- NDRE map
- NDWI map
- Water stress analysis
- Chlorophyll estimation
- Vegetation zone map
- Crop classification result
- Statistical summaries and zone-level information

The availability of individual outputs depends on the implemented pipeline and selected objective.

## 🏗️ Project Structure

```text
multispectral-crop-imaging-drone/
│
├── backend/
│   ├── engine/
│   │   ├── chlorophyll.py
│   │   ├── crop_classifier.py
│   │   ├── pipeline.py
│   │   ├── raster_loader.py
│   │   ├── statistics.py
│   │   ├── vegetation_indices.py
│   │   ├── water_stress.py
│   │   └── zone_mapping.py
│   │
│   ├── models/
│   │   ├── kmeans_zone.pkl
│   │   ├── rf_chlorophyll_model.pkl
│   │   └── rf_crop_classifier.pkl
│   │
│   ├── outputs/
│   │   ├── maps/
│   │   └── uploads/
│   │
│   ├── utils/
│   │   ├── map_generator.py
│   │   └── preview_generator.py
│   │
│   ├── config.py
│   └── main.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── styles/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
├── requirements.txt
├── README.md
└── .gitignore
```

*Generated output files and local environment files may differ depending on the deployment configuration.*

## ⚙️ Installation and Local Setup

### Prerequisites

- Python installed
- Node.js and npm installed
- Git installed

### 1. Clone the Repository

```bash
git clone https://github.com/keerthana17291729/multispectral-crop-imaging-drone.git
cd multispectral-crop-imaging-drone
```

### 2. Backend Setup

Create a virtual environment:

**Windows:**

```bash
python -m venv crop_env
crop_env\Scripts\activate
```

Install the backend dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI server from the repository root:

```bash
python -m uvicorn backend.main:app --reload
```

The backend API will be available at:

- API: http://127.0.0.1:8000
- Swagger documentation: http://127.0.0.1:8000/docs

### 3. Frontend Setup

Open a new terminal and navigate to the frontend directory:

```bash
cd frontend
npm install
npm run dev
```

The Vite development server will display the local frontend URL, normally:

http://localhost:5173

**Configuration:** The deployed frontend uses the Render backend URL. If you change the API URL or run the application locally, configure the frontend API base URL accordingly.

## 🚀 Deployment Architecture

```text
                 User / Browser
                       |
                       v
              React Frontend
                  (Vercel)
                       |
                       v
               FastAPI REST API
                  (Render)
                       |
                       v
        TIFF Processing and ML Models
                       |
                       v
             Generated Maps / Results
                       |
                       v
               Results Dashboard
```

### Frontend Deployment

The React application is deployed on Vercel.

Live URL: https://multispectral-crop-imaging-drone.vercel.app/

### Backend Deployment

The FastAPI application is deployed on Render.

API URL: https://multispectral-paddy-api.onrender.com

Interactive API documentation: https://multispectral-paddy-api.onrender.com/docs

**Deployment considerations:** Render's free instance may spin down after inactivity, and its local filesystem is not persistent. Uploaded TIFF files and generated maps should not be treated as permanently stored data.

## 📸 Application Screenshots

Add screenshots of the following sections to showcase the application's interface:

- Main dashboard
- TIFF image upload
- Uploaded image preview
- NDVI map
- NDRE map
- NDWI map
- Water stress analysis
- Chlorophyll estimation
- Vegetation zone map
- Statistical results

Example:

```markdown
![Application Dashboard](screenshots/dashboard.png)
![NDVI Map](screenshots/ndvi-map.png)
![NDRE Map](screenshots/ndre-map.png)
![NDWI Map](screenshots/ndwi-map.png)
```

Create a `screenshots/` directory in the repository and add the corresponding image files before using these examples.

## 🔮 Future Enhancements

- Multi-image and batch analysis
- Time-series crop monitoring
- Crop yield prediction
- Crop disease detection
- AI-based crop recommendations
- Satellite imagery support
- Historical analysis and report export
- Persistent cloud storage for uploaded images and generated maps
- Mobile-friendly crop monitoring interface

## 🎯 Applications

- Precision agriculture
- Smart farming
- Crop health monitoring
- Agricultural water management
- UAV-based field inspection
- Agricultural research and decision support

## 👩‍💻 Developed By

**Keerthana**  
B.Tech — Artificial Intelligence and Data Science

GitHub: https://github.com/keerthana17291729

## 📜 License

This project was developed for academic and research purposes. No explicit open-source license is specified in this repository unless a license file is added.

---

⭐ If you find this project interesting, consider starring the repository!

**Live Demo:** https://multispectral-crop-imaging-drone.vercel.app/  
**API Documentation:** https://multispectral-paddy-api.onrender.com/docs
