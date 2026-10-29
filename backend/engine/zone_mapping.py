
import joblib
import numpy as np
from scipy.ndimage import median_filter

from backend.config import KMEANS_MODEL

# Load the trained model once when the backend starts.
kmeans = joblib.load(KMEANS_MODEL)

# Predict a limited number of pixels per batch to reduce peak memory usage.
PREDICTION_BATCH_SIZE = 50_000


def smooth_index(index):
    """Apply median filtering while retaining float32 precision."""
    index = np.asarray(index, dtype=np.float32)

    if index.ndim != 2:
        raise ValueError("Vegetation index arrays must be two-dimensional.")

    return median_filter(index, size=5)


def compute_zones(NDVI, NDRE, NDWI):
    """
    Generate management zones using the existing trained K-means model.

    Feature order: NDVI, NDRE, NDWI.
    Predictions are processed in batches to reduce peak memory usage.
    """
    NDVI = np.asarray(NDVI, dtype=np.float32)
    NDRE = np.asarray(NDRE, dtype=np.float32)
    NDWI = np.asarray(NDWI, dtype=np.float32)

    if NDVI.ndim != 2 or NDRE.ndim != 2 or NDWI.ndim != 2:
        raise ValueError("NDVI, NDRE, and NDWI must be two-dimensional arrays.")

    if NDVI.shape != NDRE.shape or NDVI.shape != NDWI.shape:
        raise ValueError("NDVI, NDRE, and NDWI must have identical shapes.")

    height, width = NDVI.shape
    if height == 0 or width == 0:
        raise ValueError("Vegetation index arrays cannot be empty.")

    if not hasattr(kmeans, "cluster_centers_"):
        raise ValueError("The saved K-means model is not fitted or is invalid.")

    centers = np.asarray(kmeans.cluster_centers_)
    if centers.ndim != 2 or centers.shape[1] != 3:
        raise ValueError(
            "The saved K-means model must have exactly 3 features "
            "in NDVI, NDRE, NDWI order."
        )

    model_dtype = centers.dtype
    if model_dtype not in (np.dtype("float32"), np.dtype("float64")):
        raise ValueError(
            f"Unsupported K-means model dtype: {model_dtype}. "
            "Expected float32 or float64."
        )

    smoothed_ndvi = smooth_index(NDVI)
    smoothed_ndre = smooth_index(NDRE)
    smoothed_ndwi = smooth_index(NDWI)

    ndvi_flat = smoothed_ndvi.reshape(-1)
    ndre_flat = smoothed_ndre.reshape(-1)
    ndwi_flat = smoothed_ndwi.reshape(-1)

    total_pixels = height * width
    clusters = np.empty(total_pixels, dtype=np.int32)

    for start in range(0, total_pixels, PREDICTION_BATCH_SIZE):
        end = min(start + PREDICTION_BATCH_SIZE, total_pixels)

        features = np.empty((end - start, 3), dtype=model_dtype, order="C")
        features[:, 0] = ndvi_flat[start:end]
        features[:, 1] = ndre_flat[start:end]
        features[:, 2] = ndwi_flat[start:end]

        if not np.isfinite(features).all():
            raise ValueError(
                "Vegetation indices contain NaN or infinite values. "
                "Check the input TIFF and vegetation-index calculations."
            )

        clusters[start:end] = kmeans.predict(features)

    return clusters.reshape(height, width)
