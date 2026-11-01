"""Two more charts for the README (each series on its own, in its own units).

figures/guard_pay.png      monthly scheduled earnings of security guards, building cleaners and (from 2020) other
                           protective service workers, Japan
                           (workers who are not position holders, comparable across 2019 and 2020)
figures/minimum_wage.png   national weighted average of the prefecture minimum wages
"""
import csv
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

plt.rcParams["font.family"] = ["Noto Sans CJK JP", "DejaVu Sans"]

ROOT = os.path.join(os.path.dirname(__file__), "..")
BLUE, ORANGE, GREEN = "#2a78d6", "#eb6834", "#3d8f5a"
INK, MUTED, GRID, SURFACE = "#1f1f1e", "#6b6a63", "#e4e3de", "#fcfcfb"


def style(ax, title, ylabel):
    ax.set_facecolor(SURFACE)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(colors=MUTED, labelsize=9)
    ax.set_title(title, loc="left", color=INK, fontsize=12, pad=12)
    ax.set_ylabel(ylabel, color=MUTED, fontsize=9)


def pay():
    rows = list(csv.DictReader(open(os.path.join(ROOT, "data/clean/pay_by_prefecture.csv"), encoding="utf-8")))
    fig, ax = plt.subplots(figsize=(8, 4.5), facecolor=SURFACE)
    for occ, c, label in (("security_guards", BLUE, "Security guards"), ("building_cleaners", ORANGE, "Building cleaners"),
                          ("other_protective", GREEN, "Other protective\nservice workers")):
        pts = sorted((int(r["survey_year"]), float(r["scheduled_earnings_kyen"]) * 1000) for r in rows
                     if r["occupation"] == occ and r["pref_code"] == "00" and r["sex"] == "total"
                     and r["position_holders"] == "excluded")
        for seg in ([p for p in pts if p[0] <= 2019], [p for p in pts if p[0] >= 2020]):
            ax.plot([p[0] for p in seg], [p[1] for p in seg], color=c, linewidth=2, marker="o", markersize=5)
        dy = {"security_guards": -6, "other_protective": 16}.get(occ, 0)
        ax.annotate(f"{label}: ¥{pts[-1][1]:,.0f}", (pts[-1][0], pts[-1][1]), xytext=(8, dy),
                    textcoords="offset points", va="center", color=INK, fontsize=9)
    ax.axvline(2019.5, color=MUTED, linewidth=1, linestyle="--")
    ax.text(2019.6, 95000, "New occupation list\nand estimation method\nfrom 2020", color=MUTED, fontsize=7.5, va="top")
    ax.set_xlim(2011.5, 2028.8)
    ax.set_xticks(range(2012, 2026, 2))
    ax.set_ylim(0, 260000)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"¥{v:,.0f}"))
    style(ax, "Monthly scheduled earnings, Japan, full-time workers, both sexes",
          "Yen per month (June; excludes overtime and bonuses)")
    fig.text(0.01, 0.075, "Workers who are not position holders (役職者), the coverage MHLW used for occupations to 2019. "
             "Lines are broken at the 2020 survey change.", color=MUTED, fontsize=7.5)
    fig.text(0.01, 0.045, "Other protective service workers (from 2020) is the occupation in which MHLW places traffic and "
             "crowd guards; security guards cover facility and personal guarding.", color=MUTED, fontsize=7.5)
    fig.text(0.01, 0.01, "Source: MHLW, 賃金構造基本統計調査 (Basic Survey on Wage Structure), 2012-2025.",
             color=MUTED, fontsize=7.5)
    fig.tight_layout(rect=(0, 0.1, 1, 1))
    fig.savefig(os.path.join(ROOT, "figures/guard_pay.png"), dpi=150)


def minwage():
    rows = list(csv.DictReader(open(os.path.join(ROOT, "data/clean/minimum_wage_by_prefecture.csv"), encoding="utf-8")))
    pts = sorted((int(r["fiscal_year"]), int(r["hourly_yen"])) for r in rows
                 if r["pref_code"] == "00" and int(r["fiscal_year"]) >= 2012)
    fig, ax = plt.subplots(figsize=(8, 4.5), facecolor=SURFACE)
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=BLUE, linewidth=2, marker="o", markersize=5)
    ax.annotate(f"¥{pts[-1][1]:,}", (pts[-1][0], pts[-1][1]), xytext=(8, 0), textcoords="offset points",
                va="center", color=INK, fontsize=9)
    ax.annotate(f"¥{pts[0][1]:,}", (pts[0][0], pts[0][1]), xytext=(-8, 0), textcoords="offset points",
                ha="right", va="center", color=MUTED, fontsize=8)
    ax.set_xlim(2010.5, 2027.8)
    ax.set_xticks(range(2012, 2027, 2))
    ax.set_ylim(0, 1300)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"¥{v:,.0f}"))
    style(ax, "Minimum wage, national weighted average of the 47 prefectures", "Yen per hour")
    fig.text(0.01, 0.01, "Source: MHLW, 地域別最低賃金改定状況, FY2012-FY2026 (each year's revision takes effect "
             "from the end of September onwards).", color=MUTED, fontsize=7.5)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(os.path.join(ROOT, "figures/minimum_wage.png"), dpi=150)


if __name__ == "__main__":
    pay()
    minwage()
    print("charts written")
