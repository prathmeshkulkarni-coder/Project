from ingestion.fetch_yfinance import fetch_stock
from storage.postgres_loader import load_to_postgres, get_engine
from cleaning.clean_data import clean_price_data
from sqlalchemy import text
import numpy as np

def get_existing_dates(symbol):
    """Returns a set of dates already stored in DB for this symbol."""
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT date FROM prices WHERE symbol = :symbol"),
            {"symbol": symbol}
        )
        rows = result.fetchall()
    return {str(r[0])[:10] for r in rows}  # normalize to 'YYYY-MM-DD'

def ingest_stock_to_db(symbol, start, end):
    # 1. Fetch
    raw_df = fetch_stock(symbol, start=start, end=end)

    # 2. Clean
    clean_df = clean_price_data(raw_df)

    # 3. Add Log Return (Feature Engineering Step)
    clean_df["log_return"] = np.log(
        clean_df["adj_close"] / clean_df["adj_close"].shift(1)
        )
    clean_df["log_return"] = clean_df["log_return"].fillna(0)

    # 4. Filter out dates already in DB
    try:
        existing_dates = get_existing_dates(symbol)
        clean_df["date_str"] = clean_df["date"].astype(str).str[:10]
        new_df = clean_df[~clean_df["date_str"].isin(existing_dates)].drop(columns=["date_str"])
    except Exception:
        new_df = clean_df  # Table may not exist yet — insert everything

    if new_df.empty:
        return f"{symbol} — no new data to insert (already up to date)"

    # 5. Safety check
    assert new_df.isna().sum().sum() == 0, "NaNs found after cleaning"

    # 6. Load only new rows
    load_to_postgres(new_df)

    return f"{symbol} ingested successfully ({len(new_df)} new rows)"

def ingest_many_stocks(symbols, start,end):
    results = []

    for symbol in symbols:
        try:
            msg = ingest_stock_to_db(symbol, start=start,end = end)
            results.append(msg)
        except Exception as e:
            results.append(f"{symbol} failed: {e}")

    return results