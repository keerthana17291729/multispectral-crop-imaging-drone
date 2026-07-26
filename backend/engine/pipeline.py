import os
import numpy as np

from .raster_loader import load_tiff
from .vegetation_indices import compute_indices
from .crop_classifier import predict_crop
from .water_stress import compute_water_stress
from .chlorophyll import chlorophyll_map, chlorophyll_statistics
from .zone_mapping import compute_zones
from .statistics import compute_statistics

from backend.utils.map_generator import save_map


def compute_zone_features(zone_map, NDVI, NDRE, NDWI):

    zone_features = {}

    for z in [0,1,2]:

        mask = zone_map == z

        if np.sum(mask) == 0:
            continue

        zone_features[f"zone_{z}"] = {

            "mean_ndvi": float(np.mean(NDVI[mask])),
            "mean_ndre": float(np.mean(NDRE[mask])),
            "mean_ndwi": float(np.mean(NDWI[mask]))
        }

    return zone_features


def run_pipeline(file_path, objective):

    image_name = os.path.splitext(os.path.basename(file_path))[0]

    G, RE, R, NIR = load_tiff(file_path)

    NDVI, NDRE, NDWI = compute_indices(G, RE, R, NIR)

    crop = predict_crop(G, RE, R, NIR, NDVI, NDRE, NDWI)

    if crop != "Paddy":
        return {"crop":"Non-Paddy"}

    results = {
        "crop":"Paddy",
        "maps":{}
    }

    # ALWAYS create vegetation index maps

    ndvi_file = save_map(NDVI,"ndvi",image_name)
    ndre_file = save_map(NDRE,"ndre",image_name)
    ndwi_file = save_map(NDWI,"ndwi",image_name)

    results["ndvi"]=f"/maps/{ndvi_file}"
    results["ndre"]=f"/maps/{ndre_file}"
    results["ndwi"]=f"/maps/{ndwi_file}"

    # classification mode stops here
    if objective == "classification":
        return results

    # WATER STRESS

    if objective in ["All","Water Stress"]:

        stress_map = compute_water_stress(NDWI)

        stress_stats,_,_ = compute_statistics(stress_map,NDRE,stress_map)

        stress_file = save_map(stress_map,"water_stress",image_name,stress_stats)

        results["maps"]["water_stress"]=f"/maps/{stress_file}"
        results["water_stress_stats"]=stress_stats

    # CHLOROPHYLL

    if objective in ["All","Chlorophyll"]:

        chl_map = chlorophyll_map(NDRE)

        chl_stats,chl_index = chlorophyll_statistics(NDRE,chl_map)

        chl_file = save_map(chl_map,"chlorophyll",image_name,chl_stats)

        results["maps"]["chlorophyll"]=f"/maps/{chl_file}"
        results["chlorophyll_stats"]=chl_stats
        results["chlorophyll_index"]=chl_index

    # ZONE MAPPING

    if objective in ["All","Zone Mapping"]:

        zone_map = compute_zones(NDVI,NDRE,NDWI)

        _,_,zone_stats = compute_statistics(zone_map,NDRE,zone_map)

        zone_features = compute_zone_features(zone_map,NDVI,NDRE,NDWI)

        zone_stats.update(zone_features)

        zone_file = save_map(zone_map,"zone",image_name,zone_stats)

        results["maps"]["zone"]=f"/maps/{zone_file}"
        results["zone_stats"]=zone_stats

    return results