"""Fetch all source series to data/raw and print a coverage report.

Run:  python scripts/fetch_data.py
"""
from __future__ import annotations

import os
import sys

import pandas as pd

# allow running as a plain script (no install needed)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from etfsynth import config, ingest  # noqa: E402


def _row(name, ticker, s):
    if s is None or s.empty:
        return {"series": name, "ticker": ticker or "-", "start": "-",
                "end": "-", "months": 0, "back_to_95": ""}
    return {
        "series": name,
        "ticker": ticker or "-",
        "start": s.index.min().date().isoformat(),
        "end": s.index.max().date().isoformat(),
        "months": len(s),
        "back_to_95": "yes" if s.index.min() <= pd.Timestamp("1995-01-31") else "no",
    }


def main():
    rows = []

    print("== Real ETFs (calibration targets) ==")
    for name, tkr in config.REAL_ETFS.items():
        s = ingest.fetch_yf_monthly(tkr)
        if not s.empty:
            ingest.save_series(s, f"etf_{name}")
        print(f"  {name:5s} {tkr:9s} -> {len(s)} months")
        rows.append(_row(f"etf_{name}", tkr, s))

    print("\n== Sleeve proxies (longest candidate wins) ==")
    for sleeve, candidates in config.SLEEVE_PROXIES.items():
        tkr, s = ingest.fetch_first_available(candidates)
        if not s.empty:
            ingest.save_series(s, f"sleeve_{sleeve}")
        print(f"  {sleeve:12s} -> {tkr or 'NONE':9s} {len(s)} months")
        rows.append(_row(f"sleeve_{sleeve}", tkr, s))

    print("\n== FX & rates (FRED) ==")
    for name, sid in config.FRED_SERIES.items():
        try:
            s = ingest.fetch_fred_monthly(sid)
            ingest.save_series(s, name)
        except Exception as e:
            print(f"  {name:12s} -> ERROR {e}")
            rows.append(_row(name, sid, None))
            continue
        print(f"  {name:12s} -> {sid:18s} {len(s)} months")
        rows.append(_row(name, sid, s))

    report = pd.DataFrame(rows)
    print("\n== Coverage report ==")
    print(report.to_string(index=False))
    os.makedirs(config.RAW_DIR, exist_ok=True)
    report.to_csv(os.path.join(config.RAW_DIR, "_coverage.csv"), index=False)
    print(f"\nSaved raw series + _coverage.csv to {config.RAW_DIR}/")


if __name__ == "__main__":
    main()
