import numpy as np

def compute_statistics(stress_map, NDRE, zone_map):

    total = stress_map.size

    high = np.sum(stress_map == 2)
    moderate = np.sum(stress_map == 1)
    low = np.sum(stress_map == 0)

    stress_stats = {

        "high_stress_percent": high/total*100,
        "moderate_stress_percent": moderate/total*100,
        "low_stress_percent": low/total*100
    }

    chlorophyll_index = float(np.mean(NDRE))
    zone_stats = {}

    for z in [0,1,2]:

        zone_pixels = zone_map == z
        zone_stats[f"zone_{z}_percent"] = float(np.sum(zone_pixels)/total*100)

    return stress_stats, chlorophyll_index, zone_stats