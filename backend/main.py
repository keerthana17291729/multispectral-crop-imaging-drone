from pathlib import Path
import logging
import shutil
import time
import uuid

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from backend.utils.preview_generator import generate_preview
from backend.engine.pipeline import run_pipeline
from backend.config import UPLOAD_DIR, MAP_DIR

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("crop_api")

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
MAP_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="Multispectral Crop Imaging Drone API",
    description="API for multispectral crop image analysis",
    version="1.1.0",
)

allowed_origins = [
    "http://localhost:5173",
    "https://multispectral-crop-imaging-drone.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/maps", StaticFiles(directory=str(MAP_DIR)), name="maps")
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")


@app.get("/")
def root():
    return {"message": "Crop Imaging Drone API running", "status": "healthy"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/analyze")
async def analyze_crop(
    file: UploadFile = File(...),
    objectives: str = Form(...),
):
    request_id = uuid.uuid4().hex[:10]
    started = time.perf_counter()
    filepath = None

    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided.")

    safe_filename = Path(file.filename).name
    if not safe_filename.lower().endswith((".tif", ".tiff")):
        raise HTTPException(status_code=400, detail="Please upload a TIFF or TIF multispectral image.")

    # Unique filenames prevent simultaneous uploads with the same original name
    # from overwriting each other's input or generated output.
    unique_stem = f"{Path(safe_filename).stem}_{request_id}"
    filepath = UPLOAD_DIR / f"{unique_stem}{Path(safe_filename).suffix.lower()}"

    try:
        logger.info("ANALYZE id=%s started filename=%s objective=%s", request_id, safe_filename, objectives)
        stage = time.perf_counter()
        with filepath.open("wb") as destination:
            shutil.copyfileobj(file.file, destination, length=1024 * 1024)
        logger.info(
            "ANALYZE id=%s stage=upload_saved seconds=%.2f bytes=%s",
            request_id, time.perf_counter() - stage, filepath.stat().st_size,
        )

        stage = time.perf_counter()
        preview_file = generate_preview(str(filepath), max_dimension=1000)
        logger.info("ANALYZE id=%s stage=preview seconds=%.2f", request_id, time.perf_counter() - stage)

        result = run_pipeline(str(filepath), objectives)
        if not isinstance(result, dict):
            raise HTTPException(status_code=500, detail="The analysis pipeline returned an invalid result.")

        result["uploaded_image"] = f"/maps/{preview_file}"
        result["request_id"] = request_id

        if result.get("crop") != "Paddy":
            result = {
                "crop": "Non-Paddy",
                "uploaded_image": f"/maps/{preview_file}",
                "message": "Uploaded image is not Paddy.",
                "request_id": request_id,
            }

        logger.info("ANALYZE id=%s completed seconds=%.2f", request_id, time.perf_counter() - started)
        return JSONResponse(content=result)

    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("ANALYZE id=%s failed after %.2f seconds", request_id, time.perf_counter() - started)
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed ({type(exc).__name__}). Reference request_id={request_id} in Render logs.",
        ) from exc
    finally:
        await file.close()
        # Do not delete the preview/maps; the frontend uses them after response.
