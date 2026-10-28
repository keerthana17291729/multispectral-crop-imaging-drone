import numpy as np
import joblib
from scipy.ndimage import median_filter
kmeans = joblib.load("backend/models/kmeans_zone.pkl")
def smooth_index(index):
    # 5x5 spatial smoothing
    smoothed = median_filter(index, size=5)
    return smoothed

def compute_zones(NDVI, NDRE, NDWI):
    # -------- SMOOTH INDICES --------
    NDVI = smooth_index(NDVI)
    NDRE = smooth_index(NDRE)
    NDWI = smooth_index(NDWI)
    # convert dtype
    NDVI = NDVI.astype(np.float64)
    NDRE = NDRE.astype(np.float64)
    NDWI = NDWI.astype(np.float64)
    h, w = NDVI.shape
    features = np.stack(
        (NDVI, NDRE, NDWI),
        axis=-1
    )
    pixels = features.reshape(-1, 3)
    pixels = pixels.astype(np.float64)
    clusters = kmeans.predict(pixels)
    zone_map = clusters.reshape(h, w)
    return zone_map