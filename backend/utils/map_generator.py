import matplotlib.pyplot as plt
import numpy as np
import os

from backend.config import MAP_DIR


def draw_north_arrow(ax):

    ax.annotate(
        'N',
        xy=(0.95, 0.15),
        xytext=(0.95, 0.05),
        arrowprops=dict(facecolor='black', width=6, headwidth=18),
        ha='center',
        va='center',
        fontsize=40,
        xycoords=ax.transAxes
    )


def draw_scale_bar(ax, pixel_length=350, label="Scale"):

    ax.plot(
        [40, 40 + pixel_length],
        [40, 40],
        color="black",
        linewidth=8
    )

    ax.text(
        40 + pixel_length / 2,
        70,
        label,
        ha="center",
        fontsize=40
    )


def overlay_boundaries(ax, array):

    boundaries = np.gradient(array)

    edge = np.sqrt(boundaries[0] ** 2 + boundaries[1] ** 2)

    ax.contour(edge, levels=[np.mean(edge)], colors="black", linewidths=2)


def save_map(array, map_type, image_name, stats=None):

    filename = f"{image_name}_{map_type}.png"

    path = os.path.join(MAP_DIR, filename)

    if os.path.exists(path):
        return filename

    fig, ax = plt.subplots(figsize=(30,22))

    # ---------------- NDVI ----------------

    if map_type == "ndvi":

        im = ax.imshow(array, cmap="RdYlGn", vmin=-1, vmax=1)

        ax.set_title(
            "NDVI Map (Vegetation Health)",
            fontsize=55,
            pad=40
        )

        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

        cbar.set_label(
            "NDVI Value",
            fontsize=45
        )

        cbar.ax.tick_params(labelsize=40)

    # ---------------- NDRE ----------------

    elif map_type == "ndre":

        im = ax.imshow(array, cmap="YlGn", vmin=-1, vmax=1)

        ax.set_title(
            "NDRE Map (Chlorophyll Indicator)",
            fontsize=55,
            pad=40
        )

        cbar = plt.colorbar(im, ax=ax)

        cbar.set_label(
            "NDRE Value",
            fontsize=45
        )

        cbar.ax.tick_params(labelsize=40)

    # ---------------- NDWI ----------------

    elif map_type == "ndwi":

        im = ax.imshow(array, cmap="Blues", vmin=-1, vmax=1)

        ax.set_title(
            "NDWI Map (Water Content)",
            fontsize=55,
            pad=40
        )

        cbar = plt.colorbar(im, ax=ax)

        cbar.set_label(
            "NDWI Value",
            fontsize=45
        )

        cbar.ax.tick_params(labelsize=40)

    # ---------------- WATER STRESS ----------------

    elif map_type == "water_stress":

        cmap = plt.get_cmap("coolwarm",3)

        im = ax.imshow(array,cmap=cmap)

        ax.set_title(
            "Water Stress Map",
            fontsize=55,
            pad=40
        )

        cbar = plt.colorbar(im,ax=ax,ticks=[0,1,2])

        cbar.ax.set_yticklabels(
        [
        "Low Stress",
        "Moderate Stress",
        "High Stress"
        ],
        fontsize=40
        )

        overlay_boundaries(ax,array)

    # ---------------- CHLOROPHYLL ----------------

    elif map_type == "chlorophyll":

        cmap = plt.get_cmap("YlGn",3)

        im = ax.imshow(array,cmap=cmap)

        ax.set_title(
            "Chlorophyll Map",
            fontsize=55,
            pad=40
        )

        cbar = plt.colorbar(im,ax=ax,ticks=[0,1,2])

        cbar.ax.set_yticklabels(
        [
        "Low",
        "Medium",
        "High"
        ],
        fontsize=40
        )

        overlay_boundaries(ax,array)

    # ---------------- ZONE ----------------

    elif map_type == "zone":

        cmap = plt.get_cmap("tab10",3)

        im = ax.imshow(array,cmap=cmap)

        ax.set_title(
            "Management Zone Map",
            fontsize=55,
            pad=40
        )

        cbar = plt.colorbar(im,ax=ax,ticks=[0,1,2])

        cbar.ax.set_yticklabels(
        [
        "Zone 0",
        "Zone 1",
        "Zone 2"
        ],
        fontsize=40
        )

        overlay_boundaries(ax,array)

    # ---------------- COMMON LABELS ----------------

    ax.set_xlabel(
        "Field Width (pixels)",
        fontsize=50,
        labelpad=30
    )

    ax.set_ylabel(
        "Field Height (pixels)",
        fontsize=50,
        labelpad=30
    )

    ax.tick_params(
        axis='both',
        labelsize=40
    )

    # ---------------- MAP ELEMENTS ----------------

    draw_north_arrow(ax)

    draw_scale_bar(ax)

    # ---------------- STATISTICS ----------------

    if stats:

        lines=[]

        for k,v in stats.items():

            if isinstance(v,dict):

                lines.append(f"{k}:")

                for sk,sv in v.items():
                    lines.append(f"  {sk}: {sv:.3f}")

            else:
                lines.append(f"{k}: {v:.3f}")

        text="\n".join(lines)

        ax.text(
        0.02,
        0.98,
        text,
        transform=ax.transAxes,
        fontsize=40,
        verticalalignment="top",
        bbox=dict(
            boxstyle="round",
            facecolor="white",
            alpha=0.9
        )
        )

    plt.tight_layout(rect=[0.05,0.05,0.95,0.95])

    plt.savefig(path,dpi=700)

    plt.close()

    return filename