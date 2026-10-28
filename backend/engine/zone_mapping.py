import joblib
import numpy as np
from scipy.ndimage import median_filter
from backend.config import KMEANS_MODEL

kmeans = joblib.load(KMEANS_MODEL)


def smooth_index(index):
    return median_filter(index, size=5)


def compute_zones(NDVI, NDRE, NDWI):
    NDVI = smooth_index(NDVI).astype(np.float32, copy=False)
    NDRE = smooth_index(NDRE).astype(np.float32, copy=False)
    NDWI = smooth_index(NDWI).astype(np.float32, copy=False)
    h, w = NDVI.shape
    features = np.stack((NDVI, NDRE, NDWI), axis=-1).reshape(-1, 3)
    clusters = kmeans.predict(features)
    return clusters.reshape(h, w)
