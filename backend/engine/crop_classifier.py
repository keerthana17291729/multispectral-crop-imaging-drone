import joblib
import numpy as np
from backend.config import CROP_MODEL

model = joblib.load(CROP_MODEL)


def predict_crop(G, RE, R, NIR, NDVI, NDRE, NDWI):
    features = [
        np.mean(G), np.std(G),
        np.mean(RE), np.std(RE),
        np.mean(R), np.std(R),
        np.mean(NIR), np.std(NIR),
        np.mean(NDVI), np.std(NDVI),
        np.mean(NDRE), np.std(NDRE),
        np.mean(NDWI), np.std(NDWI),
    ]
    pred = model.predict(np.asarray(features, dtype=np.float64).reshape(1, -1))[0]
    return "Paddy" if pred == 1 else "Non-Paddy"
