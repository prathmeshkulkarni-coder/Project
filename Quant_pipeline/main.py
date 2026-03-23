from storage.pipeline import ingest_many_stocks


if __name__ == "__main__":
    symbols = [
        "SI=F",
    ]
    results = ingest_many_stocks(symbols, start="2024-01-01",end = "2025-12-15")

    for r in results:
        print(r)

'''WITH return_calc AS (
    SELECT 
        date, 
        symbol,
        LN(adj_close / LAG(adj_close) OVER (PARTITION BY symbol ORDER BY date)) as calc_return
    FROM prices
)
UPDATE prices
SET log_return = return_calc.calc_return
FROM return_calc
WHERE prices.date = return_calc.date 
AND prices.symbol = return_calc.symbol;'''

