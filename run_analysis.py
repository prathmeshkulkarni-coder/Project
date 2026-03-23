"""
Run this FIRST from terminal before opening the Streamlit app:
    python3 run_analysis.py

It runs the heavy LPPL computation and saves output to result.json.
Streamlit then just reads the JSON and displays it instantly.
"""
import sys
import os
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Instability_engine.main import run_lppl

def main():
    SYMBOLS = ["SI=F"]  # Add more symbols here if needed

    results = {}
    for symbol in SYMBOLS:
        print(f"Running LPPL for {symbol}...")
        try:
            output = run_lppl(symbol)
            results[symbol] = output
            print(f"  Done: {output}")
        except Exception as e:
            results[symbol] = {"error": str(e)}
            print(f"  Error for {symbol}: {e}")

    with open("result.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\n✅ Saved results to result.json — now open Streamlit!")

if __name__ == "__main__":
    main()
