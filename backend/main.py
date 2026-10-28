
from pathlib import Path
import os
import shutil

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from backend.utils.preview_generator import generate_preview
from backend.engine.pipeline import run_pipeline
from backend.config import UPLOAD_DIR

# --------------------------------------------------
# DIRECTORIES
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
MAPS_DIR = BASE_DIR / "outputs" / "maps"
UPLOADS_DIR = BASE_DIR / "outputs" / "uploads"

MAPS_DIR.mkdir(parents=True, exist_ok=True)
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# FASTAPI APPLICATION
# --------------------------------------------------
app = FastAPI(
    title="Multispectral Crop Imaging Drone API",
    description="API for multispectral crop image analysis",
    version="1.0.0",
)

# --------------------------------------------------
# CORS
# --------------------------------------------------
allowed_origins = [
    "http://localhost:5173",
    "https://multispectral-crop-imaging-drone.vercel.app",
]

vercel_url = os.getenv("FRONTEND_URL")
if vercel_url:
    normalized_url = vercel_url.rstrip("/")
    if normalized_url not in allowed_origins:
        allowed_origins.append(normalized_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# STATIC FILES
# --------------------------------------------------
app.mount(
    "/maps",
    StaticFiles(directory=str(MAPS_DIR)),
    name="maps",
)

app.mount(
    "/uploads",
    StaticFiles(directory=str(UPLOADS_DIR)),
    name="uploads",
)

# --------------------------------------------------
# ROOT
# --------------------------------------------------
@app.get("/")
def root():
    return {
        "message": "Crop Imaging Drone API running",
        "status": "healthy",
    }

# --------------------------------------------------
# ANALYZE CROP
# --------------------------------------------------
@app.post("/analyze")
async def analyze_crop(
    file: UploadFile = File(...),
    objectives: str = Form(...),
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No filename provided.",
        )

    safe_filename = Path(file.filename).name

    if not safe_filename.lower().endswith((".tif", ".tiff")):
        raise HTTPException(
            status_code=400,
            detail="Please upload a TIFF or TIF multispectral image.",
        )

    upload_dir = Path(UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)
    filepath = upload_dir / safe_filename

    try:
        with filepath.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        preview_file = generate_preview(str(filepath))

        if objectives == "classification":
            result = run_pipeline(str(filepath), "classification")
        else:
            result = run_pipeline(str(filepath), objectives)

        if not isinstance(result, dict):
            raise HTTPException(
                status_code=500,
                detail="The analysis pipeline returned an invalid result.",
            )

        result["uploaded_image"] = f"/maps/{Path(preview_file).name}"

        if result.get("crop") != "Paddy":
            return JSONResponse(
                content={
                    "crop": "Non-Paddy",
                    "uploaded_image": f"/maps/{Path(preview_file).name}",
                    "message": "Uploaded image is not Paddy.",
                }
            )

        return result

    except HTTPException:
        raise
    except Exception as exc:
        print(f"Crop analysis failed: {type(exc).__name__}: {exc}")
        raise HTTPException(
            status_code=500,
            detail=f"Crop analysis failed: {type(exc).__name__}: {exc}",
        ) from exc
    finally:
        await file.close()
