"""Extract each prefecture's minimum wage (地域別最低賃金, yen per hour) and the date each
revision took effect, FY2002-FY2026, from MHLW's history file.

Input:  data/raw/mhlw_minwage/minwage_FY2002-FY2026.xlsx
        (「平成14年度から令和８年度までの地域別最低賃金改定状況」, MHLW)
Output: data/clean/minimum_wage_by_prefecture.csv
"""
import csv
import datetime
import os
import re
import unicodedata

import openpyxl

ROOT = os.path.join(os.path.dirname(__file__), "..")
SRC = os.path.join(ROOT, "data", "raw", "mhlw_minwage", "minwage_FY2002-FY2026.xlsx")
OUT = os.path.join(ROOT, "data", "clean", "minimum_wage_by_prefecture.csv")
RATES = os.path.join(ROOT, "data", "clean", "guard_rates_by_prefecture.csv")


def norm(s):
    return re.sub(r'\s+', '', unicodedata.normalize('NFKC', str(s)))


def fiscal_year(label):
    s = norm(label).replace('元', '1')
    m = re.match(r'^(平成|令和)(\d+)年度$', s)
    assert m, label
    return (1988 if m.group(1) == '平成' else 2018) + int(m.group(2))


def excel_date(v):
    if isinstance(v, datetime.datetime):
        return v.date()
    return datetime.date(1899, 12, 30) + datetime.timedelta(days=int(v))


def main():
    codes = {}
    with open(RATES, encoding='utf-8') as f:
        for r in csv.DictReader(f):
            codes[r['prefecture_ja']] = (r['pref_code'], r['prefecture_en'])
    by_name = {}
    for ja, (code, en) in codes.items():
        short = ja if ja == '北海道' else re.sub(r'(都|府|県)$', '', ja)
        by_name[short] = (code, en, ja)
    wb = openpyxl.load_workbook(SRC, data_only=True)
    ws = wb[wb.sheetnames[0]]
    rows = list(ws.iter_rows(values_only=True))
    years = [fiscal_year(v) for v in rows[0][1:] if v not in (None, '')]
    assert norm(rows[1][1]) == '改定額(円)' and norm(rows[1][2]) == '発効年月日'
    out = []
    for r in rows[2:]:
        if r[0] is None:
            continue
        name = norm(r[0])
        if name == '全国加重平均額':
            for k, fy in enumerate(years):
                out.append({'fiscal_year': fy, 'pref_code': '00', 'prefecture_ja': '全国（加重平均）',
                            'prefecture_en': 'Japan (weighted average)', 'hourly_yen': int(r[1 + 2 * k]),
                            'effective_date': ''})
            continue
        code, en, ja = by_name[name]
        for k, fy in enumerate(years):
            amount, eff = r[1 + 2 * k], r[2 + 2 * k]
            out.append({'fiscal_year': fy, 'pref_code': code, 'prefecture_ja': ja, 'prefecture_en': en,
                        'hourly_yen': int(amount), 'effective_date': excel_date(eff).isoformat()})
    out.sort(key=lambda x: (x['fiscal_year'], x['pref_code']))
    with open(OUT, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    print(f'{len(out)} rows, FY{years[0]}-FY{years[-1]} -> {os.path.relpath(OUT, ROOT)}')


if __name__ == '__main__':
    main()
