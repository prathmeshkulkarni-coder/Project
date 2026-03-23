import numpy as np
from ..model.lppl_fit import fit_lppl

def run_rolling_lppl(t, log_prices, min_window=100, max_window=250, step=10):
    t_last = t[-1]
    valid_fits = []
    
    # We want to know how many windows we ACTUALLY checked
    actual_checks = 0
    
    for window_size in range(min_window, max_window, step):
        if len(t) < window_size:
            continue
            
        actual_checks += 1
        t_window = t[-window_size:]
        p_window = log_prices[-window_size:]
        
        fit = fit_lppl(t_window, p_window)
        
        if fit is not None:
            valid_fits.append(fit)
            
    probability = len(valid_fits) / actual_checks if actual_checks > 0 else 0
    
    # Extract tc values carefully (assuming fit is a dict or list)
    # If fit_lppl returns a list [A, B, C, tc, m, omega, phi], use f[3]
    try:
        avg_tc = np.mean([f[3] for f in valid_fits]) if valid_fits else None
    except:
        # If f is a dictionary f['tc']
        avg_tc = np.mean([f['tc'] for f in valid_fits]) if valid_fits else None
    
    return {
        "fits": valid_fits,
        "total_windows": actual_checks,  # Fixed: main.py needs this
        "probability_score": probability, 
        "avg_tc": avg_tc
    }