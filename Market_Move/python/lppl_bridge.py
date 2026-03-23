import sys
import os

# Get Project root directory
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from Instability_engine.main import run_lppl

def compute_lppl_instability(symbol):
    lppl_result = run_lppl(symbol)
    instability_score = lppl_result["criticality"] / 100.0

    return {
        "instability_score": instability_score,
        "t_today": lppl_result["t_today"],
        "t_median":lppl_result["tc_median"],
        "lppl_regime": lppl_result["regime"],
        "tc_distance": lppl_result["tc_median"] - lppl_result["t_today"]
    }


