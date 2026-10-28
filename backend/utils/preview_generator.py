from pathlib import Path
import numpy as np
import rasterio
from rasterio.enums import Resampling
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from backend.config import MAP_DIR


def _normalize(band):
    band = np.asarray(band, dtype=np.float32)
    finite = np.isfinite(band)
    if not finite.any():
        return np.zeros(band.shape, dtype=np.float32)
    low = float(np.nanpercentile(band[finite], 2))
    high = float(np.nanpercentile(band[finite], 98))
    if high <= low:
        return np.zeros(band.shape, dtype=np.float32)
    return np.clip((band - low) / (high - low), 0.0, 1.0)


def generate_preview(tiff_path, max_dimension=1000):
    """Create a small false-colour preview without loading full-size bands."""
    tiff_path = Path(tiff_path)
    filename = f"{tiff_path.stem}_preview.png"
    save_path = MAP_DIR / filename
    MAP_DIR.mkdir(parents=True, exist_ok=True)

    with rasterio.open(tiff_path) as src:
        if src.count < 4:
            raise ValueError(
                f"TIFF must contain at least 4 bands; this file has {src.count}."
            )
        scale = min(1.0, float(max_dimension) / max(src.width, src.height))
        out_width = max(1, int(round(src.width * scale)))
        out_height = max(1, int(round(src.height * scale)))
        # False-colour composite: R=red band, G=green band, B=NIR band.
        red, green, nir = src.read(
            indexes=[3, 1, 4],
            out_shape=(3, out_height, out_width),
            resampling=Resampling.average if scale < 1.0 else Resampling.nearest,
        )

    rgb = np.dstack((_normalize(red), _normalize(green), _normalize(nir)))
    # imsave writes at the array's dimensions; it avoids a huge Matplotlib canvas.
    plt.imsave(save_path, np.clip(rgb, 0.0, 1.0))
    return filename
