# Synthetic long-run history for DHHF / BGBL / GHHF / GGBL

These four Betashares ETFs are popular but **young** — DHHF launched Dec 2019, BGBL
May 2023, GHHF Apr 2024, GGBL Oct 2025. So there's no way to see how they'd have
behaved through the dot-com crash, the GFC, or COVID. This project **reconstructs
monthly total-return histories back to January 1995** so you can.

Everything is built from **free public data**.

## How the data was procured

- **Real ETF prices** (for validation): Yahoo Finance, since each fund's inception.
- **Long-history building blocks** (the actual history): low-cost index funds whose
  adjusted close is total return (dividends reinvested), via Yahoo Finance —
  - US shares: Vanguard VTSMX (1992)
  - Emerging markets: Vanguard VEIEX (1994)
  - Developed ex-US: Vanguard VTMGX / VGTSX (spliced)
  - Australian shares: SPDR STW (since 2001) + All Ords price index with a dividend
    add-back before that
- **AUD/USD exchange rate** and the **RBA cash rate proxy**: FRED (free).

## How it was built

1. Blend the building blocks into each fund's published asset allocation.
2. Convert overseas returns into AUD (the funds are unhedged).
3. Subtract each fund's management fee.
4. For the geared funds (GHHF, GGBL): apply ~1.5x leverage and subtract borrowing
   cost (cash rate + spread), matching their 30–40% LVR.

## Does it actually match the real funds?

Yes — checked against each fund's real returns over the period it has existed.
Monthly-return correlation: **DHHF 0.97, BGBL 0.92, GHHF 0.94, GGBL 0.99**.

## Headline results (Jan 1995 → Jun 2026, total return, AUD)

| Fund | Total return | CAGR | Worst drawdown |
|------|-------------:|-----:|---------------:|
| DHHF | +1,547% | 9.3% | −41% |
| BGBL | +1,892% | 10.0% | −47% |
| GHHF | +2,493% | 10.9% | **−60%** |
| GGBL | +3,086% | 11.6% | **−73%** |

The geared funds compound faster but the synthetic GFC drawdowns (−60% / −73%) show
the risk their short real track records have never had to display.

## Caveats (please read before using)

- This is **synthetic/reconstructed** data, not the real funds before inception.
- Pre-2001 leans more on proxies, so treat the earliest years as softer.
- The geared series are the most assumption-sensitive.
- Total return basis; **franking credits are not included**.
- Not financial advice — for research/curiosity.

Code, full monthly tables, and methodology: see the repo.
