"""Extract the traffic-guard daily rates (A and B) for every prefecture and
table year from MLIT's public works labor rate releases.

Input:  data/raw/mlit/*_FY*_release.pdf
Output: data/clean/guard_rates_by_prefecture.csv  (one row per year x prefecture x grade)
"""
import csv
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from mlit_tables import PREFECTURES, read_release  # noqa: E402

PREF_EN = [
    "Hokkaido", "Aomori", "Iwate", "Miyagi", "Akita", "Yamagata", "Fukushima", "Ibaraki",
    "Tochigi", "Gunma", "Saitama", "Chiba", "Tokyo", "Kanagawa", "Niigata", "Toyama",
    "Ishikawa", "Fukui", "Yamanashi", "Nagano", "Gifu", "Shizuoka", "Aichi", "Mie",
    "Shiga", "Kyoto", "Osaka", "Hyogo", "Nara", "Wakayama", "Tottori", "Shimane",
    "Okayama", "Hiroshima", "Yamaguchi", "Tokushima", "Kagawa", "Ehime", "Kochi", "Fukuoka",
    "Saga", "Nagasaki", "Kumamoto", "Oita", "Miyazaki", "Kagoshima", "Okinawa",
]

NOTES = {
    "()": "special rate for Iwate, Miyagi and Fukushima set to reflect failed bids (shown in round brackets in the source)",
    "<>": "special COVID-19 measure (shown in angle brackets in the source)",
    "": "",
}

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "data", "clean", "guard_rates_by_prefecture.csv")


def main():
    files = sorted(f for f in glob.glob(os.path.join(ROOT, "data/raw/mlit/20*_FY*_release.pdf"))
                   if "revision" not in f)
    out = []
    for f in files:
        name = os.path.basename(f)
        effective_from = name[:7]
        table_year = int(name.split("_FY")[1][:4])
        page, rows = read_release(f, "pymupdf")
        assert len(rows) == 47
        for code, (r, en) in enumerate(zip(rows, PREF_EN), start=1):
            for grade in ("A", "B"):
                v = r[grade.lower()]
                if v is None:
                    raise ValueError(f"{name}: missing {grade} for {r['pref']}")
                mark = r[grade.lower() + "_mark"]
                out.append({
                    "table_year": table_year,
                    "effective_from": effective_from,
                    "pref_code": f"{code:02d}",
                    "prefecture_ja": r["pref"],
                    "prefecture_en": en,
                    "grade": grade,
                    "daily_rate_yen": v,
                    "special_rate": "yes" if mark else "no",
                    "note": NOTES[mark],
                    "source_file": name,
                    "source_page": page,
                })
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    print(f"wrote {len(out)} rows from {len(files)} releases to {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
