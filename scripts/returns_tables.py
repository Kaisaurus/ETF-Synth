"""Plain-text return/drawdown tables from the synthetic series.

Per asset: monthly returns (years x Jan..Dec) with a compounded annual column.
Comparison: annual return matrix and intra-year max-drawdown matrix (years x assets).

All values in percent. Prereq: scripts/build_synthetic.py has written data/processed.
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


def _fmt(x, w=7):
    return " " * w if pd.isna(x) else f"{x*100:>{w}.2f}"


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
    """Worst peak-to-trough drawdown occurring during `year`, with the running
    peak anchored at the prior year-end so a fall starting in January is fully
    counted (running peak still updates on new highs made mid-year)."""
    prior = level[level.index.year < year]
    anchor = prior.iloc[-1:] if len(prior) else level.iloc[:0]
    window = pd.concat([anchor, level[level.index.year == year]])
    if window.empty:
        return float("nan")
    dd = window / window.cummax() - 1.0
    return dd[dd.index.year == year].min()


def asset_monthly_table(rets: pd.Series, asset: str) -> str:
    lines = [f"=== {asset} - monthly total return (%), annual compounded ==="]
    header = "Year " + "".join(f"{m:>7}" for m in MONTHS) + f"{'Annual':>9}"
    lines.append(header)
    lines.append("-" * len(header))
    for year, grp in rets.groupby(rets.index.year):
        by_month = {d.month: v for d, v in grp.items()}
        cells = "".join(_fmt(by_month.get(m + 1, float("nan"))) for m in range(12))
        ann = annual_return(grp)
        lines.append(f"{year:<5}{cells}{ann*100:>9.2f}")
    return "\n".join(lines)


def comparison_tables(levels: pd.DataFrame, rets: pd.DataFrame) -> str:
    years = sorted(set(levels.index.year))

    ret_rows, dd_rows = [], []
    for y in years:
        rmask = rets.index.year == y
        ret_rows.append([annual_return(rets[a][rmask]) for a in ASSETS])
        dd_rows.append([calendar_year_max_dd(levels[a], y) for a in ASSETS])
    ret_df = pd.DataFrame(ret_rows, index=years, columns=ASSETS)
    dd_df = pd.DataFrame(dd_rows, index=years, columns=ASSETS)

    def matrix(df, title):
        out = [title]
        head = "Year " + "".join(f"{a:>9}" for a in ASSETS)
        out.append(head)
        out.append("-" * len(head))
        for y in df.index:
            out.append(f"{y:<5}" + "".join(f"{df.loc[y, a]*100:>9.2f}" for a in ASSETS))
        return "\n".join(out)

    return (matrix(ret_df, "=== Annual return (%) - assets x years ===") + "\n\n" +
            matrix(dd_df, "=== Calendar-year max drawdown (%) - assets x years ==="))


def main():
    levels = load_levels()
    rets = monthly_returns(levels)

    blocks = [asset_monthly_table(rets[a], a) for a in ASSETS]
    blocks.append(comparison_tables(levels, rets))
    text = "\n\n\n".join(blocks) + "\n"

    os.makedirs("reports", exist_ok=True)
    out_path = os.path.join("reports", "returns_tables.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(text)
    print(f"(written to {out_path})")


if __name__ == "__main__":
    main()
