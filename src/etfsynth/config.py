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
    "VDHG": "VDHG.AX",
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

# Splice chains for sleeves whose primary proxy is too short (returns-based splice,
# priority/best-quality first). All USD funds are AUD-converted before splicing.
DEV_EX_US_CHAIN = ["VTMGX", "VGTSX", "VWIGX"]   # 1999 <- 1996 <- 1981(active)
# Australian total return: real ETF TR spliced over a price-index reconstruction.
AUS_TR_ETF = "STW.AX"          # SPDR S&P/ASX 200, TR via adj close (~2001)
AUS_PRICE_INDEX = "^AORD"      # All Ordinaries PRICE (no dividends)
AUS_DIV_YIELD = 0.04           # annual yield add-back for pre-STW reconstruction

# Currency: USD-denominated proxies that must be converted to AUD (unhedged).
USD_PROXIES = {"VTSMX", "^SP500TR", "VFINX", "VTMGX", "EFA", "VEA",
               "VEIEX", "EEM", "VWO", "VGTSX", "VXUS", "VWIGX", "VBMFX"}

# BGBL = developed markets ex-Australia ~ market-cap blend of US + developed-ex-US.
WORLD_EX_AUS_WEIGHTS = {"us_total": 0.70, "dev_ex_us": 0.30}

# Bond proxy for diversified funds' defensive sleeve. VBMFX = Vanguard Total Bond
# Market (US Agg), TR via adj close, from 1986. Used in *local* (USD) terms as a
# proxy for AUD-hedged global aggregate bonds (ignores hedge carry).
BOND_PROXY = "VBMFX"

# VDHG (Vanguard Diversified High Growth) ~90% growth / 10% bonds. Approximate SAA,
# with intl small-cap folded into developed-unhedged and all bonds proxied as
# hedged global agg. "hedged" sleeve uses local-currency (USD) returns.
VDHG_WEIGHTS = {
    "aus_shares":    0.36,
    "intl_unhedged": 0.33,   # developed ex-Aus unhedged (+ intl small folded in)
    "intl_hedged":   0.16,   # developed ex-Aus AUD-hedged
    "emerging":      0.05,
    "bonds":         0.10,
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
    "VDHG": 0.0027,
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
