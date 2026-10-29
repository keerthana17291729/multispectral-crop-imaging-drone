
import joblib
import numpy as np
from scipy.ndimage import median_filter
from backend.config import KMEANS_MODEL

kmeans = joblib.load(KMEANS_MODEL)


def smooth_index(index):
    """Apply median filtering while preserving the input array's dtype."""
    index = np.asarray(index, dtype=np.float32)
    smoothed = median_filter(index, size=5)
    return np.asarray(smoothed, dtype=np.float32)


def compute_zones(NDVI, NDRE, NDWI):
    """
    Classify each pixel into a vegetation zone using the trained K-Means model.

    The prediction input dtype is matched to the loaded model's cluster centers
    to prevent NumPy/sklearn numeric buffer dtype mismatches.
    """
    NDVI = smooth_index(NDVI)
    NDRE = smooth_index(NDRE)
    NDWI = smooth_index(NDWI)

    if NDVI.ndim != 2 or NDRE.ndim != 2 or NDWI.ndim != 2:
        raise ValueError("NDVI, NDRE, and NDWI must all be two-dimensional arrays.")

    if NDVI.shape != NDRE.shape or NDVI.shape != NDWI.shape:
        raise ValueError("NDVI, NDRE, and NDWI must have identical shapes.")

    h, w = NDVI.shape

    # Build one feature row per pixel: [NDVI, NDRE, NDWI].
    features = np.stack((NDVI, NDRE, NDWI), axis=-1).reshape(-1, 3)

    # Use the numeric dtype of the trained K-Means cluster centers.
    model_dtype = getattr(kmeans.cluster_centers_, "dtype", np.dtype(np.float32))
    features = np.ascontiguousarray(features, dtype=model_dtype)

    if not np.isfinite(features).all():
        raise ValueError(
            "Vegetation indices contain NaN or infinite values; "
            "cannot perform vegetation zone classification."
        )

    clusters = kmeans.predict(features)

    return clusters.reshape(h, w)
