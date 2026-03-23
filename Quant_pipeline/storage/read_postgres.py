import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
def read_from_postgres(symbol):
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        engine = create_engine(database_url)
    else:
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        db = os.getenv("DB_NAME")
        engine = create_engine(
            f"postgresql://{user}:{password}@{host}:{port}/{db}"
        )

    query = f"""
    SELECT date, adj_close, close, open
    FROM prices
    WHERE symbol = '{symbol}'
    ORDER BY date
    """

    df = pd.read_sql(query, engine)
    return df