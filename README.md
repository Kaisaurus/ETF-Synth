# ETF-Synth

Reconstructed **long-run monthly histories** for popular but young Australian ETFs
(DHHF, BGBL, NDQ, GHHF, GGBL, GNDQ — plus VDHG for comparison), so you can see how they'd
have behaved through the dot-com crash, the GFC and COVID — eras the real funds are too
new to have lived through.

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
| DHHF | +1,558% | 9.33% | −40.9% | May 2007 – Feb 2009 | 6.4 yrs |
| BGBL | +1,913% | 10.00% | −47.4% | Oct 2000 – Feb 2003 | 13.1 yrs |
| NDQ | +8,597% | 15.23% | **−79.1%** | Mar 2000 – Sep 2002 | **17.0 yrs** |
| GHHF | +2,521% | 10.93% | **−59.7%** | May 2007 – Feb 2009 | 7.6 yrs |
| GGBL | +3,135% | 11.67% | **−73.3%** | Oct 2000 – Aug 2011 | 16.2 yrs |
| GNDQ | +21,709% | 18.64% | **−94.3%** | Mar 2000 – Dec 2008 | **19.8 yrs** |

The geared funds compound faster but show brutal worst-case drawdowns. Note BGBL/GGBL's
worst drawdown isn't the GFC — it's the **dot-com crash**: GGBL peaked in Oct 2000, fell
73% and didn't fully recover until Dec 2016, spending over a decade underwater across both
the dot-com bust and the GFC back to back. NDQ/GNDQ (Nasdaq-100) are even more concentrated:
GNDQ's synthetic dot-com drawdown bottomed at −94% in Dec 2008, having never recovered in
between, and only fully recovered in 2019 — nearly two decades underwater. "Time to recover"
= from the pre-crash peak back to break-even.

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
| NDQ | +1,967% | 23.23% | **−29.3%** | Nov 2021 – Dec 2022 | 1.6 yrs |
| GHHF | +1,030% | 18.20% | −27.3% | Jan 2020 – Mar 2020 | 1.1 yrs |
| GGBL | +1,771% | 22.39% | −25.2% | Dec 2021 – Sep 2022 | 1.6 yrs |
| GNDQ | +6,949% | 34.11% | **−43.4%** | Nov 2021 – Dec 2022 | 1.7 yrs |

Post-2012, CAGRs roughly double and drawdowns recover in **under 2 years** instead of 6–16 —
and the worst drawdown is COVID or the 2022 rate shock, not a multi-year crisis. Whether the
1995–2011 era or the 2012–2026 era is more representative of the future is exactly the
judgement call this dataset is meant to help you make, not answer for you.

Annual return (Ret) and calendar-year max drawdown (DD), every year:

```
+------+------------------+------------------+------------------+------------------+------------------+------------------+------------------+
| Year |       DHHF       |       VDHG       |       BGBL       |       NDQ        |       GHHF       |       GGBL       |       GNDQ       |
|      |      Ret       DD|      Ret       DD|      Ret       DD|      Ret       DD|      Ret       DD|      Ret       DD|      Ret       DD|
+------+------------------+------------------+------------------+------------------+------------------+------------------+------------------+
| 1995 |    26.67    -2.52|    24.36    -2.01|    34.22    -2.20|    48.87    -3.04|    36.73    -4.25|    49.11    -3.78|    74.42    -5.05|
| 1996 |    11.19    -3.33|    11.68    -3.22|     9.50    -3.30|    33.51    -5.21|    12.40    -6.75|     9.59    -6.46|    47.79    -8.72|
| 1997 |    30.97    -5.97|    23.45    -5.99|    47.17    -5.37|    47.26   -15.86|    44.62    -9.46|    72.39    -8.86|    69.27   -24.38|
| 1998 |    19.89    -9.90|    17.18    -9.43|    28.74    -9.87|    97.39   -12.13|    26.65   -15.51|    40.55   -15.47|   164.23   -18.93|
| 1999 |    18.79    -3.27|    17.80    -3.43|    17.12    -3.62|    86.04    -8.14|    25.59    -5.30|    22.61    -5.86|   142.77   -12.77|
| 2000 |     3.15    -8.23|     1.27    -5.97|     4.19   -12.38|   -24.92   -42.05|     0.39   -13.15|     1.23   -19.41|   -43.29   -60.98|
| 2001 |     0.02   -13.37|     0.07   -12.58|    -6.99   -16.39|   -27.86   -50.20|    -3.79   -21.94|   -14.22   -26.31|   -46.80   -69.11|
| 2002 |   -19.71   -22.43|   -15.28   -18.42|   -26.67   -29.31|   -43.25   -49.96|   -31.48   -34.39|   -40.82   -43.43|   -61.94   -67.73|
| 2003 |     6.40    -9.72|    11.76    -7.32|    -0.17   -11.91|    11.53    -7.32|     5.92   -15.24|    -4.33   -18.51|    13.53   -11.52|
| 2004 |    17.09    -2.72|    16.93    -1.98|    10.52    -6.30|     6.10   -11.43|    22.85    -4.48|    12.07   -10.76|     5.05   -17.89|
| 2005 |    18.52    -3.75|    15.74    -3.55|    15.05    -4.31|     7.56   -12.81|    24.83    -6.36|    19.05    -7.82|     6.60   -20.28|
| 2006 |    15.95    -5.31|    16.47    -3.61|    10.43    -7.37|    -0.60   -17.33|    20.52    -9.30|    11.55   -12.41|    -5.51   -26.80|
| 2007 |     5.40    -4.93|     8.00    -3.66|    -3.77    -8.04|     6.53    -5.66|     3.74    -8.18|   -10.28   -14.73|     5.25    -9.27|
| 2008 |   -31.79   -31.79|   -31.86   -31.86|   -22.48   -22.48|   -27.05   -27.05|   -47.95   -47.95|   -36.51   -36.51|   -43.22   -43.22|
| 2009 |    12.74   -11.07|    17.73   -11.27|     0.01   -11.98|    19.85    -5.87|    16.28   -17.23|    -3.61   -18.73|    27.63    -9.21|
| 2010 |     0.40    -7.72|     2.82    -8.09|     1.52    -6.76|     6.17    -8.91|    -2.83   -12.44|    -1.22   -11.59|     5.72   -14.26|
| 2011 |    -9.29   -15.17|    -7.92   -14.02|    -4.48   -13.34|     1.79    -9.24|   -16.99   -24.05|   -10.24   -21.36|    -0.64   -15.32|
| 2012 |    15.29    -4.56|    14.30    -4.59|    15.34    -5.00|    16.06    -5.39|    20.98    -7.60|    20.79    -8.49|    21.76    -8.97|
| 2013 |    36.72    -0.12|    28.00    -0.42|    51.15    -1.93|    58.46    -0.15|    57.79    -0.37|    83.04    -3.32|    96.93    -0.38|
| 2014 |    12.07    -2.26|     9.31    -2.26|    16.51    -3.47|    29.72    -6.75|    16.58    -3.65|    23.37    -5.52|    45.35   -10.66|
| 2015 |     7.56    -7.47|     4.58    -7.54|    12.28    -5.46|    22.30    -4.89|     9.18   -11.66|    16.44    -8.64|    32.63    -7.75|
| 2016 |    10.89    -5.66|     9.87    -5.28|    10.23    -5.09|     7.52    -9.39|    14.81    -8.93|    13.52    -8.25|     9.28   -14.68|
| 2017 |    13.11    -2.44|    13.35    -0.90|    13.39    -4.10|    22.27    -5.42|    18.80    -3.99|    18.90    -6.55|    33.56    -8.56|
| 2018 |    -0.31   -10.66|    -2.11    -9.76|     1.90   -11.85|    10.36   -15.36|    -2.44   -16.58|     0.62   -18.38|    13.45   -23.34|
| 2019 |    25.86    -2.44|    23.80    -2.03|    28.22    -4.61|    38.76    -6.80|    39.98    -3.87|    43.58    -7.22|    62.00   -10.57|
| 2020 |     5.26   -18.06|     7.01   -17.82|     7.21   -13.94|    34.83    -5.02|     5.72   -27.29|     9.17   -21.23|    55.78    -7.80|
| 2021 |    22.79    -2.81|    18.51    -2.76|    28.62    -3.13|    34.80    -4.68|    35.95    -4.37|    45.58    -4.88|    56.02    -7.24|
| 2022 |    -8.66   -13.89|    -9.63   -15.20|   -12.85   -16.72|   -28.35   -28.35|   -15.05   -21.43|   -21.21   -25.20|   -42.20   -42.20|
| 2023 |    18.21    -5.64|    16.52    -6.23|    23.23    -5.28|    53.77    -5.11|    25.44    -9.07|    33.50    -8.56|    86.61    -8.28|
| 2024 |    22.49    -3.07|    17.59    -3.08|    28.87    -3.61|    38.12    -3.90|    32.27    -4.96|    42.49    -5.82|    58.51    -6.24|
| 2025 |    12.25    -5.25|    12.90    -4.64|    13.37    -6.39|    11.59   -11.15|    16.02    -8.59|    17.52   -10.46|    14.32   -17.50|
| 2026 |     5.09    -4.27|     5.42    -4.78|     6.27    -4.69|    14.03    -8.57|     6.22    -6.81|     7.94    -7.85|    19.68   -13.58|
+------+------------------+------------------+------------------+------------------+------------------+------------------+------------------+
|TOTAL |  1558.46   -40.91|  1284.93   -41.14|  1912.62   -47.36|  8596.78   -79.08|  2520.81   -59.70|  3135.50   -73.27| 21708.95   -94.33|
| CAGR |     9.33         |     8.70         |    10.00         |    15.23         |    10.93         |    11.67         |    18.64         |
+------+------------------+------------------+------------------+------------------+------------------+------------------+------------------+
```

Full per-month grids for every fund: **[reports/returns_tables.txt](reports/returns_tables.txt)**.
Plain-language write-up: **[SUMMARY.md](SUMMARY.md)**.

## Funds in scope

| Ticker | Fund | Type | Inception | MER |
|--------|------|------|-----------|-----|
| DHHF | Diversified All Growth | Multi-asset (fund-of-ETFs, ~100% growth) | Dec 2019 | 0.19% |
| VDHG | Vanguard Diversified High Growth | Multi-asset (90% growth / 10% bonds) | Nov 2017 | 0.27% |
| BGBL | Global Shares | Index (Solactive GBS Dev Mkts ex-Aus L&M Cap) | May 2023 | 0.08% |
| NDQ | Nasdaq 100 | Index (Nasdaq-100) | May 2015 | 0.38% |
| GHHF | Wealth Builder Diversified All Growth Geared | Internally geared DHHF, 30–40% LVR | Apr 2024 | 0.35% |
| GGBL | Wealth Builder Global Shares Geared | Internally geared BGBL, 30–40% LVR | ~Oct 2025 | ~0.35% |
| GNDQ | Wealth Builder Nasdaq 100 Geared | Internally geared NDQ, 30–40% LVR | Oct 2024 | 0.50% |

Full specs, sleeve weights and data sources: **[docs/fund_specs.md](docs/fund_specs.md)**.

## Method

1. **Ungeared funds (DHHF, BGBL, NDQ, VDHG)** — blend long-history proxy funds into each
   fund's asset allocation, convert overseas sleeves to AUD, subtract fees.
2. **Geared funds (GHHF, GGBL, GNDQ)** — apply ~1.5× leverage to the ungeared basket and
   subtract borrowing cost (RBA cash rate + spread), matching the 30–40% LVR band.
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
