import pandas as pd
import numpy as np

def run_regime_backtest(price_df, regime_df, risk_off_factor=0.2):
    """
    Price_df: columns [date, adj_close]
    Regime_df: columns [date, regime] (The output of your LPPL engine)
    risk_off_factor: 0.2 means you keep only 20% exposure during CRITICAL states.
    """
    
    # 1. Prepare Returns
    df = price_df.sort_values('date').copy()
    df['log_price'] = np.log(df['adj_close'])
    df['log_return'] = df['log_price'].diff()

    # 2. Merge Regime Signals
    # We use an inner join to ensure we only test dates where both exist
    df = df.merge(regime_df[['date', 'regime']], on='date', how='inner')

    # 3. Execution Lag (The 'Honest' Factor)
    # You see a bubble today, you can only act at the next market open.
    # This prevents 'Look-Ahead Bias'.
    df['active_regime'] = df['regime'].shift(1).fillna("NORMAL")

    # 4. Strategy Returns
    # Baseline: Always 100% invested (Buy & Hold)
    df['baseline_ret'] = df['log_return']

    # LPPL Strategy: Reduce exposure during CRITICAL or WARNING
    df['strat_ret'] = np.where(
        df['active_regime'] == "CRITICAL",
        df['log_return'] * risk_off_factor,
        np.where(
            df['active_regime'] == "WARNING",
            df['log_return'] * 0.6, # Moderate protection for warnings
            df['log_return']
        )
    )

    # 5. Performance Math
    # Cumulative returns via log-summation (Vectorized)
    df['baseline_equity'] = df['baseline_ret'].cumsum().apply(np.exp)
    df['strat_equity'] = df['strat_ret'].cumsum().apply(np.exp)

    # 6. Risk Metrics (Max Drawdown & Sharpe)
    def calculate_metrics(equity_curve, returns):
        # Max Drawdown
        running_max = equity_curve.cummax()
        drawdown = (equity_curve - running_max) / running_max
        max_dd = drawdown.min()
        
        # Annualized Sharpe (Risk-Adjusted Return)
        vol = returns.std() * np.sqrt(252)
        sharpe = (returns.mean() * 252) / vol if vol != 0 else 0
        
        return max_dd, sharpe

    base_dd, base_sharpe = calculate_metrics(df['baseline_equity'], df['baseline_ret'])
    strat_dd, strat_sharpe = calculate_metrics(df['strat_equity'], df['strat_ret'])

    # 7. Final Results Object
    performance = {
        "baseline": {"drawdown": base_dd, "sharpe": base_sharpe},
        "strategy": {"drawdown": strat_dd, "sharpe": strat_sharpe},
        "protection_efficiency": (1 - (strat_dd / base_dd)) if base_dd != 0 else 0
    }

    return performance, df

# ==========================================
# Example Usage:
# results, full_df = run_regime_backtest(my_prices, my_regimes)
# print(f"Drawdown Protection: {results['protection_efficiency']:.2%}")
# ==========================================