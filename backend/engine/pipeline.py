import logging
import os
import time
import numpy as np

from .raster_loader import load_tiff
from .vegetation_indices import compute_indices
from .crop_classifier import predict_crop
from .water_stress import compute_water_stress
from .chlorophyll import chlorophyll_map, chlorophyll_statistics
from .zone_mapping import compute_zones
from .statistics import compute_statistics
from backend.utils.map_generator import save_map

logger = logging.getLogger("crop_pipeline")


def compute_zone_features(zone_map, NDVI, NDRE, NDWI):
    zone_features = {}
    for z in [0, 1, 2]:
        mask = zone_map == z
        if np.any(mask):
            zone_features[f"zone_{z}"] = {
                "mean_ndvi": float(np.mean(NDVI[mask])),
                "mean_ndre": float(np.mean(NDRE[mask])),
                "mean_ndwi": float(np.mean(NDWI[mask])),
            }
    return zone_features


def run_pipeline(file_path, objective):
    started = time.perf_counter()
    image_name = os.path.splitext(os.path.basename(file_path))[0]

    stage = time.perf_counter()
    G, RE, R, NIR = load_tiff(file_path, max_dimension=1500)
    logger.info("PIPELINE stage=load_tiff seconds=%.2f shape=%s", time.perf_counter() - stage, G.shape)

    stage = time.perf_counter()
    NDVI, NDRE, NDWI = compute_indices(G, RE, R, NIR)
    logger.info("PIPELINE stage=indices seconds=%.2f", time.perf_counter() - stage)

    stage = time.perf_counter()
    crop = predict_crop(G, RE, R, NIR, NDVI, NDRE, NDWI)
    logger.info("PIPELINE stage=crop_prediction seconds=%.2f crop=%s", time.perf_counter() - stage, crop)
    if crop != "Paddy":
        logger.info("PIPELINE total_seconds=%.2f", time.perf_counter() - started)
        return {"crop": "Non-Paddy"}

    results = {"crop": "Paddy", "maps": {}}

    # Keep the existing frontend response keys, but create dashboard-sized maps.
    stage = time.perf_counter()
    for index_name, index_array in (("ndvi", NDVI), ("ndre", NDRE), ("ndwi", NDWI)):
        filename = save_map(index_array, index_name, image_name)
        results[index_name] = f"/maps/{filename}"
    logger.info("PIPELINE stage=index_maps seconds=%.2f", time.perf_counter() - stage)

    if objective in ["All", "Water Stress"]:
        stage = time.perf_counter()
        stress_map = compute_water_stress(NDWI)
        stress_stats, _, _ = compute_statistics(stress_map, NDRE, stress_map)
        stress_file = save_map(stress_map, "water_stress", image_name, stress_stats)
        results["maps"]["water_stress"] = f"/maps/{stress_file}"
        results["water_stress_stats"] = stress_stats
        logger.info("PIPELINE stage=water_stress seconds=%.2f", time.perf_counter() - stage)

    if objective in ["All", "Chlorophyll"]:
        stage = time.perf_counter()
        chl_map = chlorophyll_map(NDRE)
        chl_stats, chl_index = chlorophyll_statistics(NDRE, chl_map)
        chl_file = save_map(chl_map, "chlorophyll", image_name, chl_stats)
        results["maps"]["chlorophyll"] = f"/maps/{chl_file}"
        results["chlorophyll_stats"] = chl_stats
        results["chlorophyll_index"] = chl_index
        logger.info("PIPELINE stage=chlorophyll seconds=%.2f", time.perf_counter() - stage)

    if objective in ["All", "Zone Mapping"]:
        stage = time.perf_counter()
        zone_map = compute_zones(NDVI, NDRE, NDWI)
        _, _, zone_stats = compute_statistics(zone_map, NDRE, zone_map)
        zone_stats.update(compute_zone_features(zone_map, NDVI, NDRE, NDWI))
        zone_file = save_map(zone_map, "zone", image_name, zone_stats)
        results["maps"]["zone"] = f"/maps/{zone_file}"
        results["zone_stats"] = zone_stats
        logger.info("PIPELINE stage=zone_mapping seconds=%.2f", time.perf_counter() - stage)

    logger.info("PIPELINE total_seconds=%.2f objective=%s", time.perf_counter() - started, objective)
    return results
