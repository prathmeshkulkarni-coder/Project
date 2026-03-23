import pandas as pd

def clean_price_data(df):
    # 1. Sort by date
    df = df.sort_values("date")

    # 2. Set date as index
    df = df.set_index("date")

    # 3. Create continuous business-day index
    full_index = pd.date_range(
        start=df.index.min(),
        end=df.index.max(),
        freq="B"
    )

    # 4. Reindex (this introduces NaNs)
    df = df.reindex(full_index)

    # 5. Forward-fill price columns
    price_cols = ["open", "high", "low", "close", "adj_close"]
    df[price_cols] = df[price_cols].ffill()

    # 6. Volume = 0 on non-trading days
    df["volume"] = df["volume"].fillna(0)

    # 7.  FIX: restore symbol column
    df["symbol"] = df["symbol"].ffill()

    # 8. Restore index name
    df.index.name = "date"

    # 9. Back to column form
    df = df.reset_index()

    return df
