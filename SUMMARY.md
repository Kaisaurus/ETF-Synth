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
Monthly-return correlation: **DHHF 0.97, VDHG 0.97, BGBL 0.92, GHHF 0.94, GGBL 0.99**.

## Headline results (Jan 1995 → Jun 2026, total return, AUD)

| Fund | Total return | CAGR | Worst drawdown | Drawdown period | Time to recover |
|------|-------------:|-----:|---------------:|:----------------:|-----------------:|
| VDHG | +1,285% | 8.8% | −41% | Oct 2007 – Feb 2009 | 5.9 yrs |
| DHHF | +1,558% | 9.4% | −41% | May 2007 – Feb 2009 | 6.4 yrs |
| BGBL | +1,913% | 10.0% | −47% | Oct 2000 – Feb 2003 | 13.1 yrs |
| GHHF | +2,520% | 11.0% | **−60%** | May 2007 – Feb 2009 | 7.6 yrs |
| GGBL | +3,135% | 11.6% | **−73%** | Oct 2000 – Aug 2011 | **16.2 yrs** |

(VDHG = Vanguard Diversified High Growth, included as a comparison; it holds 10% bonds.)
"Time to recover" = years from the pre-crash peak back to break-even.

The geared funds compound faster but show brutal worst-case drawdowns. Note BGBL/GGBL's
worst drawdown is actually the **dot-com crash**, not the GFC: GGBL peaked Oct 2000, fell
73%, and didn't fully recover until Dec 2016 — over a decade underwater spanning both
the dot-com bust and the GFC back to back.

## Same table, post-2012 only

1995–2011 was an unusually brutal double-crisis stretch (dot-com + GFC, back to back).
Splitting at 2012 — roughly when central banks settled into the sustained low-rate/QE era —
shows a very different market:

| Fund | Total return | CAGR | Worst drawdown | Drawdown period | Time to recover |
|------|-------------:|-----:|---------------:|:----------------:|-----------------:|
| VDHG | +372% | 11.3% | −17.8% | Jan 2020 – Mar 2020 | 0.8 yrs |
| DHHF | +503% | 13.2% | −18.1% | Jan 2020 – Mar 2020 | 0.8 yrs |
| BGBL | +756% | 16.0% | −16.7% | Dec 2021 – Jun 2022 | 1.5 yrs |
| GHHF | +1,030% | 18.2% | −27.3% | Jan 2020 – Mar 2020 | 1.1 yrs |
| GGBL | +1,771% | 22.4% | −25.2% | Dec 2021 – Sep 2022 | 1.6 yrs |

Post-2012, CAGRs roughly double and recoveries take under 2 years instead of 6–16 — the
worst hit is COVID or the 2022 rate shock, not a multi-year crisis. Which era is more
representative going forward is a judgement call, not something this data answers for you.

## Caveats (please read before using)

- This is **synthetic/reconstructed** data, not the real funds before inception.
- Pre-2001 leans more on proxies, so treat the earliest years as softer.
- The geared series are the most assumption-sensitive.
- Total return basis; **franking credits are not included**.
- Not financial advice — for research/curiosity.

Code, full monthly tables, and methodology: see the repo.
