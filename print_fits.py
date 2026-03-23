import sys
import os

from Instability_engine.main import run_lppl
from Instability_engine.data.input.db_data import read_prices_for_lppl
from Instability_engine.analysis.rolling_windows import run_rolling_lppl
from Instability_engine.analysis.convergence_metrics import lppl_convergence_metrics
from Instability_engine.analysis.convergence_tests import calculate_criticality_index
from Instability_engine.analysis.hazard_score import calculate_hazard_score

symbol = "SI=F"
df = read_prices_for_lppl(symbol)
t = df["t"].values
log_prices = df["log_price"].values

lppl_result = run_rolling_lppl(t, log_prices)
fits = lppl_result["fits"]
print(f"Total fits found: {len(fits)}")
for i, f in enumerate(fits):
    print(f"Fit {i}: A={f['A']:.2f}, B={f['B']:.4f}, C={f['C']:.4f}, tc={f['tc']:.2f}, m={f['m']:.4f}, omega={f['omega']:.4f}, phi={f['phi']:.4f}")

metrics = lppl_convergence_metrics(fits)
if metrics:
    print(metrics)
