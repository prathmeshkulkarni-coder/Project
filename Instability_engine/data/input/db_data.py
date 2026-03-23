import pandas as pd
import numpy as np
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), "../../../../.env")
load_dotenv(dotenv_path="/home/prathmesh/Desktop/Quant/Project/.env")

def get_engine():
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        return create_engine(database_url)

    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db = os.getenv("DB_NAME")
    return create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

def read_prices_for_lppl(symbol):
    engine = get_engine()
    
    # Using text() and params for SQL safety
    query = text("""
        SELECT date, adj_close , log_return
        FROM prices 
        WHERE symbol = :symbol 
        ORDER BY date ASC
    """)
    
    # 1. Load data
    df = pd.read_sql(query, engine, params={"symbol": symbol})
    
    if df.empty:
        return None
    
    # 2. Transform for the LPPL Math
    # We create 't' as an ordinal sequence (1, 2, 3...)
    df['t'] = np.arange(len(df))
    
    # 'Logarithmic Turn': Essential for Phase 1 math
    df['log_price'] = np.log(df['adj_close'])
    return df