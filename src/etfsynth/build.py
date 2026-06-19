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


_LEVEL_CACHE: dict[str, pd.Series] = {}


def _level(ticker: str) -> pd.Series:
    """Fetch a ticker's monthly TR level once, then memoize for the run."""
    if ticker not in _LEVEL_CACHE:
        _LEVEL_CACHE[ticker] = ingest.fetch_yf_monthly(ticker)
    return _LEVEL_CACHE[ticker]


def _proxy_aud_returns(ticker: str, fx: pd.Series) -> pd.Series:
    """Monthly AUD total returns (USD proxies converted to AUD = unhedged)."""
    lvl = _level(ticker)
    if lvl.empty:
        return pd.Series(dtype="float64")
    if ticker in config.USD_PROXIES:
        lvl = to_aud(lvl, fx)
    return returns(lvl)


def _proxy_local_returns(ticker: str) -> pd.Series:
    """Monthly local-currency total returns (no FX conversion). Used as a proxy
    for AUD-hedged exposure (ignores hedge carry)."""
    lvl = _level(ticker)
    return returns(lvl) if not lvl.empty else pd.Series(dtype="float64")


def _spliced(tickers: list[str], fx: pd.Series, local: bool = False) -> pd.Series:
    fn = (lambda t: _proxy_local_returns(t)) if local else (lambda t: _proxy_aud_returns(t, fx))
    parts = [fn(t) for t in tickers]
    return splice_returns([s for s in parts if not s.empty])


def _aus_sleeve(fx: pd.Series) -> pd.Series:
    """Australian shares total return: STW.AX real TR spliced over ^AORD price +
    dividend-yield add-back for the pre-STW period."""
    r_stw = returns(_level(config.AUS_TR_ETF))
    r_aord_tr = returns(_level(config.AUS_PRICE_INDEX)) + config.AUS_DIV_YIELD / 12.0
    return splice_returns([r_stw, r_aord_tr])


# ---------------------------------------------------------------------------
# Sleeves (AUD monthly total returns)
# ---------------------------------------------------------------------------
def build_sleeves(fx: pd.Series) -> dict[str, pd.Series]:
    sleeves: dict[str, pd.Series] = {}

    # US total market & emerging markets: single long proxies, AUD-converted.
    sleeves["us_total"] = _proxy_aud_returns(config.SLEEVE_PROXIES["us_total"][0], fx)
    sleeves["emerging"] = _proxy_aud_returns(config.SLEEVE_PROXIES["emerging"][0], fx)

    # Developed ex-US: splice VTMGX <- VGTSX <- VWIGX (all AUD).
    sleeves["dev_ex_us"] = _spliced(config.DEV_EX_US_CHAIN, fx)

    # Australian shares total return.
    sleeves["aus_shares"] = _aus_sleeve(fx)

    return sleeves


def build_vdhg(fx: pd.Series) -> pd.Series:
    """Synthetic VDHG (90/10) monthly net return from free proxies.

    Developed ex-Aus is the US+dev market-cap blend, taken both unhedged (AUD) and
    hedged (local-currency). Emerging is AUD; bonds use the local-currency bond
    proxy as a stand-in for AUD-hedged global aggregate.
    """
    w = config.WORLD_EX_AUS_WEIGHTS
    us_t = config.SLEEVE_PROXIES["us_total"][0]

    intl_unhedged = (w["us_total"] * _proxy_aud_returns(us_t, fx)
                     + w["dev_ex_us"] * _spliced(config.DEV_EX_US_CHAIN, fx))
    intl_hedged = (w["us_total"] * _proxy_local_returns(us_t)
                   + w["dev_ex_us"] * _spliced(config.DEV_EX_US_CHAIN, fx, local=True))

    parts = {
        "aus_shares":    _aus_sleeve(fx),
        "intl_unhedged": intl_unhedged,
        "intl_hedged":   intl_hedged,
        "emerging":      _proxy_aud_returns(config.SLEEVE_PROXIES["emerging"][0], fx),
        "bonds":         _proxy_local_returns(config.BOND_PROXY),
    }
    df = pd.DataFrame(parts).dropna()
    gross = (df * pd.Series(config.VDHG_WEIGHTS)).sum(axis=1)
    return apply_fee(gross, config.MER["VDHG"])


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
        "VDHG": build_vdhg(fx),
        "BGBL": apply_fee(world_basket, config.MER["BGBL"]),
        "GHHF": apply_fee(apply_gearing(dhhf_basket, cash), config.MER["GHHF"]),
        "GGBL": apply_fee(apply_gearing(world_basket, cash), config.MER["GGBL"]),
    }
    levels = {k: level_from_returns(v) for k, v in out_rets.items()}
    levels["_dhhf_basket_gross"] = level_from_returns(dhhf_basket)
    levels["_world_basket_gross"] = level_from_returns(world_basket)
    return levels
