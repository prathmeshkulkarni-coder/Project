import numpy as np 

def calculate_hazard_score(criticality_index, avg_tc, tc_std, t_today, decay_scale=30):
    if criticality_index < 40 or avg_tc is None:
        return 0.0

    delta_t = avg_tc - t_today
    
    # 1. Proximity: If we are past the date, hazard is max (1.0)
    if delta_t <= 0: return 1.0

    # 2. Time Factor: Exponentially grows as we get closer to tc
    time_factor = np.exp(-delta_t / decay_scale)

    # 3. Strength: Normalizes criticality (0.0 to 1.0 range)
    strength_factor = np.clip((criticality_index - 40) / 30, 0, 1)
    
    # 4. Certainty Penalty (THE FIX): 
    # Instead of crushing the signal, we use a softer threshold.
    # If std is 20 days, penalty is ~0.5. If std is 100, penalty is 0.1 (not zero).
    certainty_penalty = 1.0 / (1.0 + (tc_std / 15.0)) 

    # Combine: The hazard rate represents the "instantaneous probability of a crash"
    hazard = strength_factor * time_factor * certainty_penalty

    return round(float(hazard), 3)