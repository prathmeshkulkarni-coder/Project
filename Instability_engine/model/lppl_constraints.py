# model/lppl_constraints.py

def validate_lppl_params(params, t_last):
    """
    Enforces hard LPPL constraints.
    
    params: dict with keys
        A, B, C, tc, m, omega, phi
    t_last: last time index in the fitting window
    
    Returns:
        True  -> valid critical regime
        False -> reject fit
    """

    A = params["A"]
    B = params["B"]
    C = params["C"]
    tc = params["tc"]
    m = params["m"]
    omega = params["omega"]

    # Constraint 1: Power-law exponent
    if not (0 < m < 1):
        return False

    # Constraint 2: Bubble condition
    if B >= 0:
        return False

    # Constraint 3: Log-periodic frequency
    if not (6 <= omega <= 13):
        return False

    # Constraint 4: Critical time must be in the future
    if tc <= t_last:
        return False

    # Constraint 5: Oscillation amplitude sanity
    if abs(C) >= 1:
        return False
    # Constraint 6: Damping Condition (Positivity of the Hazard Rate)
    # This ensures the oscillations don't "overpower" the trend.
    damping = m / (omega * abs(C) + 1e-9)
    if damping < 0.5:
        return False

    return True
