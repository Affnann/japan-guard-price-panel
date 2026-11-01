"""Check data/clean/pay_by_prefecture.csv and write data/clean/checks_report_pay.md.

1. Coverage: every survey year 2012-2025 has Japan and all 47 prefectures, for both
   occupations, both sexes combined and men (and women where MHLW publishes them).
2. Second reading: every value is read again from the source file with a different Excel
   reader (python-calamine) at the recorded row and column, and compared.
3. Men and women add up: where all three rows are published, total workers equal men plus
   women (to rounding), and total earnings lie between men's and women's.
4. Japan against the prefectures: Japan's scheduled earnings against the worker-weighted
   mean of the 47 prefectures, and Japan's workers against their sum.
5. Large year-on-year changes (over 15 percent) in scheduled earnings, listed.
6. Missing values, listed.
"""
import csv
import os
import re
import unicodedata
from collections import defaultdict

from python_calamine import CalamineWorkbook

ROOT = os.path.join(os.path.dirname(__file__), "..")
RAW = os.path.join(ROOT, "data", "raw", "mhlw_wages")
CLEAN = os.path.join(ROOT, "data", "clean", "pay_by_prefecture.csv")
REPORT = os.path.join(ROOT, "data", "clean", "checks_report_pay.md")
FIELDS = ['age', 'tenure_years', 'scheduled_hours', 'overtime_hours', 'contractual_earnings_kyen',
          'scheduled_earnings_kyen', 'annual_bonus_kyen', 'workers_tens']
OCC = {'security_guards': 'Security guards', 'building_cleaners': 'Building cleaners', 'gatekeepers': 'Gatekeepers',
       'other_protective': 'Other protective service workers'}
SPAN = {'security_guards': (2012, 2025), 'building_cleaners': (2012, 2025), 'gatekeepers': (2012, 2019),
        'other_protective': (2020, 2025)}


def norm(s):
    return re.sub(r'\s+', '', unicodedata.normalize('NFKC', str(s)))


def fnum(v):
    if v in (None, ''):
        return None
    s = norm(v)
    if s in ('-', '－', '‐', '…', 'X', 'x', '*', '***', ''):
        return None
    return float(s)


def main():
    rows = list(csv.DictReader(open(CLEAN, encoding='utf-8')))
    lines = ['# Checks: security guards\' and building cleaners\' pay by prefecture', '',
             'Output of `code/07_check_mhlw_wages.py`.', '']
    ok_all = True

    # 1. coverage
    have = defaultdict(set)
    for r in rows:
        have[(r['occupation'], r['position_holders'], int(r['survey_year']), r['sex'])].add(r['pref_code'])
    lines += ['## 1. Coverage', '']
    problems = []
    for occ in OCC:
        lo, hi = SPAN[occ]
        for cov, years in (('excluded', range(lo, hi + 1)), ('included', range(max(lo, 2020), hi + 1))):
            for y in years:
                sexes = ['total', 'male'] + (['female'] if (occ == 'building_cleaners' or y >= 2020) else [])
                for s in sexes:
                    n = len(have[(occ, cov, y, s)])
                    if n != 48:
                        problems.append(f'{occ} {cov} {y} {s}: {n} regions')
    women_guards_old = [y for y in range(2012, 2020) if have[('security_guards', 'excluded', y, 'female')]]
    lines.append(f'- Every survey year 2012-2025 has Japan and all 47 prefectures for security guards and building '
                 f'cleaners, 2012-2019 for gatekeepers (merged into security guards from 2020) and 2020-2025 for other '
                 f'protective service workers (the occupation that includes traffic guards from 2020), '
                 f'excluding position holders (and, for 2020-2025, also including them), '
                 f'both sexes combined and men; women are published for building cleaners in every year '
                 f'and for security guards from 2020 (MHLW\'s list to 2019 has no separate row for women '
                 f'guards){"." if not problems and not women_guards_old else ": PROBLEMS " + "; ".join(problems)}')
    ok_all &= not problems and not women_guards_old
    lines.append(f'- Rows: {len(rows)}.')
    lines.append('')

    # 2. second reading with python-calamine
    cache = {}
    mismatches = 0
    checked = 0
    for r in rows:
        fn = r['source_file']
        if fn not in cache:
            wb = CalamineWorkbook.from_path(os.path.join(RAW, fn))
            cache[fn] = {name: wb.get_sheet_by_name(name).to_python() for name in wb.sheet_names}
        sheet = cache[fn][r['source_sheet']]
        row = sheet[int(r['source_row']) - 1]
        # locate the prefecture block: header row containing 区分
        hdr = next(i for i, x in enumerate(sheet[:20]) if any(norm(v) == '区分' for v in x))
        col = None
        for j, v in enumerate(sheet[hdr]):
            c = norm(v)
            if (r['pref_code'] == '00' and c == '全国') or (r['pref_code'] != '00' and c.startswith(r['pref_code'])):
                col = j
                break
        vals = [fnum(row[col + k]) if col + k < len(row) else None for k in range(8)]
        for k, f in enumerate(FIELDS):
            a = fnum(r[f])
            b = vals[k]
            checked += 1
            if (a is None) != (b is None) or (a is not None and abs(a - b) > 1e-9):
                mismatches += 1
    lines += ['## 2. Second reading', '',
              f'- {checked:,} values read again with python-calamine (the extraction uses xlrd and openpyxl): '
              f'{checked - mismatches:,} agree, {mismatches} differ.', '']
    ok_all &= mismatches == 0

    # 3. men and women add up
    idx = {(r['occupation'], r['position_holders'], r['survey_year'], r['pref_code'], r['sex']): r for r in rows}
    n3 = 0
    bad_w, bad_between, devs = [], [], []
    for (occ, cov, y, p, s), r in idx.items():
        if s != 'total':
            continue
        m, f = idx.get((occ, cov, y, p, 'male')), idx.get((occ, cov, y, p, 'female'))
        if not m or not f or '' in (r['workers_tens'], m['workers_tens'], f['workers_tens'],
                                    r['scheduled_earnings_kyen'], m['scheduled_earnings_kyen'],
                                    f['scheduled_earnings_kyen']):
            continue
        n3 += 1
        wt, wm, wf = float(r['workers_tens']), float(m['workers_tens']), float(f['workers_tens'])
        if abs(wt - (wm + wf)) > 2:
            bad_w.append(f'{occ} {cov} {y} {p}: {wt:g} vs {wm + wf:g}')
        et, em, ef = (float(r['scheduled_earnings_kyen']), float(m['scheduled_earnings_kyen']),
                      float(f['scheduled_earnings_kyen']))
        if not (min(em, ef) - 0.1 <= et <= max(em, ef) + 0.1):
            bad_between.append(f'{occ} {cov} {y} {p}: total {et} outside men {em} and women {ef}')
        devs.append(abs(et - (em * wm + ef * wf) / (wm + wf)))
    devs.sort()
    lines += ['## 3. Men and women add up', '',
              f'- Region-years with all three rows published: {n3}.',
              f'- Total workers equal men plus women within 20 people (2 tens): {n3 - len(bad_w)} of {n3}.'
              + ('' if not bad_w else ' Exceptions: ' + '; '.join(bad_w[:20])),
              f'- Total scheduled earnings lie between men\'s and women\'s (within 0.1 thousand yen of rounding): '
              f'{n3 - len(bad_between)} of {n3}.' + ('' if not bad_between else ' Exceptions: ' + '; '.join(bad_between[:20])),
              f'- For information: the total differs from the mean of men and women weighted by the rounded '
              f'worker counts by a median of {devs[len(devs) // 2]:.2f} and at most {devs[-1]:.2f} thousand yen '
              f'(worker counts are published in tens, so the weights are rounded).',
              '']
    ok_all &= not bad_w and not bad_between

    # 4. Japan against the prefectures
    lines += ['## 4. Japan against the 47 prefectures (both sexes combined)', '',
              '| Occupation | Position holders | Year | Japan, scheduled earnings (thousand yen) | Worker-weighted mean of prefectures | Japan, workers (tens) | Sum of prefectures |',
              '|---|---|---|---|---|---|---|']
    gaps = []
    for occ in OCC:
        lo, hi = SPAN[occ]
        for cov, years in (('excluded', range(lo, hi + 1)), ('included', range(max(lo, 2020), hi + 1))):
            for y in years:
                nat = idx[(occ, cov, str(y), '00', 'total')]
                prefs = [idx[(occ, cov, str(y), '%02d' % p, 'total')] for p in range(1, 48)]
                prefs = [x for x in prefs if x['workers_tens'] != '' and x['scheduled_earnings_kyen'] != '']
                w = sum(float(x['workers_tens']) for x in prefs)
                mean = sum(float(x['scheduled_earnings_kyen']) * float(x['workers_tens']) for x in prefs) / w
                if len(prefs) == 47:
                    gaps.append(abs(mean - float(nat['scheduled_earnings_kyen'])))
                note = '' if len(prefs) == 47 else f' ({47 - len(prefs)} prefectures without figures)'
                lines.append(f'| {OCC[occ]} | {cov} | {y} | {float(nat["scheduled_earnings_kyen"]):.1f} | {mean:.1f} | '
                             f'{float(nat["workers_tens"]):,.0f} | {w:,.0f}{note} |')
    lines += ['', f'- Largest gap between Japan and the worker-weighted mean of the prefectures, where all 47 have figures: '
              f'{max(gaps):.2f} thousand yen.']
    lines.append('')

    # 5. large changes
    lines += ['## 5. Year-on-year changes in scheduled earnings over 15 percent (both sexes combined, excluding position holders)', '',
              'Listed for inspection; prefecture figures come from a sample survey, so small prefectures move more.', '']
    big = []
    for occ in OCC:
        for p in ['00'] + ['%02d' % i for i in range(1, 48)]:
            for y in range(SPAN[occ][0] + 1, SPAN[occ][1] + 1):
                a, b = idx[(occ, 'excluded', str(y - 1), p, 'total')], idx[(occ, 'excluded', str(y), p, 'total')]
                if a['scheduled_earnings_kyen'] and b['scheduled_earnings_kyen']:
                    ch = float(b['scheduled_earnings_kyen']) / float(a['scheduled_earnings_kyen']) - 1
                    if abs(ch) > 0.15:
                        big.append(f'{OCC[occ]}, {b["prefecture_en"]}, {y - 1}-{y}: {ch * 100:+.1f}% '
                                   f'(workers {a["workers_tens"]} and {b["workers_tens"]} tens)')
    lines += [f'- {x}' for x in big] or ['- None.']
    lines.append('')

    # 6. missing
    miss = [f'{r["occupation_en"]}, {r["prefecture_en"]}, {r["survey_year"]}, {r["sex"]}, position holders {r["position_holders"]}'
            for r in rows if r['scheduled_earnings_kyen'] == '']
    lines += ['## 6. Missing values', '',
              f'- {len(miss)} rows have no figures in the source (shown as "-"): ' + ('; '.join(miss) if miss else 'none') + '.', '']
    lines += ['## Result', '', '- All checks passed.' if ok_all else '- SOME CHECKS FAILED: see above.', '']
    open(REPORT, 'w', encoding='utf-8').write('\n'.join(lines))
    print('\n'.join(lines[:30]))
    print('...')
    print('ALL OK' if ok_all else 'FAILED')


if __name__ == '__main__':
    main()
