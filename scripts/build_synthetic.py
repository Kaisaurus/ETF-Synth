"""Build synthetic histories and calibrate against the live ETF windows.

Prereq: run scripts/fetch_data.py first (needs data/raw FX + cash rate + real ETFs).
Run:    python scripts/build_synthetic.py
"""
from __future__ import annotations

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from etfsynth import build, calibrate, config  # noqa: E402


def main():
    levels = build.build_all()

    os.makedirs(config.PROCESSED_DIR, exist_ok=True)
    funds = ["DHHF", "BGBL", "GHHF", "GGBL"]

    # Save synthetic levels (base 100) + a combined wide CSV.
    wide = pd.DataFrame({k: levels[k] for k in funds})
    for f in funds:
        levels[f].to_frame("level").to_csv(
            os.path.join(config.PROCESSED_DIR, f"synth_{f}.csv"), index_label="date")
    wide.to_csv(os.path.join(config.PROCESSED_DIR, "synth_all.csv"), index_label="date")

    print("== Synthetic series ==")
    for f in funds:
        s = levels[f]
        cagr = (s.iloc[-1] / s.iloc[0]) ** (12 / (len(s) - 1)) - 1
        print(f"  {f:5s} {s.index.min().date()} -> {s.index.max().date()}  "
              f"{len(s):3d} mo  CAGR {cagr:6.2%}  end {s.iloc[-1]:,.1f}")

    print("\n== Calibration vs real ETFs (overlap window) ==")
    rep = calibrate.report(levels, config.REAL_ETFS)
    if rep.empty:
        print("  (no overlap data — run fetch_data.py first)")
    else:
        with pd.option_context("display.float_format", lambda x: f"{x:.4f}"):
            print(rep.to_string(index=False))
        rep.to_csv(os.path.join(config.PROCESSED_DIR, "_calibration.csv"), index=False)

    print(f"\nSaved synthetic series + calibration to {config.PROCESSED_DIR}/")


if __name__ == "__main__":
    main()
