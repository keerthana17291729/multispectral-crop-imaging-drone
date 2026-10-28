from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from backend.config import MAP_DIR


def overlay_boundaries(ax, array):
    if array.ndim != 2 or min(array.shape) < 2:
        return
    grad_y, grad_x = np.gradient(array.astype(np.float32, copy=False))
    edge = np.sqrt(grad_y * grad_y + grad_x * grad_x)
    level = float(np.mean(edge))
    if np.isfinite(level):
        ax.contour(edge, levels=[level], colors="black", linewidths=0.5)


def save_map(array, map_type, image_name, stats=None):
    """Save dashboard-sized maps; avoid multi-hundred-megapixel PNGs."""
    MAP_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{Path(image_name).stem}_{map_type}.png"
    path = MAP_DIR / filename

    if map_type == "ndvi":
        cmap, vmin, vmax, title, label = "RdYlGn", -1, 1, "NDVI Map (Vegetation Health)", "NDVI value"
    elif map_type == "ndre":
        cmap, vmin, vmax, title, label = "YlGn", -1, 1, "NDRE Map (Chlorophyll Indicator)", "NDRE value"
    elif map_type == "ndwi":
        cmap, vmin, vmax, title, label = "Blues", -1, 1, "NDWI Map (Water Content)", "NDWI value"
    elif map_type == "water_stress":
        cmap, vmin, vmax, title, label = plt.get_cmap("coolwarm", 3), None, None, "Water Stress Map", "Stress level"
    elif map_type == "chlorophyll":
        cmap, vmin, vmax, title, label = plt.get_cmap("YlGn", 3), None, None, "Chlorophyll Map", "Chlorophyll level"
    elif map_type == "zone":
        cmap, vmin, vmax, title, label = plt.get_cmap("tab10", 3), None, None, "Management Zone Map", "Zone"
    else:
        raise ValueError(f"Unsupported map type: {map_type}")

    arr = np.asarray(array)
    fig, ax = plt.subplots(figsize=(9, 7), constrained_layout=True)
    try:
        im = ax.imshow(arr, cmap=cmap, vmin=vmin, vmax=vmax, interpolation="nearest")
        ax.set_title(title, fontsize=13)
        ax.set_xlabel("Field width (pixels)", fontsize=9)
        ax.set_ylabel("Field height (pixels)", fontsize=9)
        ax.tick_params(axis="both", labelsize=8)
        cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label(label, fontsize=9)
        cbar.ax.tick_params(labelsize=8)

        if map_type in {"water_stress", "chlorophyll", "zone"}:
            cbar.set_ticks([0, 1, 2])
            if map_type == "water_stress":
                cbar.set_ticklabels(["Low", "Moderate", "High"])
            elif map_type == "chlorophyll":
                cbar.set_ticklabels(["Low", "Medium", "High"])
            else:
                cbar.set_ticklabels(["Zone 0", "Zone 1", "Zone 2"])
            overlay_boundaries(ax, arr)

        if stats:
            lines = []
            for key, value in stats.items():
                if isinstance(value, dict):
                    lines.append(f"{key}:")
                    lines.extend(f"  {subkey}: {subvalue:.2f}" for subkey, subvalue in value.items() if isinstance(subvalue, (int, float)))
                elif isinstance(value, (int, float)):
                    lines.append(f"{key}: {value:.2f}")
            if lines:
                ax.text(
                    0.02, 0.98, "\n".join(lines[:12]), transform=ax.transAxes,
                    fontsize=7, va="top", bbox={"boxstyle": "round", "facecolor": "white", "alpha": 0.85}
                )

        # 9x7 inches * 120 DPI = 1080x840 pixels, not hundreds of millions.
        fig.savefig(path, dpi=120)
    finally:
        plt.close(fig)

    return filename
