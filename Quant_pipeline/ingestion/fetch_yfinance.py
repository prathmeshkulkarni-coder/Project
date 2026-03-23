import yfinance as yf
import pandas as pd

def fetch_stock(symbol,start,end):
    df = yf.download(symbol, start=start, end =end,auto_adjust=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df.reset_index()
    df.columns = (
        df.columns
        .str.lower()
        .str.replace(" ", "_")
    )
    print(df)
    df["symbol"] = symbol
    return df
