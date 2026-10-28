import numpy as np
import joblib

model = joblib.load("backend/models/rf_crop_classifier.pkl")

def predict_crop(G, RE, R, NIR, NDVI, NDRE, NDWI):
    features = [
        np.mean(G), np.std(G),
        np.mean(RE), np.std(RE),
        np.mean(R), np.std(R),
        np.mean(NIR), np.std(NIR),
        np.mean(NDVI), np.std(NDVI),
        np.mean(NDRE), np.std(NDRE),
        np.mean(NDWI), np.std(NDWI)
    ]
    features = np.array(features).reshape(1,-1)
    pred = model.predict(features)[0]

    if pred == 1:
        return "Paddy"
    else:
        return "Non-Paddy"