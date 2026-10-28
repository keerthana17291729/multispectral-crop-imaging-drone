import numpy as np

def chlorophyll_map(NDRE):
    q1 = np.percentile(NDRE, 33)
    q2 = np.percentile(NDRE, 66)
    chlorophyll = np.zeros_like(NDRE)
    chlorophyll[NDRE < q1] = 0
    chlorophyll[(NDRE >= q1) & (NDRE < q2)] = 1
    chlorophyll[NDRE >= q2] = 2
    
    return chlorophyll

def chlorophyll_statistics(NDRE, chl_map):
    total = chl_map.size
    low = np.sum(chl_map == 0)
    moderate = np.sum(chl_map == 1)
    high = np.sum(chl_map == 2)
    stats = {
        "low_chlorophyll_percent": (low / total) * 100,
        "moderate_chlorophyll_percent": (moderate / total) * 100,
        "high_chlorophyll_percent": (high / total) * 100
    }
    chlorophyll_index = float(np.mean(NDRE))

    return stats, chlorophyll_index