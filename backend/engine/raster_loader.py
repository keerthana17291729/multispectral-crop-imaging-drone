import rasterio
import numpy as np
from rasterio.enums import Resampling


def load_tiff(file_path, max_dimension=1500):
    """Load the first four bands at a bounded display/analysis resolution.

    The deployed API must not expand a large compressed TIFF into several full-size
    float arrays. This resamples large rasters to at most max_dimension pixels on
    their longest side. Output maps are consequently analysis previews, not full-
    resolution scientific exports.
    """
    with rasterio.open(file_path) as src:
        if src.count < 4:
            raise ValueError(
                f"TIFF must contain at least 4 bands; this file has {src.count}."
            )
        if src.width <= 0 or src.height <= 0:
            raise ValueError("TIFF has invalid image dimensions.")

        scale = min(1.0, float(max_dimension) / max(src.width, src.height))
        out_width = max(1, int(round(src.width * scale)))
        out_height = max(1, int(round(src.height * scale)))
        bands = src.read(
            indexes=[1, 2, 3, 4],
            out_shape=(4, out_height, out_width),
            resampling=Resampling.average if scale < 1.0 else Resampling.nearest,
            masked=False,
        ).astype(np.float32, copy=False)

    # Band order expected by the existing project: Green, Red Edge, Red, NIR.
    return bands[0], bands[1], bands[2], bands[3]
