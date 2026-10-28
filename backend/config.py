from pathlib import Path

# Resolve paths from this file, not from Render's current working directory.
BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BACKEND_DIR.parent
OUTPUT_DIR = BACKEND_DIR / "outputs"
UPLOAD_DIR = OUTPUT_DIR / "uploads"
MAP_DIR = OUTPUT_DIR / "maps"
MODEL_DIR = BACKEND_DIR / "models"

CROP_MODEL = MODEL_DIR / "rf_crop_classifier.pkl"
KMEANS_MODEL = MODEL_DIR / "kmeans_zone.pkl"
CHL_MODEL = MODEL_DIR / "rf_chlorophyll_model.pkl"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
MAP_DIR.mkdir(parents=True, exist_ok=True)
