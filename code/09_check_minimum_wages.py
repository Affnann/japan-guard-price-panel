"""Check data/clean/minimum_wage_by_prefecture.csv and write data/clean/checks_report_minwage.md.

1. Every fiscal year FY2002-FY2026 has all 47 prefectures and the national weighted average.
2. A prefecture's minimum wage never falls from one year to the next.
3. Each revision took effect in its fiscal year (April of that year to March of the next),
   or, where the amount did not change, the earlier date is kept.
4. The national weighted average lies between the lowest and highest prefecture.
5. The national weighted average matches figures MHLW states in its press releases
   (FY2025: 1,121 yen; FY2024: 1,055 yen).
6. Second reading of MHLW's file with a different library (python-calamine): every amount equals the
   cell as the file displays it, in whole yen rounded half up (the national averages are stored with
   decimals, e.g. FY2017 847.72, displayed as 848).
"""
import csv
import datetime
import os
import re
import unicodedata
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP

from python_calamine import CalamineWorkbook

ROOT = os.path.join(os.path.dirname(__file__), "..")
CLEAN = os.path.join(ROOT, "data", "clean", "minimum_wage_by_prefecture.csv")
REPORT = os.path.join(ROOT, "data", "clean", "checks_report_minwage.md")
SRC = os.path.join(ROOT, "data", "raw", "mhlw_minwage", "minwage_FY2002-FY2026.xlsx")
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
    # 6. second reading of the raw file
    grid = CalamineWorkbook.from_path(SRC).get_sheet_by_index(0).to_python()
    norm = lambda v: re.sub(r'\s+', '', unicodedata.normalize('NFKC', str(v)))
    head = [norm(v) for v in grid[0]]
    fys = []
    for v in head[1:]:
        m = re.match(r'^(平成|令和)(\d+|元)年度$', v)
        if m:
            fys.append((1988 if m.group(1) == '平成' else 2018) + (1 if m.group(2) == '元' else int(m.group(2))))
    names = {}
    for r in rows:
        if r['pref_code'] == '00':
            names['全国加重平均額'] = '00'
        else:
            ja = r['prefecture_ja']
            names[ja if ja == '北海道' else re.sub(r'(都|府|県)$', '', ja)] = r['pref_code']
    n_cells, diff = 0, []
    for row in grid[2:]:
        if not row or norm(row[0]) not in names:
            continue
        code = names[norm(row[0])]
        for k, fy in enumerate(fys):
            v = row[1 + 2 * k]
            shown = int(Decimal(str(v)).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
            got = int(by[fy][code]['hourly_yen'])
            n_cells += 1
            if shown != got:
                diff.append(f'FY{fy} {code}: file {got}, MHLW {v}')
    lines += ['', '## 6. Second reading of MHLW\'s file (python-calamine)', '',
              f'- {n_cells:,} amounts read again: ' + (f'all {n_cells:,} agree.' if not diff else 'DIFFER: ' + '; '.join(diff))]
    ok &= not diff and n_cells == 48 * len(years)
    lines += ['', '## Result', '', '- All checks passed.' if ok else '- SOME CHECKS FAILED: see above.', '']
    open(REPORT, 'w', encoding='utf-8').write('\n'.join(lines))
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
