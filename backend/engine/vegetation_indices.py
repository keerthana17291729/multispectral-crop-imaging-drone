import numpy as np

def compute_indices(G, RE, R, NIR):
    eps = 1e-6
    NDVI = (NIR - R) / (NIR + R + eps)
    NDRE = (NIR - RE) / (NIR + RE + eps)
    NDWI = (NIR - G) / (NIR + G + eps)

    return NDVI, NDRE, NDWI