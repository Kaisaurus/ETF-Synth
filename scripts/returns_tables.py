"""Plain-text return/drawdown tables from the synthetic series.

Per asset: monthly returns (years x Jan..Dec) + compounded annual column, with a
TOTAL (cumulative) and CAGR footer. Combined table: each asset's annual return and
calendar-year max drawdown side by side, with a TOTAL (cumulative return / full-period
max drawdown) footer. All values in percent; ASCII box borders.

Prereq: scripts/build_synthetic.py has written data/processed.
Run: python scripts/returns_tables.py
"""
from __future__ import annotations

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from etfsynth import config  # noqa: E402

ASSETS = ["DHHF", "VDHG", "BGBL", "NDQ", "GHHF", "GGBL", "GNDQ"]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def load_levels() -> pd.DataFrame:
    path = os.path.join(config.PROCESSED_DIR, "synth_all.csv")
    df = pd.read_csv(path, parse_dates=["date"]).set_index("date")
    return df[ASSETS]


def monthly_returns(levels: pd.DataFrame) -> pd.DataFrame:
    prior = levels.shift()
    prior.iloc[0] = 100.0          # implied base level before first month
    return levels / prior - 1.0


def annual_return(rets_year: pd.Series) -> float:
    return (1.0 + rets_year.dropna()).prod() - 1.0


def calendar_year_max_dd(level: pd.Series, year: int) -> float:
    """Worst peak-to-trough drawdown during `year`, running peak anchored at the
    prior year-end so a fall starting in January is fully counted."""
    prior = level[level.index.year < year]
    anchor = prior.iloc[-1:] if len(prior) else level.iloc[:0]
    window = pd.concat([anchor, level[level.index.year == year]])
    if window.empty:
        return float("nan")
    dd = window / window.cummax() - 1.0
    return dd[dd.index.year == year].min()


def period_metrics(level: pd.Series, start=None) -> dict:
    """Total return / CAGR / max drawdown / drawdown window for `level` from
    `start` (inclusive) to its end. start=None covers the whole series, anchored
    at the synthetic base of 100; a real `start` is anchored at the last value
    before it (the "entry price" for an investor starting then) - the same trick
    used in calendar_year_max_dd, generalised to an arbitrary cutoff."""
    sub = level if start is None else level[level.index >= start]
    prior = level[level.index < sub.index[0]]
    anchor = float(prior.iloc[-1]) if len(prior) else 100.0

    n = len(sub)
    total = sub.iloc[-1] / anchor - 1.0
    cg = (sub.iloc[-1] / anchor) ** (12.0 / n) - 1.0

    base = pd.concat([pd.Series([anchor], index=[sub.index[0]]), sub])
    run_max = base.cummax()
    dd = base / run_max - 1.0
    trough_date = dd.idxmin()
    peak_level = run_max.loc[trough_date]
    peak_date = base[:trough_date].idxmax()
    after = base[base.index > trough_date]
    recovered = after[after >= peak_level]
    recovery_date = recovered.index[0] if not recovered.empty else None

    return {"total_return": total, "cagr": cg, "max_dd": dd.min(),
            "peak_date": peak_date, "trough_date": trough_date,
            "recovery_date": recovery_date}


def total_return(level: pd.Series) -> float:
    return period_metrics(level)["total_return"]


def cagr(level: pd.Series) -> float:
    return period_metrics(level)["cagr"]


def full_period_max_dd(level: pd.Series) -> float:
    return period_metrics(level)["max_dd"]


# ---------------------------------------------------------------------------
# Per-asset monthly table (bordered)
# ---------------------------------------------------------------------------
def asset_monthly_table(rets: pd.Series, level: pd.Series, asset: str) -> str:
    def cell(x):
        return "" if pd.isna(x) else f"{x*100:.2f}"

    rule = "+" + "-" * 6 + "+" + "-" * 85 + "+" + "-" * 9 + "+"
    mhead = " " + " ".join(f"{m:>6}" for m in MONTHS) + " "
    out = [f"=== {asset} - monthly total return (%), annual compounded ===",
           rule,
           "|" + f" {'Year':>4} " + "|" + mhead + "|" + f" {'Annual':>7} " + "|",
           rule]

    for year, grp in rets.groupby(rets.index.year):
        by_month = {d.month: v for d, v in grp.items()}
        vals = [cell(by_month.get(m + 1)) for m in range(12)]
        block = " " + " ".join(f"{v:>6}" for v in vals) + " "
        ann = f"{annual_return(grp)*100:.2f}"
        out.append("|" + f" {year:>4} " + "|" + block + "|" + f" {ann:>7} " + "|")

    out.append(rule)
    blank = " " + " ".join(f"{'':>6}" for _ in range(12)) + " "
    tot = f"{total_return(level)*100:.2f}"
    cg = f"{cagr(level)*100:.2f}"
    out.append("|" + f" {'TOT':>4} " + "|" + blank + "|" + f" {tot:>7} " + "|")
    out.append("|" + f" {'CAGR':>4} " + "|" + blank + "|" + f" {cg:>7} " + "|")
    out.append(rule)
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Headline summary table
# ---------------------------------------------------------------------------
def _format_period(peak_date, trough_date) -> str:
    return f"{peak_date.strftime('%b %Y')} - {trough_date.strftime('%b %Y')}"


def _format_recovery(peak_date, recovery_date) -> str:
    if recovery_date is None:
        return "not yet"
    days = (recovery_date - peak_date).days
    return f"{days:,}d ({days/365.25:.1f}y)"


def summary_table(levels: pd.DataFrame, start: str | None = None) -> str:
    """`levels` must be the full-history DataFrame (pre-cutoff values are needed
    to anchor a sub-period); pass `start` (e.g. "2012-01-01") for a sub-period."""
    sub_index = levels.index if start is None else levels.index[levels.index >= start]
    range_start = sub_index.min().strftime("%b %Y")
    end = sub_index.max().strftime("%b %Y")
    rule = ("+" + "-" * 7 + "+" + "-" * 15 + "+" + "-" * 9 + "+" + "-" * 15
            + "+" + "-" * 21 + "+" + "-" * 18 + "+")
    out = [f"=== Summary ({range_start} - {end}, total return, AUD) ===", rule,
           "|" + f" {'Fund':<5} " + "|" + f" {'Total return':>13} " + "|"
           + f" {'CAGR':>7} " + "|" + f" {'Max DD':>13} " + "|"
           + f" {'Drawdown period':>19} " + "|"
           + f" {'Max DD recovery':>16} " + "|", rule]
    for a in ASSETS:
        m = period_metrics(levels[a], start=start)
        tr, cg, dd = m["total_return"] * 100, m["cagr"] * 100, m["max_dd"] * 100
        period = _format_period(m["peak_date"], m["trough_date"])
        rec = _format_recovery(m["peak_date"], m["recovery_date"])
        out.append("|" + f" {a:<5} " + "|" + f" {tr:>11.1f}%  " + "|"
                   + f" {cg:>6.2f}% " + "|" + f" {dd:>11.1f}%  " + "|"
                   + f" {period:>19} " + "|"
                   + f" {rec:>16} " + "|")
    out.append(rule)
    out.append("  (Drawdown period = pre-crash peak to trough; "
               "Max DD recovery = calendar days peak to full recovery)")
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Combined return + drawdown table (bordered, grouped by asset)
# ---------------------------------------------------------------------------
def combined_table(levels: pd.DataFrame, rets: pd.DataFrame) -> str:
    years = sorted(set(levels.index.year))
    grp = "-" * 18
    rule = "+" + "-" * 6 + "+" + ("+".join([grp] * len(ASSETS))) + "+"

    name_hdr = "|" + f"{'Year':^6}" + "|" + "|".join(f"{a:^18}" for a in ASSETS) + "|"
    sub_hdr = "|" + " " * 6 + "|" + "|".join(f"{'Ret':>9}{'DD':>9}" for _ in ASSETS) + "|"

    out = ["=== Annual return & calendar-year max drawdown (%) - all assets ===",
           rule, name_hdr, sub_hdr, rule]

    for y in years:
        rmask = rets.index.year == y
        cells = []
        for a in ASSETS:
            r = annual_return(rets[a][rmask]) * 100
            dd = calendar_year_max_dd(levels[a], y) * 100
            cells.append(f"{r:>9.2f}{dd:>9.2f}")
        out.append("|" + f"{y:^6}" + "|" + "|".join(cells) + "|")

    out.append(rule)
    tot_cells = []
    for a in ASSETS:
        tr = total_return(levels[a]) * 100
        mdd = full_period_max_dd(levels[a]) * 100
        tot_cells.append(f"{tr:>9.2f}{mdd:>9.2f}")
    out.append("|" + f"{'TOTAL':^6}" + "|" + "|".join(tot_cells) + "|")
    cagr_cells = [f"{cagr(levels[a])*100:>9.2f}{'':>9}" for a in ASSETS]
    out.append("|" + f"{'CAGR':^6}" + "|" + "|".join(cagr_cells) + "|")
    out.append(rule)
    out.append("  (TOTAL = cumulative return | full-period max drawdown; "
               "CAGR = annualised return)")
    return "\n".join(out)


def main():
    levels = load_levels()
    rets = monthly_returns(levels)

    blocks = [summary_table(levels),
              summary_table(levels, start="2012-01-01"),
              combined_table(levels, rets)]
    blocks += [asset_monthly_table(rets[a], levels[a], a) for a in ASSETS]
    text = "\n\n\n".join(blocks) + "\n"

    os.makedirs("reports", exist_ok=True)
    out_path = os.path.join("reports", "returns_tables.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(text)
    print(f"(written to {out_path})")


if __name__ == "__main__":
    main()
