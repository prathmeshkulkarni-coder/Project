import pandas as pd
import numpy as np


def false_positive_analysis(
    price_df,
    regime_df,
    horizon=20,
    drawdown_threshold=-0.05
):
    """
    Measures how often LPPL CRITICAL signals are followed by
    NO increase in risk (false positives).
    
    price_df  : [date, adj_close]
    regime_df : [date, regime]
    """

    # Prepare price data
    df = price_df.sort_values("date").copy()
    df["log_price"] = np.log(df["adj_close"])
    df["log_return"] = df["log_price"].diff()
    df = df.dropna()

    # Merge regime signals
    df = df.merge(
        regime_df[["date", "regime"]],
        on="date",
        how="inner"
    )

    # Execution lag (no look-ahead)
    df["active_regime"] = df["regime"].shift(1)
    df = df.dropna(subset=["active_regime"])

    # Forward returns window
    df["fwd_vol"] = (
        df["log_return"]
        .rolling(horizon)
        .std()
        .shift(-horizon)
    )

    # Forward drawdown
    def forward_max_drawdown(prices):
        peak = prices.iloc[0]
        max_dd = 0.0
        for p in prices:
            if p > peak:
                peak = p
            dd = (p - peak) / peak
            max_dd = min(max_dd, dd)
        return max_dd

    df["fwd_drawdown"] = (
        df["adj_close"]
        .rolling(horizon)
        .apply(forward_max_drawdown, raw=False)
        .shift(-horizon)
    )

    # Long-run volatility benchmark
    vol_threshold = df["log_return"].std()

    # Identify false positives
    critical_df = df[df["active_regime"] == "CRITICAL"].copy()

    critical_df["risk_event"] = (
        (critical_df["fwd_drawdown"] <= drawdown_threshold) |
        (critical_df["fwd_vol"] > vol_threshold)
    )

    false_positives = (~critical_df["risk_event"]).sum()
    total_signals = len(critical_df)

    false_positive_rate = (
        false_positives / total_signals if total_signals > 0 else 0
    )

    summary = {
        "total_critical_signals": total_signals,
        "false_positives": false_positives,
        "false_positive_rate": round(false_positive_rate, 3),
        "avg_forward_drawdown": critical_df["fwd_drawdown"].mean(),
        "avg_forward_vol": critical_df["fwd_vol"].mean(),
    }

    return summary, critical_df
