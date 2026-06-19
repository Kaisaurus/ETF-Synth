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

ASSETS = ["DHHF", "BGBL", "GHHF", "GGBL"]
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


def full_period_max_dd(level: pd.Series) -> float:
    base = pd.concat([pd.Series([100.0], index=[level.index[0]]), level])
    return (base / base.cummax() - 1.0).min()


def total_return(level: pd.Series) -> float:
    return level.iloc[-1] / 100.0 - 1.0


def cagr(level: pd.Series) -> float:
    return (level.iloc[-1] / 100.0) ** (12.0 / len(level)) - 1.0


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
    out.append(rule)
    out.append("  (TOTAL row = cumulative total return | full-period max drawdown)")
    return "\n".join(out)


def main():
    levels = load_levels()
    rets = monthly_returns(levels)

    blocks = [asset_monthly_table(rets[a], levels[a], a) for a in ASSETS]
    blocks.append(combined_table(levels, rets))
    text = "\n\n\n".join(blocks) + "\n"

    os.makedirs("reports", exist_ok=True)
    out_path = os.path.join("reports", "returns_tables.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(text)
    print(f"(written to {out_path})")


if __name__ == "__main__":
    main()
