import numpy as np
from scipy.optimize import differential_evolution
from ..model.lppl_equation import lppl
from ..model.lppl_constraints import validate_lppl_params

# 1. MOVE THIS OUTSIDE (Must be at top level for Mithril Parallelism)
def lppl_cost(params, t, log_prices):
    try:
        model_values = lppl(t, *params)
        if np.any(np.isnan(model_values)) or np.any(np.isinf(model_values)):
            return 1e12
        return np.sum((log_prices - model_values) ** 2)
    except Exception:
        return 1e12

def fit_lppl(t, log_prices):
    t_end = t[-1]
    a_ref = log_prices[-1]
    
    # Mithril Bounds [A, B, C, tc, m, omega, phi]
    bounds = [
        (a_ref - 5, a_ref + 5), 
        (-20.0, -0.001),         
        (-0.99, 0.99),           
        (t_end + 0.1, t_end + 300), 
        (0.01, 0.99),             
        (6.0, 13.0),            
        (0, 2 * np.pi)          
    ]

    # 2. USE 'args' TO PASS DATA TO THE COST FUNCTION
    result = differential_evolution(
        lppl_cost, 
        bounds, 
        args=(t, log_prices),  # <--- Mithril data injection
        strategy='best1bin',
        popsize=10, 
        mutation=(0.5, 1.0), 
        recombination=0.7, 
        tol=0.01, 
        polish=True,
        workers=1,             # Fix for Streamlit Auto-Stopping
        updating='immediate'   # Changed back to immediate since we are not using multiprocessing anymore
    )

    if result.success:
        keys = ["A", "B", "C", "tc", "m", "omega", "phi"]
        params_dict = dict(zip(keys, result.x))
        if validate_lppl_params(params_dict, t_end):
            return params_dict
            
    return None