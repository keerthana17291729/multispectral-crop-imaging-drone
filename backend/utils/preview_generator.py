import rasterio
import numpy as np
import matplotlib.pyplot as plt
import os

from backend.config import MAP_DIR


def generate_preview(tiff_path):

    image_name = os.path.splitext(os.path.basename(tiff_path))[0]

    filename = f"{image_name}_preview.png"

    save_path = os.path.join(MAP_DIR, filename)

    # reuse preview if already exists
    if os.path.exists(save_path):
        return filename

    with rasterio.open(tiff_path) as src:

        green = src.read(1).astype(np.float32)
        red = src.read(3).astype(np.float32)
        nir = src.read(4).astype(np.float32)

    def normalize(band):

        band = band - band.min()
        band = band / (band.max() + 1e-6)

        return band

    r = normalize(red)
    g = normalize(green)
    b = normalize(nir)

    rgb = np.dstack((r, g, b))

    plt.figure(figsize=(30,25))

    plt.imshow(rgb)


    plt.title(
        "False Color Composite",
        fontsize=70,
        fontweight="bold",
        pad=50
    )

    plt.axis("off")

    plt.tight_layout()

    plt.savefig(save_path, dpi=500)

    plt.close()

    return filename