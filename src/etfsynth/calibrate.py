"""Calibrate synthetic series against the real ETFs over their live overlap window.

Metrics on monthly returns:
  - n_overlap    : months both series exist
  - corr         : correlation of monthly returns (shape fidelity)
  - te_annual    : tracking error = std(synth - real) * sqrt(12)
  - drift_annual : annualized mean return gap (synth - real); systematic bias
A single constant drift adjustment can absorb that bias to produce a calibrated series.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import ingest


def _returns(level: pd.Series) -> pd.Series:
    return level.pct_change().dropna()


def metrics(synth_level: pd.Series, real_level: pd.Series) -> dict:
    rs, rr = _returns(synth_level), _returns(real_level)
    df = pd.concat([rs, rr], axis=1, join="inner").dropna()
    df.columns = ["synth", "real"]
    if len(df) < 2:
        return {"n_overlap": len(df), "corr": np.nan,
                "te_annual": np.nan, "drift_annual": np.nan}
    diff = df["synth"] - df["real"]
    return {
        "n_overlap": len(df),
        "corr": df["synth"].corr(df["real"]),
        "te_annual": diff.std(ddof=1) * np.sqrt(12),
        "drift_annual": diff.mean() * 12,
    }


def calibrate_drift(synth_level: pd.Series, real_level: pd.Series) -> pd.Series:
    """Remove the systematic monthly drift gap so the synthetic matches the real
    fund's average return over the overlap window."""
    m = metrics(synth_level, real_level)
    if not np.isfinite(m["drift_annual"]):
        return synth_level
    adj_m = m["drift_annual"] / 12.0
    rets = _returns(synth_level) - adj_m
    base = synth_level.iloc[0]
    return base * (1.0 + rets).cumprod().reindex(synth_level.index).fillna(method="bfill")


def report(levels: dict, real_map: dict[str, str]) -> pd.DataFrame:
    rows = []
    for fund in real_map:
        if fund not in levels:
            continue
        try:
            real = ingest.load_series(f"etf_{fund}")
        except FileNotFoundError:
            continue
        m = metrics(levels[fund], real)
        m = {"fund": fund, **m}
        rows.append(m)
    return pd.DataFrame(rows)
