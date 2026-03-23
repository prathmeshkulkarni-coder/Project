import numpy as np

def lppl(t, A, B, C, tc, m, omega, phi):
    """
    Log-Periodic Power Law (LPPL) equation with safety rails.
    """
    # Safety 1: The model 'breaks' at or after tc. 
    # We must ensure dt is always a small positive number.
    dt = tc - t
    
    # Clip dt so it never becomes 0 or negative (avoiding log(0) and negative powers)
    dt = np.maximum(dt, 1e-5) 
    
    # The Power Law component (Hyperbolic Growth)
    # m should be between 0 and 1 for a valid bubble.
    growth = B * np.power(dt, m)
    
    # The Log-Periodic component (The Oscillations)
    # As dt -> 0, the frequency of the cosine increases to infinity.
    oscillations = B * C * np.power(dt, m) * np.cos(omega * np.log(dt) + phi)
    
    return A + growth + oscillations

def get_lppl_bounds(t_start, t_end):
    """
    Standard professional bounds to prevent the math from 'overfitting'.
    Based on Sornette's research.
    """
    lower = [-np.inf, -np.inf, -1, t_end, 0.1, 6.0, 0]
    upper = [np.inf, 0, 1, t_end + 365, 0.9, 13.0, 2 * np.pi]
    return (lower, upper)