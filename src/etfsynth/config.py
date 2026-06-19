"""Central configuration: tickers, sources, sleeves, and model parameters.

Equity series use *total return* (yfinance auto_adjust=True -> dividends reinvested).
Proxy choices list candidates longest-history-first; the ingestion coverage report
tells us which actually reach back to the START_DATE so we can lock them in.
"""
from __future__ import annotations

# ---- Global scope ----------------------------------------------------------
START_DATE = "1994-12-01"   # buffer before Jan-1995 so first monthly return is clean
RESOLUTION = "ME"           # pandas month-end

# ---- Real ETFs (calibration targets; short live history) -------------------
REAL_ETFS = {
    "DHHF": "DHHF.AX",
    "BGBL": "BGBL.AX",
    "GHHF": "GHHF.AX",
    "GGBL": "GGBL.AX",
}

# ---- Sleeve proxies (free, long total-return history) -----------------------
# Each sleeve maps to candidate tickers, longest-history-first. Vanguard index
# *mutual funds* are used because their adjusted close is total return and many
# predate the equivalent ETFs by a decade.
SLEEVE_PROXIES = {
    "us_total":       ["VTSMX", "^SP500TR", "VFINX"],   # US total market (~1992)
    "dev_ex_us":      ["VTMGX", "EFA", "VEA"],          # Developed mkts ex-US
    "emerging":       ["VEIEX", "EEM", "VWO"],          # Emerging markets (~1994)
    "aus_shares":     ["^AXJOA", "^AXKOA", "^AORD"],    # AUS accumulation if avail
    "intl_total":     ["VGTSX", "VXUS"],                # Total intl (dev+EM, ~1996)
}

# ---- FX & rates (FRED CSV, no API key) -------------------------------------
FRED_SERIES = {
    "usd_per_aud": "DEXUSAL",        # USD per 1 AUD, daily, from 1971
    "aus_3m_rate": "IR3TIB01AUM156N",  # AUS 3m interbank, monthly, ~cash-rate proxy
}
FRED_CSV_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"

# ---- Fund fees (annual MER, decimal) ---------------------------------------
MER = {
    "DHHF": 0.0019,
    "BGBL": 0.0008,
    "GHHF": 0.0035,
    "GGBL": 0.0035,   # ⚠️ confirm
}

# ---- DHHF strategic sleeve weights (held constant in v1) -------------------
# Approximate current target; sums to 1.0. See docs/fund_specs.md.
DHHF_WEIGHTS = {
    "us_total":   0.41,
    "aus_shares": 0.36,
    "dev_ex_us":  0.17,
    "emerging":   0.06,
}

# ---- Gearing model (GHHF, GGBL) --------------------------------------------
GEARING = {
    "target_lvr": 0.35,          # mid of 30-40% band -> gross/equity ~1.538
    "borrow_spread": 0.010,      # over cash rate; calibrate to live window
}

# ---- Paths -----------------------------------------------------------------
RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
