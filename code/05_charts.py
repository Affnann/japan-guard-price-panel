"""Two charts for the README (kept separate: different units, so no shared axis).

figures/guard_rates.png       average daily rate across the 47 prefectures, guard A and B
figures/security_jobs.png     job openings per applicant: security occupations vs all occupations
"""
import csv
import os
from collections import defaultdict

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

plt.rcParams["font.family"] = ["Noto Sans CJK JP", "DejaVu Sans"]

ROOT = os.path.join(os.path.dirname(__file__), "..")
BLUE, ORANGE = "#2a78d6", "#eb6834"
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


def rates():
    rows = list(csv.DictReader(open(os.path.join(ROOT, "data/clean/guard_rates_by_prefecture.csv"), encoding="utf-8")))
    s = defaultdict(lambda: defaultdict(list))
    for r in rows:
        s[r["grade"]][int(r["table_year"])].append(int(r["daily_rate_yen"]))
    fig, ax = plt.subplots(figsize=(8, 4.5), facecolor=SURFACE)
    for g, c in (("A", BLUE), ("B", ORANGE)):
        ys = sorted(s[g])
        vals = [sum(s[g][y]) / len(s[g][y]) for y in ys]
        ax.plot(ys, vals, color=c, linewidth=2, marker="o", markersize=5)
        ax.annotate(f"Guard {g}: ¥{vals[-1]:,.0f}", (ys[-1], vals[-1]), xytext=(8, 0),
                    textcoords="offset points", va="center", color=INK, fontsize=9)
        ax.annotate(f"¥{vals[0]:,.0f}", (ys[0], vals[0]), xytext=(-8, 6 if g == "A" else -8),
                    textcoords="offset points", ha="right", va="center", color=MUTED, fontsize=8)
    ax.set_xlim(2010.2, 2028.6)
    ax.set_xticks(range(2012, 2027, 2))
    ax.set_ylim(0, 21000)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"¥{v:,.0f}"))
    style(ax, "Traffic guard daily rate on Japanese public works, average of 47 prefectures",
          "Yen per 8-hour day (wage only)")
    fig.text(0.01, 0.01, "Source: MLIT, 公共工事設計労務単価, FY2012-FY2026 (simple average of prefectures; "
             "includes special rates).", color=MUTED, fontsize=7.5)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(os.path.join(ROOT, "figures/guard_rates.png"), dpi=150)


def jobs():
    rows = list(csv.DictReader(open(os.path.join(ROOT, "data/clean/security_jobs_monthly.csv"), encoding="utf-8")))
    s = defaultdict(dict)
    for r in rows:
        if r["measure"] != "active_openings_ratio":
            continue
        # one continuous series: old classification to 2022-03, new from 2022-04 (identical in the overlap)
        new = r["source_file"].startswith("occ_2023")
        if new or r["month"] < "2022-04":
            s[r["occupation"]][r["month"]] = float(r["value"])
    fig, ax = plt.subplots(figsize=(8, 4.5), facecolor=SURFACE)
    for occ, c, label in (("security", BLUE, "Security occupations"), ("all", ORANGE, "All occupations")):
        ms = sorted(s[occ])
        x = [int(m[:4]) + (int(m[5:]) - 1) / 12 for m in ms]
        v = [s[occ][m] for m in ms]
        ax.plot(x, v, color=c, linewidth=2)
        ax.annotate(f"{label}: {v[-1]:.2f}", (x[-1], v[-1]), xytext=(8, 0), textcoords="offset points",
                    va="center", color=INK, fontsize=9)
    ax.set_xlim(2012, 2029.6)
    ax.set_xticks(range(2012, 2027, 2))
    ax.set_ylim(0, 9)
    style(ax, "Job openings per applicant in Japan, monthly", "Openings per applicant")
    fig.text(0.01, 0.01, "Source: MHLW, 一般職業紹介状況 (e-Stat table 21), March 2012 - August 2026; "
             "regular jobs incl. part-time, not seasonally adjusted.", color=MUTED, fontsize=7.5)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(os.path.join(ROOT, "figures/security_jobs.png"), dpi=150)


if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "figures"), exist_ok=True)
    rates()
    jobs()
    print("charts written to figures/")
