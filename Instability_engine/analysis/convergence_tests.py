import numpy as np


def calculate_criticality_index(metrics, probability_score):
    if not metrics:
        return 0.0

    # 1. Check for tc stability (Lower std = Higher confidence)
    # If tc_std is less than 5 days, it's very stable
    tc_stability = np.exp(-metrics["tc_std"] / 5.0) 

    # 2. Check for omega stability 
    omega_stability = np.exp(-metrics["omega_std"] / 1.0)

    # 3. Final Criticality Score (0 to 100)
    # Combines the 'number' of fits with the 'quality' (stability) of fits
    score = (probability_score * 0.5 + tc_stability * 0.25 + omega_stability * 0.25) * 100
    return round(score, 2)