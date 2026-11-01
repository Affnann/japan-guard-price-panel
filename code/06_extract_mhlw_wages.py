"""Extract what security guards (and, for comparison, building cleaners and, to 2019,
gatekeepers) are actually paid, by prefecture, from MHLW's Basic Survey on Wage Structure (賃金構造基本統計調査).

Inputs (data/raw/mhlw_wages/):
  wage_{year}_{a..d}_{prefecture range}.xls(x), survey years 2012-2025
  2012-2019: 都道府県別第2表 職種・性別きまって支給する現金給与額、所定内給与額及び年間賞与その他特別給与額
             (old MHLW occupation list; occupation and sex in one label, e.g. 警備員（男女計）)
  2020-2025: 都道府県別第3表 都道府県、職種（特掲）、性別きまって支給する現金給与額、
             所定内給与額及び年間賞与その他特別給与額（産業計）, which covers all workers
             including position holders (役職者), and the matching reference table sanko4
             (…（役職者を除く）, files *_excl-positions.xlsx), which leaves them out
             (occupations based on the Japan Standard Occupational Classification; sex in
             section headings 男女計 / 男 / 女)
  MHLW's occupation figures to 2019 cover only workers who are not position holders, so
  the 2012-2019 tables and the 2020-2025 sanko4 tables use the same coverage.
Output: data/clean/pay_by_prefecture.csv

All figures are for general workers (一般労働者, i.e. not short-time workers), all
industries, all firm sizes covered by the survey. Each prefecture block has eight
columns, in this order: age, years of service, scheduled hours, overtime hours,
contractual cash earnings, scheduled cash earnings, annual bonus and other special
earnings, number of workers (in tens).
"""
import csv
import os
import re
import unicodedata

import openpyxl
import xlrd

ROOT = os.path.join(os.path.dirname(__file__), "..")
RAW = os.path.join(ROOT, "data", "raw", "mhlw_wages")
OUT = os.path.join(ROOT, "data", "clean", "pay_by_prefecture.csv")
RATES = os.path.join(ROOT, "data", "clean", "guard_rates_by_prefecture.csv")

PREFS = ['北海道', '青森', '岩手', '宮城', '秋田', '山形', '福島', '茨城', '栃木', '群馬', '埼玉', '千葉',
         '東京', '神奈川', '新潟', '富山', '石川', '福井', '山梨', '長野', '岐阜', '静岡', '愛知', '三重',
         '滋賀', '京都', '大阪', '兵庫', '奈良', '和歌山', '鳥取', '島根', '岡山', '広島', '山口', '徳島',
         '香川', '愛媛', '高知', '福岡', '佐賀', '長崎', '熊本', '大分', '宮崎', '鹿児島', '沖縄']
FIELDS = ['age', 'tenure_years', 'scheduled_hours', 'overtime_hours', 'contractual_earnings_kyen',
          'scheduled_earnings_kyen', 'annual_bonus_kyen', 'workers_tens']
# occupation label in the source -> (occupation id, English name)
OCCUPATIONS = {
    '警備員': ('security_guards', 'Security guards'),
    # To 2019 gatekeepers (守衛, old number 602) were a separate occupation; from 2020 MHLW counts them
    # with security guards (old number 601) as occupation 1453 警備員.
    '守衛': ('gatekeepers', 'Gatekeepers (to 2019)'),
    'ビル清掃員': ('building_cleaners', 'Building cleaners'),
    'ビル・建物清掃員': ('building_cleaners', 'Building cleaners'),
}
SEX = {'男女計': 'total', '男': 'male', '女': 'female'}


def norm(s):
    return re.sub(r'\s+', '', unicodedata.normalize('NFKC', str(s)))


def read_sheets(path):
    if path.endswith('.xls'):
        book = xlrd.open_workbook(path)
        return [(sh.name, [sh.row_values(i) for i in range(sh.nrows)]) for sh in book.sheets()]
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    return [(name, [list(r) for r in wb[name].iter_rows(values_only=True)]) for name in wb.sheetnames]


def number(v):
    if v is None:
        return None
    s = norm(v)
    if s in ('', '-', '－', '‐', '…', 'X', 'x', '*', '***'):
        return None
    return float(s)


def split_label(text, section):
    """Return (occupation label, sex) for a row label, or None if it is not a wanted occupation."""
    last = norm(text.split('\n')[-1])
    m = re.match(r'^(.*?)[（(](男女計|男|女)[）)]$', last)
    if m:
        occ, sex = m.group(1), SEX[m.group(2)]
    else:
        occ, sex = last, section
    return (occ, sex) if occ in OCCUPATIONS else None


def parse(path):
    year = int(re.search(r'wage_(\d{4})_', os.path.basename(path)).group(1))
    positions = 'excluded' if (year <= 2019 or 'excl-positions' in path) else 'included'
    records = []
    for sheet, rows in read_sheets(path):
        header = next(i for i, r in enumerate(rows[:20]) if any(norm(v) == '区分' for v in r))
        blocks = {}
        for j, v in enumerate(rows[header]):
            c = norm(v)
            if c == '全国':
                blocks[j] = ('00', '全国')
            else:
                m = re.match(r'^(\d{2})(.+)$', c)
                if m and m.group(2) in PREFS:
                    blocks[j] = (m.group(1), m.group(2))
        assert len(blocks) in (12, 13), (path, sheet, len(blocks))
        section = None
        for i in range(header + 1, len(rows)):
            row = rows[i]
            labels = [v for v in row[:10] if isinstance(v, str) and v.strip()]
            for v in labels:
                first = v.replace('　', ' ').strip().split('\n')[0].strip()
                if first in SEX:
                    section = SEX[first]
            hit = None
            for v in labels:
                hit = split_label(v, section) or hit
            if not hit:
                continue
            occ, sex = hit
            occ_id, occ_en = OCCUPATIONS[occ]
            for col, (code, name) in sorted(blocks.items()):
                values = [number(row[col + k]) if col + k < len(row) else None for k in range(8)]
                records.append({
                    'survey_year': year,
                    'classification': 'MHLW occupation list to 2019' if year <= 2019 else 'JSOC-based list from 2020',
                    'position_holders': positions,
                    'pref_code': code, 'prefecture_ja': name, 'occupation': occ_id,
                    'occupation_en': occ_en, 'occupation_ja': occ, 'sex': sex,
                    **dict(zip(FIELDS, values)),
                    'source_file': os.path.basename(path), 'source_sheet': sheet, 'source_row': i + 1,
                })
    return records


def main():
    en = {}
    with open(RATES, encoding='utf-8') as f:
        for r in csv.DictReader(f):
            en[r['pref_code']] = r['prefecture_en']
    en['00'] = 'Japan'
    records = []
    for name in sorted(os.listdir(RAW)):
        if name.startswith('wage_') and name.endswith(('.xls', '.xlsx')):
            records += parse(os.path.join(RAW, name))
    for r in records:
        r['prefecture_en'] = en[r['pref_code']]
    cols = ['survey_year', 'classification', 'position_holders', 'pref_code', 'prefecture_ja', 'prefecture_en', 'occupation',
            'occupation_en', 'occupation_ja', 'sex'] + FIELDS + ['source_file', 'source_sheet', 'source_row']
    records.sort(key=lambda r: (r['occupation'], r['position_holders'], r['survey_year'], r['pref_code'],
                                ['total', 'male', 'female'].index(r['sex'])))
    with open(OUT, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in records:
            w.writerow({k: ('' if r[k] is None else (int(r[k]) if k == 'workers_tens' else r[k])) for k in cols})
    print(f'{len(records)} rows -> {os.path.relpath(OUT, ROOT)}')


if __name__ == '__main__':
    main()
