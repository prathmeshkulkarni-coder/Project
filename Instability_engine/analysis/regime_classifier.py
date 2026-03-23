from ..analysis.convergence_metrics import lppl_convergence_metrics

def classify_lppl_regime(criticality_index):
    """
    Final regime classifier.
    Input: criticality_index (0–100)
    """

    if criticality_index >= 70:
        return "CRITICAL"
    elif criticality_index >= 40:
        return "WARNING"
    else:
        return "NORMAL"
