# ETF-Synth

Reconstruct long-horizon **synthetic price/return histories** for recent Australian
Betashares ETFs from public index and proxy data, so they can be backtested across
market regimes the funds themselves are too young to have lived through.

## Funds in scope

| Ticker | Fund | Type | Inception | MER |
|--------|------|------|-----------|-----|
| DHHF | Diversified All Growth | Multi-asset (fund-of-ETFs, ~100% growth) | Dec 2019 | 0.19% |
| VDHG | Vanguard Diversified High Growth | Multi-asset (90% growth / 10% bonds) | Nov 2017 | 0.27% |
| BGBL | Global Shares | Index (Solactive GBS Dev Mkts ex-Aus L&M Cap) | May 2023 | 0.08% |
| GHHF | Wealth Builder Diversified All Growth Geared | Internally geared DHHF, 30–40% LVR | Apr 2024 | 0.35% |
| GGBL | Wealth Builder Global Shares Geared | Internally geared BGBL, 30–40% LVR | ~Oct 2025 | ~0.35% |

Inception dates confirmed from price data — see [docs/fund_specs.md](docs/fund_specs.md).

## Approach

1. **Ungeared trackers (DHHF, BGBL)** — rebuild from underlying index total returns
   (or long-history proxy ETFs), minus fees and tracking drag, in AUD.
2. **Geared trackers (GHHF, GGBL)** — apply a daily-rebalanced gearing model on top of
   the ungeared series: `geared_ret ≈ gearing × underlying_ret − borrowing_cost − fees`,
   with borrowing cost from the RBA cash rate + spread, holding LVR in the 30–40% band.
3. **Calibrate** every synthetic series against the real ETF over its live window.

## Scope (v1)

- **Resolution:** monthly
- **Start date:** January 1995 (captures the full dot-com cycle, GFC, COVID, 2022)
- **Return basis:** total return (distributions reinvested)

## Layout

```
docs/        fund specs, methodology, decisions
src/etfsynth/ reconstruction pipeline
data/raw/     downloaded source series (gitignored)
data/processed/ built synthetic series (gitignored)
```
