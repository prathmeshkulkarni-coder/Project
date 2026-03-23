import pandas as pd
from .data.input.db_data import read_prices_for_lppl
from .analysis.rolling_windows import run_rolling_lppl
from .analysis.convergence_metrics import lppl_convergence_metrics
from .analysis.convergence_tests import calculate_criticality_index
from .analysis.hazard_score import calculate_hazard_score
from .analysis.regime_classifier import classify_lppl_regime

import datetime
import os


def run_lppl(symbol: str):
    df = read_prices_for_lppl(symbol)
    if df is None or len(df) < 120:
        raise ValueError("Not enough data for LPPL")

    t = df["t"].values
    log_prices = df["log_price"].values
    t_today = t[-1]

    lppl_result = run_rolling_lppl(t, log_prices)

    metrics = lppl_convergence_metrics(lppl_result["fits"])

    criticality = calculate_criticality_index(
        metrics,
        lppl_result["probability_score"]
    )

    avg_tc = metrics["tc_median"] if metrics else None

    hazard = calculate_hazard_score(
        criticality_index=criticality,
        avg_tc=avg_tc,
        tc_std=metrics["tc_std"] if metrics else None,
        t_today=t_today
    )

    regime = classify_lppl_regime(criticality)

    output = {
        "symbol": symbol,
        "t_today": int(t_today),
        "criticality": float(criticality),
        "hazard": float(hazard),
        "regime": regime,
        "tc_median": float(avg_tc) if avg_tc else None,
        "n_fits": metrics["n_fits"] if metrics else 0
    }
    print("DEBUG LAST DATE:", df["date"].iloc[-1])
    print("DEBUG ROW COUNT:", len(df))
    print("DEBUG MAX T:", df["t"].max())
    return output


def main():
    symbol = "SI=F"
    output = run_lppl(symbol)

    print("\n--- FINAL SIGNAL ---")
    print(output)


if __name__ == "__main__":
    main()
