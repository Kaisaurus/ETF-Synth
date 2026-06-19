# Fund specifications & data sources

Verified against Betashares / Morningstar / ASX sources, June 2026. Figures that still
need a final primary-source check are flagged ⚠️.

## DHHF — Diversified All Growth ETF
- **Type:** Actively managed multi-asset, fund-of-ETFs. ~100% growth assets ("All Growth").
  Not strictly index-tracking: a strategic asset allocation (SAA) reviewed annually and
  rebalanced when sleeve weights drift >2% from target at quarter-end.
- **MER:** 0.19% p.a.
- **Inception:** **December 2019** (confirmed: yfinance month-end prices start 2019-12-31).
- **Current sleeve composition** (drifts over time):
  | Sleeve | ~Weight | Proxy index for synthetic build |
  |--------|---------|----------------------------------|
  | US total market (Vanguard Total Stock Market) | ~41% | CRSP US Total Market / MSCI USA / S&P 500 (proxy) |
  | Australia 200 (Betashares A200) | ~36% | S&P/ASX 200; All Ords Accum. pre-2000 |
  | Developed world ex-US (SPDR Dev World ex-US) | ~17% | MSCI World ex USA |
  | Emerging markets (SPDR Portfolio EM) | ~6% | MSCI Emerging Markets |
- All sleeves **unhedged** (AUD investor bears FX). US total-market sleeve implicitly
  includes US small caps.
- **Note:** for the synthetic build, decide whether to hold target SAA weights constant or
  approximate the historical drift. v1: hold constant at a documented target.

## BGBL — Global Shares ETF
- **Type:** Index tracker.
- **Index:** Solactive GBS Developed Markets ex Australia Large & Mid Cap Index (~1,300–1,500
  stocks, 23 developed countries ex-Australia), unhedged AUD.
- **MER:** 0.08% p.a.
- **Inception:** ~9 May 2023.
- **Synthetic proxy:** MSCI World ex Australia (or older ETFs VGS / IWLD) — methodology is
  near-identical (developed ex-Aus, market-cap weighted, large/mid).

## GHHF — Wealth Builder Diversified All Growth Geared (30–40% LVR) Complex ETF
- **Type:** Internally geared version of the DHHF-style all-growth portfolio.
- **Gearing:** 30–40% LVR (loan-to-value), maintained within band.
- **MER:** 0.35% p.a.
- **Inception:** 19 April 2024.
- **Synthetic build:** apply gearing model on ungeared DHHF synthetic.

## GGBL — Wealth Builder Global Shares Geared (30–40% LVR) Complex ETF
- **Type:** Internally geared version of BGBL (borrows + invests proceeds in BGBL exposure).
- **Gearing:** 30–40% LVR.
- **MER:** ⚠️ confirm (~0.35% expected).
- **Inception:** **~October 2025** (price data starts 2025-10-31; very short live window — only ~9 months for calibration).
- **Synthetic build:** apply gearing model on ungeared BGBL synthetic.

## Gearing model (GHHF, GGBL)
Monthly approximation of internal gearing:

```
geared_ret_t = G_t * underlying_ret_t  -  (G_t - 1) * borrow_rate_t/12  -  mer/12
```

where `G_t` = gross exposure / equity (e.g. LVR 35% → G ≈ 1/(1-0.35) ≈ 1.54),
`borrow_rate_t` = RBA cash rate + wholesale spread (spread calibrated to live data).
Monthly rebalancing approximates the fund's daily reset; expect some path-dependence
("volatility decay") vs the real fund — calibrate spread + G to the live overlap window.

## Data coverage (from `scripts/fetch_data.py`, June 2026)
Monthly, total-return where noted. Full report in `data/raw/_coverage.csv`.

| Series | Chosen proxy | History from | Notes |
|--------|-------------|--------------|-------|
| US total market | VTSMX (Vanguard) | 1994-12 ✅ | TR via adj. close |
| Emerging markets | VEIEX (Vanguard) | 1994-12 ✅ | TR via adj. close |
| Developed ex-US | VTMGX (Vanguard) | 1999-08 ⚠️ | **gap 1995–1999**, needs backfill |
| Australian shares | ^AORD | 1994-12 ⚠️ | **PRICE only — no dividends**, needs TR fix |
| Total international | VGTSX | 1996-04 | dev+EM; candidate backfill for dev_ex_us |
| USD per AUD | FRED DEXUSAL | 1994-12 ✅ | FX for unhedged sleeves |
| AUS 3m interbank | FRED IR3TIB01AUM156N | 1994-12 ✅ | cash-rate proxy for gearing |
| Real DHHF/BGBL/GHHF/GGBL | *.AX | 2019-12 / 2023-05 / 2024-04 / 2025-10 | calibration targets |

### Open data fixes before the build layer
1. **Australian total return** — `^AORD` excludes dividends (~4%/yr + franking). Fix by
   reconstructing accumulation (price + dividend-yield accrual) and/or splicing STW.AX
   (TR from 2001). Biggest single fidelity issue.
2. **Developed ex-US 1995–1999 gap** — backfill VTMGX with VGTSX (1996) and/or an active
   intl proxy; small residual error on a 17% sleeve.

## Data sources
| Series | Source | Notes |
|--------|--------|-------|
| Real ETF prices (calibration) | Yahoo Finance / Stooq / ASX | since inception only |
| MSCI World ex-Aus / ex-USA / USA / EM | MSCI end-of-day index series | monthly, long history |
| S&P/ASX 200 Accum. / All Ords Accum. | S&P / ASX | All Ords pre-2000 |
| RBA cash rate target | RBA (free) | from 1990 |
| AUD/USD & trade-weighted FX | RBA / FRED | unhedged sleeves |

## Decisions log
- **2026-06-19** — Resolution: **monthly**. Start date: **January 1995** (full dot-com cycle
  incl. run-up + crash, Asian crisis, GFC, COVID, 2022 shock). Binding constraint: global
  small-cap sleeve history — handled by proxying with large-cap pre-availability if needed.
- **2026-06-19** — Return basis: **total return** (distributions reinvested). Franking
  credits on the Australian sleeve: optional later layer, excluded from v1.
