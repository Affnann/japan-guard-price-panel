"""Check data/clean/minimum_wage_by_prefecture.csv and write data/clean/checks_report_minwage.md.

1. Every fiscal year FY2002-FY2026 has all 47 prefectures and the national weighted average.
2. A prefecture's minimum wage never falls from one year to the next.
3. Each revision took effect in its fiscal year (April of that year to March of the next),
   or, where the amount did not change, the earlier date is kept.
4. The national weighted average lies between the lowest and highest prefecture.
5. The national weighted average matches figures MHLW states in its press releases
   (FY2025: 1,121 yen; FY2024: 1,055 yen).
"""
import csv
import datetime
import os
from collections import defaultdict

ROOT = os.path.join(os.path.dirname(__file__), "..")
CLEAN = os.path.join(ROOT, "data", "clean", "minimum_wage_by_prefecture.csv")
REPORT = os.path.join(ROOT, "data", "clean", "checks_report_minwage.md")
# National weighted averages stated by MHLW in its press release of 5 September 2025
# (https://www.mhlw.go.jp/stf/newpage_63030.html): FY2025 1,121 yen, FY2024 1,055 yen.
STATED = {2025: 1121, 2024: 1055}


def main():
    rows = list(csv.DictReader(open(CLEAN, encoding='utf-8')))
    by = defaultdict(dict)
    for r in rows:
        by[int(r['fiscal_year'])][r['pref_code']] = r
    years = sorted(by)
    ok = True
    lines = ['# Checks: prefecture minimum wages', '', 'Output of `code/09_check_minimum_wages.py`.', '']

    miss = [y for y in years if len(by[y]) != 48]
    lines += ['## 1. Coverage', '', f'- FY{years[0]}-FY{years[-1]}: every year has 47 prefectures and the national '
              f'weighted average' + ('.' if not miss else f': MISSING in {miss}'), '']
    ok &= not miss

    falls = []
    for y in years[1:]:
        for p in ['%02d' % i for i in range(1, 48)]:
            if int(by[y][p]['hourly_yen']) < int(by[y - 1][p]['hourly_yen']):
                falls.append(f'{by[y][p]["prefecture_en"]} FY{y}')
    lines += ['## 2. Never falls', '', '- ' + ('No prefecture\'s minimum wage falls from one year to the next.'
                                           if not falls else 'FALLS: ' + '; '.join(falls)), '']
    ok &= not falls

    bad, kept = [], []
    for y in years:
        for p in ['%02d' % i for i in range(1, 48)]:
            r = by[y][p]
            d = datetime.date.fromisoformat(r['effective_date'])
            if datetime.date(y, 4, 1) <= d <= datetime.date(y + 1, 3, 31):
                continue
            prev = by.get(y - 1, {}).get(p)
            if prev and prev['hourly_yen'] == r['hourly_yen'] and prev['effective_date'] == r['effective_date']:
                kept.append(f'{r["prefecture_en"]} FY{y}')
            else:
                bad.append(f'{r["prefecture_en"]} FY{y} ({r["effective_date"]})')
    lines += ['## 3. Effective dates', '',
              f'- Revisions dated within their fiscal year: {47 * len(years) - len(bad) - len(kept)} of {47 * len(years)}.',
              f'- Unchanged amounts that keep the previous year\'s date: {len(kept)}' + (f' ({"; ".join(kept)})' if kept else '') + '.',
              f'- Other dates: ' + ('none.' if not bad else '; '.join(bad))]
    lines.append('')
    ok &= not bad

    out_range = []
    for y in years:
        vals = [int(by[y]['%02d' % i]['hourly_yen']) for i in range(1, 48)]
        nat = int(by[y]['00']['hourly_yen'])
        if not (min(vals) <= nat <= max(vals)):
            out_range.append(f'FY{y}')
    lines += ['## 4. National average within the range', '',
              '- ' + ('The national weighted average lies between the lowest and highest prefecture in every year.'
                      if not out_range else 'OUTSIDE in ' + ', '.join(out_range)), '']
    ok &= not out_range

    lines += ['## 5. Against MHLW\'s stated national averages', '']
    for y, v in STATED.items():
        got = int(by[y]['00']['hourly_yen'])
        lines.append(f'- FY{y}: file {got:,} yen, press release {v:,} yen: {"match" if got == v else "MISMATCH"}.')
        ok &= got == v
    lines += ['', '## Result', '', '- All checks passed.' if ok else '- SOME CHECKS FAILED: see above.', '']
    open(REPORT, 'w', encoding='utf-8').write('\n'.join(lines))
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
