import pandas as pd

def backtest(data,signal):
    df = data.copy()
    df["signal"] = signal

    df["position"] =df["signal"].shift(1)
    df["position"].fillna(0,inplace = True)

    df["price_return"] = df["close"].pct_change()

    df["strategy_return"] = df["position"]*df["price_return"]
    return df