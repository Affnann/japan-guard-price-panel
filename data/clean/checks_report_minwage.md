# Checks: prefecture minimum wages

Output of `code/09_check_minimum_wages.py`.

## 1. Coverage

- FY2002-FY2026: every year has 47 prefectures and the national weighted average.

## 2. Never falls

- No prefecture's minimum wage falls from one year to the next.

## 3. Effective dates

- Revisions dated within their fiscal year: 1126 of 1175.
- Unchanged amounts that keep the previous year's date: 49 (Hokkaido FY2003; Aomori FY2003; Iwate FY2003; Miyagi FY2003; Akita FY2003; Fukushima FY2003; Ibaraki FY2003; Tochigi FY2003; Gunma FY2003; Saitama FY2003; Chiba FY2003; Tokyo FY2003; Niigata FY2003; Toyama FY2003; Ishikawa FY2003; Fukui FY2003; Yamanashi FY2003; Nagano FY2003; Gifu FY2003; Shizuoka FY2003; Aichi FY2003; Mie FY2003; Shiga FY2003; Kyoto FY2003; Osaka FY2003; Hyogo FY2003; Nara FY2003; Wakayama FY2003; Tottori FY2003; Shimane FY2003; Okayama FY2003; Hiroshima FY2003; Yamaguchi FY2003; Tokushima FY2003; Ehime FY2003; Kochi FY2003; Saga FY2003; Nagasaki FY2003; Kumamoto FY2003; Oita FY2003; Miyazaki FY2003; Kagoshima FY2003; Hokkaido FY2020; Tokyo FY2020; Shizuoka FY2020; Kyoto FY2020; Osaka FY2020; Hiroshima FY2020; Yamaguchi FY2020).
- Other dates: none.

## 4. National average within the range

- The national weighted average lies between the lowest and highest prefecture in every year.

## 5. Against MHLW's stated national averages

- FY2025: file 1,121 yen, press release 1,121 yen: match.
- FY2024: file 1,055 yen, press release 1,055 yen: match.

## 6. Second reading of MHLW's file (python-calamine)

- 1,200 amounts read again: all 1,200 agree.

## Result

- All checks passed.
