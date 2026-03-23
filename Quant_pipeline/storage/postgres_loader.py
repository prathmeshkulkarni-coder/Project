import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

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
    return create_engine(
        f"postgresql://{user}:{password}@{host}:{port}/{db}"
    )

def load_to_postgres(df):
    engine = get_engine()
    df.to_sql(
        "prices",
        engine,
        if_exists="append",
        index=False,
        method="multi"
    )
