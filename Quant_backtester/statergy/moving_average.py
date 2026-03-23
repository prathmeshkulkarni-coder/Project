import pandas as pd

def strategy(data,short_window =2,long_window =4):
    df = data.copy()
    df["short_ma"] = df["close"].rolling(window = short_window).mean()
    df["long_ma"] = df["close"].rolling(window = long_window).mean()
    df["signal"] = 0
    df.loc[df["short_ma"]>df["long_ma"],"signal"] = 1
    df.loc[df["short_ma"]<df["long_ma"],"signal"] = -1

    return df["signal"]