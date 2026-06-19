"""Data ingestion: pull free total-return equity series, FX, and rates to monthly.

All series are returned/saved as month-end pandas Series indexed by a tz-naive
DatetimeIndex. Equities come from yfinance with auto_adjust=True (total return).
FX and rates come from FRED CSV (no API key needed).
"""
from __future__ import annotations

import io
import os
from typing import Iterable

import pandas as pd
import requests

from . import config


# ---------------------------------------------------------------------------
# yfinance (equities / ETFs)
# ---------------------------------------------------------------------------
def fetch_yf_monthly(ticker: str, start: str = config.START_DATE) -> pd.Series:
    """Month-end total-return level for a single ticker via yfinance.

    Downloads daily auto-adjusted closes (dividends reinvested) and resamples to
    month-end, taking the last available close in each month. Returns an empty
    Series if the ticker has no data.
    """
    import yfinance as yf

    df = yf.download(
        ticker, start=start, interval="1d", auto_adjust=True,
        progress=False, threads=False,
    )
    if df is None or df.empty:
        return pd.Series(dtype="float64", name=ticker)

    close = df["Close"]
    if isinstance(close, pd.DataFrame):       # yfinance sometimes returns a frame
        close = close.iloc[:, 0]
    monthly = close.resample(config.RESOLUTION).last().dropna()
    monthly.name = ticker
    monthly.index = monthly.index.tz_localize(None)
    return monthly


def fetch_first_available(candidates: Iterable[str], start: str = config.START_DATE):
    """Try candidate tickers in order; return (ticker, series) for the longest one
    that returns data. Returns (None, empty Series) if all fail."""
    best_ticker, best = None, pd.Series(dtype="float64")
    for tkr in candidates:
        try:
            s = fetch_yf_monthly(tkr, start=start)
        except Exception as e:  # network / parsing hiccups shouldn't abort the run
            print(f"    ! {tkr}: {e}")
            continue
        if not s.empty and len(s) > len(best):
            best_ticker, best = tkr, s
    return best_ticker, best


# ---------------------------------------------------------------------------
# FRED (FX & rates)
# ---------------------------------------------------------------------------
def fetch_fred_monthly(series_id: str, start: str = config.START_DATE) -> pd.Series:
    """Month-end series from FRED CSV. Handles '.' missing markers and resamples
    daily series to month-end last."""
    url = config.FRED_CSV_URL.format(series_id=series_id)
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    df = pd.read_csv(io.StringIO(resp.text), na_values=".")
    df.columns = ["date", "value"]
    df["date"] = pd.to_datetime(df["date"])
    s = df.set_index("date")["value"].dropna().astype("float64")
    s = s[s.index >= pd.Timestamp(start)]
    s = s.resample(config.RESOLUTION).last().dropna()
    s.name = series_id
    return s


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------
def save_series(series: pd.Series, name: str, directory: str = config.RAW_DIR) -> str:
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, f"{name}.csv")
    series.to_frame("value").to_csv(path, index_label="date")
    return path


def load_series(name: str, directory: str = config.RAW_DIR) -> pd.Series:
    path = os.path.join(directory, f"{name}.csv")
    df = pd.read_csv(path, parse_dates=["date"])
    return df.set_index("date")["value"]
