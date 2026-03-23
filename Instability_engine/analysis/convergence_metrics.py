import numpy as np

def lppl_convergence_metrics(fits):
    if not fits or len(fits) < 3: # Need at least 3 for meaningful dispersion
        return None

    # Use lists for robust extraction
    tc_vals = np.array([f["tc"] for f in fits])
    omega_vals = np.array([f["omega"] for f in fits])
    m_vals = np.array([f["m"] for f in fits])

    # 1. Outlier Rejection: Calculate Median and Filter
    # We ignore fits that are mathematically 'impossible' compared to the group
    q1, q3 = np.percentile(tc_vals, [25, 75])
    iqr = q3 - q1
    filter_mask = (tc_vals >= q1 - 1.5 * iqr) & (tc_vals <= q3 + 1.5 * iqr)
    
    clean_tc = tc_vals[filter_mask]
    if len(clean_tc) < 2: return None

    return {
        "tc_median": np.median(clean_tc),
        "tc_std": np.std(clean_tc),
        "tc_range": np.ptp(clean_tc), # Peak-to-peak (Max - Min)
        "omega_std": np.std(omega_vals[filter_mask]),
        "m_std": np.std(m_vals[filter_mask]),
        "n_fits": len(clean_tc),
        # Convergence Ratio: How many fits survived the outlier filter?
        "stability_ratio": len(clean_tc) / len(fits) 
    }