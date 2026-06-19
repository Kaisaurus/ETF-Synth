# ETF-Synth

Reconstructed **long-run monthly histories** for popular but young Australian ETFs
(DHHF, BGBL, GHHF, GGBL — plus VDHG for comparison), so you can see how they'd have
behaved through the dot-com crash, the GFC and COVID — eras the real funds are too new
to have lived through.

## How the data is used

- Built **entirely from free public data** — Yahoo Finance (prices) and FRED (FX, rates).
- Each fund's asset sleeves are stood in by **long-history, low-cost index funds** whose
  adjusted close is total return (dividends reinvested); overseas sleeves are converted
  to AUD (the funds are unhedged), then fees — and for the geared funds, borrowing costs —
  are modelled on top.
- **Monthly resolution, from Jan 1995, total-return basis.**
- Every synthetic series is **calibrated against the real fund** over the window it has
  actually existed (monthly-return correlation **0.92–0.97**, geared funds up to 0.99).

## Caveats (please read)

- This is **synthetic / reconstructed** data, not the real funds before their inception.
- Pre-2001 leans more on proxy splices; the **geared funds** and **VDHG** (hedging + a bond
  proxy) are the most assumption-sensitive.
- Total-return basis; **franking credits are not included.**
- For research / curiosity — **not financial advice.**

## Results (Jan 1995 – Jun 2026, total return, AUD)

| Fund | Total return | CAGR | Worst drawdown | Drawdown period | Time to recover |
|------|-------------:|-----:|---------------:|:----------------:|-----------------:|
| VDHG | +1,285% | 8.70% | −41.1% | Oct 2007 – Feb 2009 | 5.9 yrs |
| DHHF | +1,558% | 9.32% | −40.9% | May 2007 – Feb 2009 | 6.4 yrs |
| BGBL | +1,913% | 10.00% | −47.4% | Oct 2000 – Feb 2003 | 13.1 yrs |
| GHHF | +2,520% | 10.92% | **−59.7%** | May 2007 – Feb 2009 | 7.6 yrs |
| GGBL | +3,135% | 11.67% | **−73.3%** | Oct 2000 – Aug 2011 | **16.2 yrs** |

The geared funds compound faster but show brutal worst-case drawdowns. Note BGBL/GGBL's
worst drawdown isn't the GFC — it's the **dot-com crash**: GGBL peaked in Oct 2000, fell
73% and didn't fully recover until Dec 2016, spending over a decade underwater across both
the dot-com bust and the GFC back to back. "Time to recover" = from the pre-crash peak back
to break-even.

### Same table, post-2012 only

1995–2011 was an unusually brutal stretch — the dot-com crash and the GFC back to back,
with some funds never setting a new high in between. Splitting the history at 2012 (roughly
when central banks settled into sustained low-rate/QE policy and that double-crisis finally
resolved) shows a very different-looking market:

| Fund | Total return | CAGR | Worst drawdown | Drawdown period | Time to recover |
|------|-------------:|-----:|---------------:|:----------------:|-----------------:|
| VDHG | +372% | 11.29% | −17.8% | Jan 2020 – Mar 2020 | 0.8 yrs |
| DHHF | +503% | 13.19% | −18.1% | Jan 2020 – Mar 2020 | 0.8 yrs |
| BGBL | +756% | 15.96% | −16.7% | Dec 2021 – Jun 2022 | 1.5 yrs |
| GHHF | +1,030% | 18.20% | −27.3% | Jan 2020 – Mar 2020 | 1.1 yrs |
| GGBL | +1,771% | 22.39% | −25.2% | Dec 2021 – Sep 2022 | 1.6 yrs |

Post-2012, CAGRs roughly double and drawdowns recover in **under 2 years** instead of 6–16 —
and the worst drawdown is COVID or the 2022 rate shock, not a multi-year crisis. Whether the
1995–2011 era or the 2012–2026 era is more representative of the future is exactly the
judgement call this dataset is meant to help you make, not answer for you.

Annual return (Ret) and calendar-year max drawdown (DD), every year:

```
+------+------------------+------------------+------------------+------------------+------------------+
| Year |       DHHF       |       VDHG       |       BGBL       |       GHHF       |       GGBL       |
|      |      Ret       DD|      Ret       DD|      Ret       DD|      Ret       DD|      Ret       DD|
+------+------------------+------------------+------------------+------------------+------------------+
| 1995 |    26.67    -2.52|    24.36    -2.01|    34.22    -2.20|    36.73    -4.25|    49.11    -3.78|
| 1996 |    11.19    -3.33|    11.68    -3.22|     9.50    -3.30|    12.40    -6.75|     9.59    -6.46|
| 1997 |    30.97    -5.97|    23.45    -5.99|    47.17    -5.37|    44.62    -9.46|    72.39    -8.86|
| 1998 |    19.89    -9.90|    17.18    -9.43|    28.74    -9.87|    26.65   -15.51|    40.55   -15.47|
| 1999 |    18.79    -3.27|    17.80    -3.43|    17.12    -3.62|    25.59    -5.30|    22.61    -5.86|
| 2000 |     3.15    -8.23|     1.27    -5.97|     4.19   -12.38|     0.39   -13.15|     1.23   -19.41|
| 2001 |     0.02   -13.37|     0.07   -12.58|    -6.99   -16.39|    -3.79   -21.94|   -14.22   -26.31|
| 2002 |   -19.71   -22.43|   -15.28   -18.42|   -26.67   -29.31|   -31.48   -34.39|   -40.82   -43.43|
| 2003 |     6.40    -9.72|    11.76    -7.32|    -0.17   -11.91|     5.92   -15.24|    -4.33   -18.51|
| 2004 |    17.09    -2.72|    16.93    -1.98|    10.52    -6.30|    22.85    -4.48|    12.07   -10.76|
| 2005 |    18.52    -3.75|    15.74    -3.55|    15.05    -4.31|    24.83    -6.36|    19.05    -7.82|
| 2006 |    15.95    -5.31|    16.47    -3.61|    10.43    -7.37|    20.52    -9.30|    11.55   -12.41|
| 2007 |     5.40    -4.93|     8.00    -3.66|    -3.77    -8.04|     3.74    -8.18|   -10.28   -14.73|
| 2008 |   -31.79   -31.79|   -31.86   -31.86|   -22.48   -22.48|   -47.95   -47.95|   -36.51   -36.51|
| 2009 |    12.74   -11.07|    17.73   -11.27|     0.01   -11.98|    16.28   -17.23|    -3.61   -18.73|
| 2010 |     0.40    -7.72|     2.82    -8.09|     1.52    -6.76|    -2.83   -12.44|    -1.22   -11.59|
| 2011 |    -9.29   -15.17|    -7.92   -14.02|    -4.48   -13.34|   -16.99   -24.05|   -10.24   -21.36|
| 2012 |    15.29    -4.56|    14.30    -4.59|    15.34    -5.00|    20.98    -7.60|    20.79    -8.49|
| 2013 |    36.72    -0.12|    28.00    -0.42|    51.15    -1.93|    57.79    -0.37|    83.04    -3.32|
| 2014 |    12.07    -2.26|     9.31    -2.26|    16.51    -3.47|    16.58    -3.65|    23.37    -5.52|
| 2015 |     7.56    -7.47|     4.58    -7.54|    12.28    -5.46|     9.18   -11.66|    16.44    -8.64|
| 2016 |    10.89    -5.66|     9.87    -5.28|    10.23    -5.09|    14.81    -8.93|    13.52    -8.25|
| 2017 |    13.11    -2.44|    13.35    -0.90|    13.39    -4.10|    18.80    -3.99|    18.90    -6.55|
| 2018 |    -0.31   -10.66|    -2.11    -9.76|     1.90   -11.85|    -2.44   -16.58|     0.62   -18.38|
| 2019 |    25.86    -2.44|    23.80    -2.03|    28.22    -4.61|    39.98    -3.87|    43.58    -7.22|
| 2020 |     5.26   -18.06|     7.01   -17.82|     7.21   -13.94|     5.72   -27.29|     9.17   -21.23|
| 2021 |    22.79    -2.81|    18.51    -2.76|    28.62    -3.13|    35.95    -4.37|    45.58    -4.88|
| 2022 |    -8.66   -13.89|    -9.63   -15.20|   -12.85   -16.72|   -15.05   -21.43|   -21.21   -25.20|
| 2023 |    18.21    -5.64|    16.52    -6.23|    23.23    -5.28|    25.44    -9.07|    33.50    -8.56|
| 2024 |    22.49    -3.07|    17.59    -3.08|    28.87    -3.61|    32.27    -4.96|    42.49    -5.82|
| 2025 |    12.25    -5.25|    12.90    -4.64|    13.37    -6.39|    16.02    -8.59|    17.52   -10.46|
| 2026 |     5.07    -4.27|     5.40    -4.78|     6.27    -4.69|     6.20    -6.81|     7.94    -7.85|
+------+------------------+------------------+------------------+------------------+------------------+
|TOTAL |  1558.23   -40.91|  1284.74   -41.14|  1912.62   -47.36|  2520.27   -59.70|  3135.49   -73.27|
| CAGR |     9.32         |     8.70         |    10.00         |    10.92         |    11.67         |
+------+------------------+------------------+------------------+------------------+------------------+
```

Full per-month grids for every fund: **[reports/returns_tables.txt](reports/returns_tables.txt)**.
Plain-language write-up: **[SUMMARY.md](SUMMARY.md)**.

## Funds in scope

| Ticker | Fund | Type | Inception | MER |
|--------|------|------|-----------|-----|
| DHHF | Diversified All Growth | Multi-asset (fund-of-ETFs, ~100% growth) | Dec 2019 | 0.19% |
| VDHG | Vanguard Diversified High Growth | Multi-asset (90% growth / 10% bonds) | Nov 2017 | 0.27% |
| BGBL | Global Shares | Index (Solactive GBS Dev Mkts ex-Aus L&M Cap) | May 2023 | 0.08% |
| GHHF | Wealth Builder Diversified All Growth Geared | Internally geared DHHF, 30–40% LVR | Apr 2024 | 0.35% |
| GGBL | Wealth Builder Global Shares Geared | Internally geared BGBL, 30–40% LVR | ~Oct 2025 | ~0.35% |

Full specs, sleeve weights and data sources: **[docs/fund_specs.md](docs/fund_specs.md)**.

## Method

1. **Ungeared funds (DHHF, BGBL, VDHG)** — blend long-history proxy funds into each fund's
   asset allocation, convert overseas sleeves to AUD, subtract fees.
2. **Geared funds (GHHF, GGBL)** — apply ~1.5× leverage to the ungeared basket and subtract
   borrowing cost (RBA cash rate + spread), matching the 30–40% LVR band.
3. **Calibrate** every series against the real ETF over its live window.

## Reproduce

```
pip install -r requirements.txt
python scripts/fetch_data.py        # download free source series -> data/raw/
python scripts/build_synthetic.py   # build + calibrate -> data/processed/
python scripts/returns_tables.py    # render tables -> reports/returns_tables.txt
```

```
docs/            fund specs, methodology, decisions
src/etfsynth/    reconstruction pipeline
scripts/         fetch / build / report entry points
reports/         generated tables
```
