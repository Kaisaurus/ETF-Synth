"""Construct synthetic monthly total-return histories for DHHF, BGBL, GHHF, GGBL.

Pipeline:
  raw proxies (USD/AUD) --> AUD total-return sleeves --> fund baskets
  --> apply fees / gearing --> synthetic index levels (base 100).

All math is in monthly *simple* returns; levels are cumulative products.
"""
from __future__ import annotations

import pandas as pd

from . import config, ingest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def to_aud(usd_level: pd.Series, usd_per_aud: pd.Series) -> pd.Series:
    """Convert a USD-denominated total-return level into AUD terms.

    AUD value = USD value / (USD per AUD). When the AUD appreciates the foreign
    asset is worth less to an AUD investor, as expected for an unhedged holding.
    """
    fx = usd_per_aud.reindex(usd_level.index).ffill()
    return (usd_level / fx).dropna()


def returns(level: pd.Series) -> pd.Series:
    return level.pct_change().dropna()


def level_from_returns(rets: pd.Series, base: float = 100.0) -> pd.Series:
    return base * (1.0 + rets).cumprod()


def splice_returns(series_list: list[pd.Series]) -> pd.Series:
    """Combine return series (priority/best-quality first). For each month use the
    first source that has a value. Splicing returns (not levels) avoids seams."""
    full = sorted(set().union(*[s.index for s in series_list]))
    combined = series_list[0].reindex(full)
    for s in series_list[1:]:
        combined = combined.fillna(s.reindex(full))
    return combined.dropna()


def _proxy_aud_returns(ticker: str, fx: pd.Series) -> pd.Series:
    """Fetch a proxy's monthly TR level and return AUD monthly returns."""
    lvl = ingest.fetch_yf_monthly(ticker)
    if lvl.empty:
        return pd.Series(dtype="float64")
    if ticker in config.USD_PROXIES:
        lvl = to_aud(lvl, fx)
    return returns(lvl)


# ---------------------------------------------------------------------------
# Sleeves (AUD monthly total returns)
# ---------------------------------------------------------------------------
def build_sleeves(fx: pd.Series) -> dict[str, pd.Series]:
    sleeves: dict[str, pd.Series] = {}

    # US total market & emerging markets: single long proxies, AUD-converted.
    sleeves["us_total"] = _proxy_aud_returns(config.SLEEVE_PROXIES["us_total"][0], fx)
    sleeves["emerging"] = _proxy_aud_returns(config.SLEEVE_PROXIES["emerging"][0], fx)

    # Developed ex-US: splice VTMGX <- VGTSX <- VWIGX (all AUD).
    chain = [_proxy_aud_returns(t, fx) for t in config.DEV_EX_US_CHAIN]
    chain = [s for s in chain if not s.empty]
    sleeves["dev_ex_us"] = splice_returns(chain)

    # Australian shares total return: STW.AX (real TR) spliced over reconstructed
    # accumulation (^AORD price + dividend-yield accrual) for the pre-STW period.
    stw = ingest.fetch_yf_monthly(config.AUS_TR_ETF)          # already AUD
    aord = ingest.fetch_yf_monthly(config.AUS_PRICE_INDEX)    # price only, AUD
    r_stw = returns(stw)
    r_aord_tr = returns(aord) + config.AUS_DIV_YIELD / 12.0
    sleeves["aus_shares"] = splice_returns([r_stw, r_aord_tr])

    return sleeves


# ---------------------------------------------------------------------------
# Fund baskets & fees / gearing
# ---------------------------------------------------------------------------
def _blend(sleeves: dict[str, pd.Series], weights: dict[str, float]) -> pd.Series:
    """Weighted blend of sleeve returns over their common (inner-join) dates."""
    df = pd.DataFrame({k: sleeves[k] for k in weights}).dropna()
    return (df * pd.Series(weights)).sum(axis=1)


def apply_fee(gross: pd.Series, annual_mer: float) -> pd.Series:
    return gross - annual_mer / 12.0


def apply_gearing(gross: pd.Series, cash_rate_pct: pd.Series) -> pd.Series:
    """Internally geared monthly return on an ungeared basket.

    g   = gross exposure per unit equity = 1 / (1 - LVR)
    cost= (g - 1) * (cash_rate + spread)/12   on the borrowed portion
    """
    lvr = config.GEARING["target_lvr"]
    g = 1.0 / (1.0 - lvr)
    spread = config.GEARING["borrow_spread"]
    rate_m = (cash_rate_pct.reindex(gross.index).ffill() / 100.0 + spread) / 12.0
    return g * gross - (g - 1.0) * rate_m


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------
def build_all() -> dict[str, pd.Series]:
    """Return synthetic index levels (base 100) for all four funds + the two
    ungeared baskets used to derive the geared pair."""
    fx = ingest.load_series("usd_per_aud")
    cash = ingest.load_series("aus_3m_rate")

    sleeves = build_sleeves(fx)

    dhhf_basket = _blend(sleeves, config.DHHF_WEIGHTS)
    world_basket = _blend(sleeves, config.WORLD_EX_AUS_WEIGHTS)

    out_rets = {
        "DHHF": apply_fee(dhhf_basket, config.MER["DHHF"]),
        "BGBL": apply_fee(world_basket, config.MER["BGBL"]),
        "GHHF": apply_fee(apply_gearing(dhhf_basket, cash), config.MER["GHHF"]),
        "GGBL": apply_fee(apply_gearing(world_basket, cash), config.MER["GGBL"]),
    }
    levels = {k: level_from_returns(v) for k, v in out_rets.items()}
    levels["_dhhf_basket_gross"] = level_from_returns(dhhf_basket)
    levels["_world_basket_gross"] = level_from_returns(world_basket)
    return levels
