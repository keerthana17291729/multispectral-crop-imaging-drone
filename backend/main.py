from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import shutil
import os

from backend.utils.preview_generator import generate_preview
from backend.engine.pipeline import run_pipeline
from backend.config import UPLOAD_DIR

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/maps", StaticFiles(directory="backend/outputs/maps"), name="maps")
app.mount("/uploads", StaticFiles(directory="backend/outputs/uploads"), name="uploads")


@app.get("/")
def root():
    return {"message": "Crop Imaging Drone API running"}


@app.post("/analyze")
async def analyze_crop(
    file: UploadFile = File(...),
    objectives: str = Form(...)
):

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    filepath = os.path.join(UPLOAD_DIR, file.filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    preview_file = generate_preview(filepath)

    # ---- classification only ----
    if objectives == "classification":

        result = run_pipeline(filepath, "classification")

        result["uploaded_image"] = f"/maps/{preview_file}"

        return result

    # ---- objective analysis ----

    result = run_pipeline(filepath, objectives)

    result["uploaded_image"] = f"/maps/{preview_file}"

    if result["crop"] != "Paddy":

        return JSONResponse({
            "crop": "Non-Paddy",
            "uploaded_image": f"/maps/{preview_file}",
            "message": "Uploaded image is not Paddy"
        })

    return result