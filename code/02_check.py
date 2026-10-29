"""Checks on data/clean/guard_rates_by_prefecture.csv.

1. Second reading: re-read every release with a different PDF engine
   (pdfplumber/pdfminer instead of PyMuPDF) and flag any disagreement.
2. Completeness: 47 prefectures x 2 grades in every table year.
3. Year-to-year changes: flag falls and rises above 15% for a look in the PDF.
4. National average: compare the simple average of the 47 prefectures with the
   nationwide figure MLIT prints in the release text, where it gives one.
5. Spot check: 10 random rows with file and page, for checking by eye.

Writes data/clean/checks_report.md.
"""
import csv
import os
import random
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(__file__))
from mlit_tables import read_release, words_pymupdf  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
CLEAN = os.path.join(ROOT, "data", "clean", "guard_rates_by_prefecture.csv")
REPORT = os.path.join(ROOT, "data", "clean", "checks_report.md")


def main():
    rows = list(csv.DictReader(open(CLEAN, encoding="utf-8")))
    lines = ["# Checks report", "", f"Rows checked: {len(rows)}", ""]
    problems = 0

    # 1. second reading
    lines += ["## 1. Second reading (pdfplumber vs PyMuPDF)", ""]
    by_file = defaultdict(list)
    for r in rows:
        by_file[r["source_file"]].append(r)
    disagree = []
    for f, rs in sorted(by_file.items()):
        page, second = read_release(os.path.join(ROOT, "data/raw/mlit", f), "pdfplumber")
        second = {x["pref"]: x for x in second}
        for r in rs:
            g = r["grade"].lower()
            s = second[r["prefecture_ja"]]
            mark_second = "yes" if s[g + "_mark"] else "no"
            if s[g] != int(r["daily_rate_yen"]) or mark_second != r["special_rate"] or page != int(r["source_page"]):
                disagree.append(f"- {f} {r['prefecture_en']} {r['grade']}: first {r['daily_rate_yen']}, second {s[g]}")
    problems += len(disagree)
    lines += disagree or ["All values agree."]
    lines.append("")

    # 2. completeness
    lines += ["## 2. Completeness", ""]
    years = sorted({r["table_year"] for r in rows})
    bad = [y for y in years if sum(1 for r in rows if r["table_year"] == y) != 94]
    problems += len(bad)
    lines += [f"Table years: {years[0]}-{years[-1]} ({len(years)} years). "
              + ("Every year has 47 prefectures x 2 grades." if not bad else f"Incomplete years: {bad}"), ""]

    # 3. year-to-year changes
    lines += ["## 3. Year-to-year changes to look at in the PDF", "",
              "Falls, and rises above 15%, compared with the previous table year.", ""]
    series = defaultdict(dict)
    for r in rows:
        series[(r["prefecture_en"], r["grade"])][int(r["table_year"])] = (int(r["daily_rate_yen"]), r["special_rate"])
    flags = []
    for (pref, grade), s in sorted(series.items()):
        ys = sorted(s)
        for a, b in zip(ys, ys[1:]):
            ch = s[b][0] / s[a][0] - 1
            if ch < 0 or ch > 0.15:
                flags.append(f"- {pref} {grade}: {a} {s[a][0]:,} -> {b} {s[b][0]:,} ({ch:+.1%})"
                             + (" [special rate involved]" if "yes" in (s[a][1], s[b][1]) else ""))
    lines += flags or ["None."]
    lines.append("")

    # 4. national averages printed by MLIT
    lines += ["## 4. Simple average of 47 prefectures vs MLIT's nationwide figure", "",
              "MLIT's nationwide figure is a weighted average (by number of workers surveyed), "
              "so it is not expected to match the simple average exactly. This is a sanity check only.", "",
              "| Table year | Grade | Simple average of 47 | MLIT nationwide figure | Source file |",
              "|---|---|---|---|---|"]
    pat = re.compile(r"交通誘導警備員\s*([ＡAＢB])\s*([\d,]{5,7})\s*円")
    for f, rs in sorted(by_file.items()):
        text = "".join(t for _, t, _ in words_pymupdf(os.path.join(ROOT, "data/raw/mlit", f)))
        found = {}
        for m in pat.finditer(text.replace("\n", " ")):
            found.setdefault("A" if m.group(1) in "ＡA" else "B", int(m.group(2).replace(",", "")))
        for grade in ("A", "B"):
            vals = [int(r["daily_rate_yen"]) for r in rs if r["grade"] == grade]
            avg = sum(vals) / len(vals)
            nat = f"{found[grade]:,}" if grade in found else "not printed"
            lines.append(f"| {rs[0]['table_year']} | {grade} | {avg:,.0f} | {nat} | {f} |")
    lines.append("")

    # 5. spot check
    lines += ["## 5. Spot check by eye", "",
              "Open each file at the page shown and find the prefecture row; the last two columns are guard A and guard B.", "",
              "| Table year | Prefecture | Grade | Value in dataset | File | PDF page | Matches? |",
              "|---|---|---|---|---|---|---|"]
    random.seed(10)
    for r in random.sample(rows, 10):
        lines.append(f"| {r['table_year']} | {r['prefecture_en']} ({r['prefecture_ja']}) | {r['grade']} | "
                     f"{int(r['daily_rate_yen']):,} | {r['source_file']} | {r['source_page']} | |")
    lines.append("")

    open(REPORT, "w", encoding="utf-8").write("\n".join(lines))
    print(f"disagreements/incomplete: {problems}; year-to-year flags: {len(flags)}")
    print(f"report written to {os.path.relpath(REPORT, ROOT)}")


if __name__ == "__main__":
    main()
