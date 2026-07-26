import numpy as np

def compute_water_stress(NDWI):

    q1 = np.percentile(NDWI, 25)
    q3 = np.percentile(NDWI, 75)

    stress_map = np.zeros_like(NDWI)

    stress_map[NDWI < q1] = 2
    stress_map[(NDWI >= q1) & (NDWI < q3)] = 1
    stress_map[NDWI >= q3] = 0

    return stress_map