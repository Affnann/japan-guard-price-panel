"""Extract monthly job-openings figures for security occupations (and for all
occupations, as a benchmark) from MHLW's job placement statistics
(一般職業紹介状況, long time-series table 21, via e-Stat).

Inputs (data/raw/mhlw/):
  occ_2012-03_to_2023-03.xlsx  4th-revision MHLW occupation classification (2011)
  occ_2023-04_onward.xlsx      Japan Standard Occupational Classification (2009 revision),
                               recalculated back to April 2022
Output: data/clean/security_jobs_monthly.csv

Figures are for regular employment including part-time (パートタイムを含む常用),
not seasonally adjusted, national totals.
"""
import csv
import os
import re

import openpyxl

ROOT = os.path.join(os.path.dirname(__file__), "..")
RAW = os.path.join(ROOT, "data", "raw", "mhlw")
OUT = os.path.join(ROOT, "data", "clean", "security_jobs_monthly.csv")

FILES = [
    ("occ_2012-03_to_2023-03.xlsx", "MHLW occupation classification, 4th revision (2011)"),
    ("occ_2023-04_onward.xlsx", "Japan Standard Occupational Classification (2009 revision)"),
]
# sheet index -> measure (the sheet order is the same in both files; names are checked below)
SHEETS = {
    0: ("new_openings", "新規求人"),
    1: ("active_openings", "有効求人"),
    2: ("new_applicants", "新規求職"),
    3: ("active_applicants", "有効求職"),
    6: ("active_openings_ratio", "有効求人倍率"),
}
OCCUPATIONS = {
    "職業計": ("all", "All occupations"),
    "保安の職業": ("security", "Security occupations"),
    "保安職業従事者": ("security", "Security occupations"),
}


def main():
    out = []
    for fname, classification in FILES:
        wb = openpyxl.load_workbook(os.path.join(RAW, fname), read_only=True, data_only=True)
        for idx, (measure, ja) in SHEETS.items():
            sheet = wb.sheetnames[idx]
            assert ja in sheet and "パート含む" in sheet, (fname, sheet)
            rows = list(wb[sheet].iter_rows(values_only=True))
            years, months = rows[1], rows[3]
            for r in rows:
                label = str(r[0]).strip() if r[0] else ""
                if label not in OCCUPATIONS:
                    continue
                code, en = OCCUPATIONS[label]
                for c in range(1, len(r)):
                    if not months[c] or r[c] is None:
                        continue  # annual / fiscal-year columns have no month
                    y = int(re.match(r"(\d{4})", str(years[c])).group(1))
                    m = int(re.match(r"(\d{1,2})", str(months[c])).group(1))
                    out.append({
                        "month": f"{y}-{m:02d}",
                        "classification": classification,
                        "occupation": code,
                        "occupation_ja": label,
                        "occupation_en": en,
                        "measure": measure,
                        "value": r[c],
                        "source_file": fname,
                        "source_sheet": sheet.strip(),
                    })
    out.sort(key=lambda d: (d["classification"], d["occupation"], d["measure"], d["month"]))
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    print(f"wrote {len(out)} rows to {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
