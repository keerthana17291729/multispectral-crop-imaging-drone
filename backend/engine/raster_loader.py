import rasterio
import numpy as np

def load_tiff(file_path):
    with rasterio.open(file_path) as src:
        if src.count < 4:
            raise ValueError("TIFF must contain at least 4 bands")
        G = src.read(1).astype(np.float32)
        RE = src.read(2).astype(np.float32)
        R = src.read(3).astype(np.float32)
        NIR = src.read(4).astype(np.float32)
    return G, RE, R, NIR