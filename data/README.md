# Data

## Sources

| Source | Publisher | URL | Downloaded on | License / terms |
|---|---|---|---|---|
| 公共工事設計労務単価 (public works design labor rates), yearly press releases FY2012–FY2026 | Ministry of Land, Infrastructure, Transport and Tourism (MLIT), Japan | https://www.mlit.go.jp/totikensangyo/const/1_6_bt_000217.html | 2026-10-29 | Public Data License 1.0 (PDL1.0), per https://www.mlit.go.jp/link.html |
| 一般職業紹介状況（職業安定業務統計）, long time-series table 21 (職業別労働市場関係指標) | Ministry of Health, Labour and Welfare (MHLW), Japan, via e-Stat | https://www.e-stat.go.jp/stat-search/files?toukei=00450222&tstat=000001020327 | 2026-10-29 | e-Stat terms of use (Government Standard Terms of Use 2.0, compatible with CC BY 4.0), per https://www.e-stat.go.jp/terms-of-use |
| 賃金構造基本統計調査 (Basic Survey on Wage Structure), prefecture tables by occupation and sex, survey years 2012-2025 | MHLW, via e-Stat | https://www.e-stat.go.jp/stat-search/files?toukei=00450091&tstat=000001011429 | 2026-11-01 | e-Stat terms of use (Government Standard Terms of Use 2.0, compatible with CC BY 4.0), per https://www.e-stat.go.jp/terms-of-use |
| 平成14年度から令和８年度までの地域別最低賃金改定状況 (prefecture minimum wages, FY2002-FY2026) | MHLW | https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/koyou_roudou/roudoukijun/minimumichiran/ | 2026-11-01 | Public Data License 1.0 (PDL1.0), per https://www.mhlw.go.jp/chosakuken/index.html |

Credit line for the MLIT files: 出典：「公共工事設計労務単価」（国土交通省） https://www.mlit.go.jp/totikensangyo/const/1_6_bt_000217.html. Any table in `data/clean/` is edited from these files (「公共工事設計労務単価」（国土交通省）を加工して作成) and is not an official MLIT product.

## Clean files: `data/clean/`

- `guard_rates_by_prefecture.csv`: guard A and B daily rates by prefecture and table year, built by `code/01_extract_mlit_rates.py`. Column definitions are in the main README.
- `checks_report.md`: output of `code/02_check.py`.
- `security_jobs_monthly.csv`: monthly job-openings figures for security occupations and all occupations, built by `code/03_extract_mhlw_jobs.py`.
- `checks_report_jobs.md`: output of `code/04_check_mhlw_jobs.py`.
- `pay_by_prefecture.csv`: pay of security guards, building cleaners and (to 2019) gatekeepers by prefecture, survey years 2012-2025, built by `code/06_extract_mhlw_wages.py`. Column definitions are in the main README.
- `checks_report_pay.md`: output of `code/07_check_mhlw_wages.py`.
- `minimum_wage_by_prefecture.csv`: prefecture minimum wages and their effective dates, FY2002-FY2026, built by `code/08_extract_minimum_wages.py`.
- `checks_report_minwage.md`: output of `code/09_check_minimum_wages.py`.

## Raw files: `data/raw/mlit/`

File names start with the month the rates took effect (YYYY-MM) and the Japanese fiscal year they cover (April–March). `release` is the main press release with the rate tables; `reference` is the supporting material published with it.

| File | Original URL |
|---|---|
| 2012-00_tohoku-3pref_release.pdf | https://www.mlit.go.jp/common/000191739.pdf |
| 2012-04_FY2012_release.pdf | https://www.mlit.go.jp/common/000205321.pdf |
| 2012-04_FY2012_reference.pdf | https://www.mlit.go.jp/common/000205840.pdf |
| 2012-06_tohoku-3pref_release.pdf | https://www.mlit.go.jp/common/000214214.pdf |
| 2013-04_FY2013_release.pdf | https://www.mlit.go.jp/common/000993048.pdf |
| 2013-04_FY2013_reference.pdf | https://www.mlit.go.jp/common/000993051.pdf |
| 2014-02_FY2014_release.pdf | https://www.mlit.go.jp/common/001026047.pdf |
| 2014-02_FY2014_reference.pdf | https://www.mlit.go.jp/common/001026048.pdf |
| 2014-04_FY2014-revision_release.pdf | https://www.mlit.go.jp/common/001031566.pdf |
| 2015-02_FY2015_release.pdf | https://www.mlit.go.jp/common/001067649.pdf |
| 2015-02_FY2015_reference.pdf | https://www.mlit.go.jp/common/001067648.pdf |
| 2016-02_FY2016_release.pdf | https://www.mlit.go.jp/common/001116339.pdf |
| 2016-02_FY2016_reference.pdf | https://www.mlit.go.jp/common/001116340.pdf |
| 2017-03_FY2017_release.pdf | https://www.mlit.go.jp/common/001172245.pdf |
| 2017-03_FY2017_reference.pdf | https://www.mlit.go.jp/common/001172244.pdf |
| 2018-03_FY2018_release.pdf | https://www.mlit.go.jp/common/001221741.pdf |
| 2018-03_FY2018_reference.pdf | https://www.mlit.go.jp/common/001221740.pdf |
| 2019-03_FY2019_release.pdf | https://www.mlit.go.jp/common/001274167.pdf |
| 2020-03_FY2020_release.pdf | https://www.mlit.go.jp/report/press/content/001328838.pdf |
| 2021-03_FY2021_release.pdf | https://www.mlit.go.jp/common/001387434.pdf |
| 2022-03_FY2022_release.pdf | https://www.mlit.go.jp/report/press/content/001464445.pdf |
| 2023-03_FY2023_release.pdf | https://www.mlit.go.jp/report/press/content/001587029.pdf |
| 2024-03_FY2024_release.pdf | https://www.mlit.go.jp/report/press/content/001724088.pdf |
| 2025-03_FY2025_release.pdf | https://www.mlit.go.jp/report/press/content/001864366.pdf |
| 2026-03_FY2026_release.pdf | https://www.mlit.go.jp/report/press/content/001981942.pdf |

Notes:
- `2014-04_FY2014-revision_release.pdf` contains no new rates: it says the rates published on 30 January 2014 stay in force from April 2014.
- The two `tohoku-3pref` files are mid-year special rates for Iwate, Miyagi and Fukushima after the 2011 earthquake.

## Raw files: `data/raw/mhlw/`

Credit line: 出典：「一般職業紹介状況（職業安定業務統計）」（厚生労働省）, e-Stat. Tables in `data/clean/` are edited from these files.

| File | What it is | Original URL |
|---|---|---|
| occ_2012-03_to_2023-03.xlsx | Table 21, occupation figures, MHLW classification (4th revision), March 2012-March 2023 (old format, published 2024-03-29) | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040050660&fileKind=0 |
| occ_2023-04_onward.xlsx | Table 21, occupation figures, Japan Standard Occupational Classification, April 2022-August 2026 (published 2026-10-02) | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040505332&fileKind=0 |
| occupation_classification_from_2023-04.pdf | MHLW's note on the change of occupation classification from April 2023 | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040505339&fileKind=2 |

## Raw files: `data/raw/mhlw_wages/`

Credit line: 出典：「賃金構造基本統計調査」（厚生労働省）, e-Stat. Tables in `data/clean/` are edited from these files.

Each survey year's prefecture table by occupation and sex comes in four files, split by prefecture. For 2012-2019 it is 都道府県別第2表 (職種・性別きまって支給する現金給与額、所定内給与額及び年間賞与その他特別給与額). For 2020-2025 it is 都道府県別第3表 (都道府県、職種（特掲）、性別…（産業計）), which covers all workers, and 都道府県別参考表4, the same table without position holders (役職者を除く; files ending `_excl-positions`). Where e-Stat offers only its viewing version of a file (fileKind=4), that version was downloaded.

| File | Table | Prefectures | Original URL |
|---|---|---|---|
| wage_2012_a_zenkoku-saitama.xls | 2012 第2表 | Japan to Saitama | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000016356582&fileKind=0 |
| wage_2012_b_chiba-aichi.xls | 2012 第2表 | Chiba to Aichi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000016356583&fileKind=0 |
| wage_2012_c_mie-yamaguchi.xls | 2012 第2表 | Mie to Yamaguchi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000016356584&fileKind=0 |
| wage_2012_d_tokushima-okinawa.xls | 2012 第2表 | Tokushima to Okinawa | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000016356585&fileKind=0 |
| wage_2013_a_zenkoku-saitama.xls | 2013 第2表 | Japan to Saitama | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000023602754&fileKind=0 |
| wage_2013_b_chiba-aichi.xls | 2013 第2表 | Chiba to Aichi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000023602755&fileKind=0 |
| wage_2013_c_mie-yamaguchi.xls | 2013 第2表 | Mie to Yamaguchi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000023602756&fileKind=0 |
| wage_2013_d_tokushima-okinawa.xls | 2013 第2表 | Tokushima to Okinawa | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000023602757&fileKind=0 |
| wage_2014_a_zenkoku-saitama.xls | 2014 第2表 | Japan to Saitama | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000028447490&fileKind=0 |
| wage_2014_b_chiba-aichi.xls | 2014 第2表 | Chiba to Aichi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000028447491&fileKind=0 |
| wage_2014_c_mie-yamaguchi.xls | 2014 第2表 | Mie to Yamaguchi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000028447492&fileKind=0 |
| wage_2014_d_tokushima-okinawa.xls | 2014 第2表 | Tokushima to Okinawa | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000028447493&fileKind=0 |
| wage_2015_a_zenkoku-saitama.xls | 2015 第2表 | Japan to Saitama | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000028996937&fileKind=0 |
| wage_2015_b_chiba-aichi.xls | 2015 第2表 | Chiba to Aichi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000028996938&fileKind=0 |
| wage_2015_c_mie-yamaguchi.xls | 2015 第2表 | Mie to Yamaguchi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000028996939&fileKind=0 |
| wage_2015_d_tokushima-okinawa.xls | 2015 第2表 | Tokushima to Okinawa | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000028996940&fileKind=0 |
| wage_2016_a_zenkoku-saitama.xls | 2016 第2表 | Japan to Saitama | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000031228832&fileKind=0 |
| wage_2016_b_chiba-aichi.xls | 2016 第2表 | Chiba to Aichi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000031228833&fileKind=0 |
| wage_2016_c_mie-yamaguchi.xls | 2016 第2表 | Mie to Yamaguchi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000031228834&fileKind=0 |
| wage_2016_d_tokushima-okinawa.xls | 2016 第2表 | Tokushima to Okinawa | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000031228835&fileKind=0 |
| wage_2017_a_zenkoku-saitama.xls | 2017 第2表 | Japan to Saitama | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000031559894&fileKind=0 |
| wage_2017_b_chiba-aichi.xls | 2017 第2表 | Chiba to Aichi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000031559895&fileKind=0 |
| wage_2017_c_mie-yamaguchi.xls | 2017 第2表 | Mie to Yamaguchi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000031559896&fileKind=0 |
| wage_2017_d_tokushima-okinawa.xls | 2017 第2表 | Tokushima to Okinawa | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000031559897&fileKind=0 |
| wage_2018_a_zenkoku-saitama.xls | 2018 第2表 | Japan to Saitama | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000031683192&fileKind=0 |
| wage_2018_b_chiba-aichi.xls | 2018 第2表 | Chiba to Aichi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000031683193&fileKind=0 |
| wage_2018_c_mie-yamaguchi.xls | 2018 第2表 | Mie to Yamaguchi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000031683194&fileKind=0 |
| wage_2018_d_tokushima-okinawa.xls | 2018 第2表 | Tokushima to Okinawa | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000031683195&fileKind=0 |
| wage_2019_a_zenkoku-saitama.xls | 2019 第2表 | Japan to Saitama | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000031919907&fileKind=0 |
| wage_2019_b_chiba-aichi.xls | 2019 第2表 | Chiba to Aichi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000031919908&fileKind=0 |
| wage_2019_c_mie-yamaguchi.xls | 2019 第2表 | Mie to Yamaguchi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000031919909&fileKind=0 |
| wage_2019_d_tokushima-okinawa.xls | 2019 第2表 | Tokushima to Okinawa | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000031919910&fileKind=0 |
| wage_2020_a_zenkoku-saitama.xls | 2020 第3表 | Japan to Saitama | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032069529&fileKind=0 |
| wage_2020_b_chiba-aichi.xls | 2020 第3表 | Chiba to Aichi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032069530&fileKind=0 |
| wage_2020_c_mie-yamaguchi.xls | 2020 第3表 | Mie to Yamaguchi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032069531&fileKind=0 |
| wage_2020_d_tokushima-okinawa.xls | 2020 第3表 | Tokushima to Okinawa | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032069532&fileKind=0 |
| wage_2020_a_zenkoku-saitama_excl-positions.xlsx | 2020 参考表4 (excluding position holders) | Japan to Saitama | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032187173&fileKind=0 |
| wage_2020_b_chiba-aichi_excl-positions.xlsx | 2020 参考表4 (excluding position holders) | Chiba to Aichi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032187194&fileKind=0 |
| wage_2020_c_mie-yamaguchi_excl-positions.xlsx | 2020 参考表4 (excluding position holders) | Mie to Yamaguchi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032187195&fileKind=0 |
| wage_2020_d_tokushima-okinawa_excl-positions.xlsx | 2020 参考表4 (excluding position holders) | Tokushima to Okinawa | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032187196&fileKind=0 |
| wage_2021_a_zenkoku-saitama.xlsx | 2021 第3表 | Japan to Saitama | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032183050&fileKind=4 |
| wage_2021_b_chiba-aichi.xlsx | 2021 第3表 | Chiba to Aichi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032183051&fileKind=4 |
| wage_2021_c_mie-yamaguchi.xlsx | 2021 第3表 | Mie to Yamaguchi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032183052&fileKind=4 |
| wage_2021_d_tokushima-okinawa.xlsx | 2021 第3表 | Tokushima to Okinawa | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032183053&fileKind=4 |
| wage_2021_a_zenkoku-saitama_excl-positions.xlsx | 2021 参考表4 (excluding position holders) | Japan to Saitama | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032183063&fileKind=4 |
| wage_2021_b_chiba-aichi_excl-positions.xlsx | 2021 参考表4 (excluding position holders) | Chiba to Aichi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032183064&fileKind=4 |
| wage_2021_c_mie-yamaguchi_excl-positions.xlsx | 2021 参考表4 (excluding position holders) | Mie to Yamaguchi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032183065&fileKind=4 |
| wage_2021_d_tokushima-okinawa_excl-positions.xlsx | 2021 参考表4 (excluding position holders) | Tokushima to Okinawa | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032183066&fileKind=4 |
| wage_2022_a_zenkoku-saitama.xlsx | 2022 第3表 | Japan to Saitama | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040029279&fileKind=4 |
| wage_2022_b_chiba-aichi.xlsx | 2022 第3表 | Chiba to Aichi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040029280&fileKind=4 |
| wage_2022_c_mie-yamaguchi.xlsx | 2022 第3表 | Mie to Yamaguchi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040029281&fileKind=4 |
| wage_2022_d_tokushima-okinawa.xlsx | 2022 第3表 | Tokushima to Okinawa | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040029282&fileKind=4 |
| wage_2022_a_zenkoku-saitama_excl-positions.xlsx | 2022 参考表4 (excluding position holders) | Japan to Saitama | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040029292&fileKind=4 |
| wage_2022_b_chiba-aichi_excl-positions.xlsx | 2022 参考表4 (excluding position holders) | Chiba to Aichi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040029293&fileKind=4 |
| wage_2022_c_mie-yamaguchi_excl-positions.xlsx | 2022 参考表4 (excluding position holders) | Mie to Yamaguchi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040029294&fileKind=4 |
| wage_2022_d_tokushima-okinawa_excl-positions.xlsx | 2022 参考表4 (excluding position holders) | Tokushima to Okinawa | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040029295&fileKind=4 |
| wage_2023_a_zenkoku-saitama.xlsx | 2023 第3表 | Japan to Saitama | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040163839&fileKind=4 |
| wage_2023_b_chiba-aichi.xlsx | 2023 第3表 | Chiba to Aichi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040163840&fileKind=4 |
| wage_2023_c_mie-yamaguchi.xlsx | 2023 第3表 | Mie to Yamaguchi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040163841&fileKind=4 |
| wage_2023_d_tokushima-okinawa.xlsx | 2023 第3表 | Tokushima to Okinawa | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040163842&fileKind=4 |
| wage_2023_a_zenkoku-saitama_excl-positions.xlsx | 2023 参考表4 (excluding position holders) | Japan to Saitama | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040163852&fileKind=4 |
| wage_2023_b_chiba-aichi_excl-positions.xlsx | 2023 参考表4 (excluding position holders) | Chiba to Aichi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040163853&fileKind=4 |
| wage_2023_c_mie-yamaguchi_excl-positions.xlsx | 2023 参考表4 (excluding position holders) | Mie to Yamaguchi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040163854&fileKind=4 |
| wage_2023_d_tokushima-okinawa_excl-positions.xlsx | 2023 参考表4 (excluding position holders) | Tokushima to Okinawa | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040163855&fileKind=4 |
| wage_2024_a_zenkoku-saitama.xlsx | 2024 第3表 | Japan to Saitama | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040247952&fileKind=4 |
| wage_2024_b_chiba-aichi.xlsx | 2024 第3表 | Chiba to Aichi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040247953&fileKind=4 |
| wage_2024_c_mie-yamaguchi.xlsx | 2024 第3表 | Mie to Yamaguchi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040247954&fileKind=4 |
| wage_2024_d_tokushima-okinawa.xlsx | 2024 第3表 | Tokushima to Okinawa | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040247955&fileKind=4 |
| wage_2024_a_zenkoku-saitama_excl-positions.xlsx | 2024 参考表4 (excluding position holders) | Japan to Saitama | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040247965&fileKind=4 |
| wage_2024_b_chiba-aichi_excl-positions.xlsx | 2024 参考表4 (excluding position holders) | Chiba to Aichi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040247966&fileKind=4 |
| wage_2024_c_mie-yamaguchi_excl-positions.xlsx | 2024 参考表4 (excluding position holders) | Mie to Yamaguchi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040247967&fileKind=4 |
| wage_2024_d_tokushima-okinawa_excl-positions.xlsx | 2024 参考表4 (excluding position holders) | Tokushima to Okinawa | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040247968&fileKind=4 |
| wage_2025_a_zenkoku-saitama.xlsx | 2025 第3表 | Japan to Saitama | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040421195&fileKind=4 |
| wage_2025_b_chiba-aichi.xlsx | 2025 第3表 | Chiba to Aichi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040421196&fileKind=4 |
| wage_2025_c_mie-yamaguchi.xlsx | 2025 第3表 | Mie to Yamaguchi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040421197&fileKind=4 |
| wage_2025_d_tokushima-okinawa.xlsx | 2025 第3表 | Tokushima to Okinawa | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040421198&fileKind=4 |
| wage_2025_a_zenkoku-saitama_excl-positions.xlsx | 2025 参考表4 (excluding position holders) | Japan to Saitama | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040421208&fileKind=4 |
| wage_2025_b_chiba-aichi_excl-positions.xlsx | 2025 参考表4 (excluding position holders) | Chiba to Aichi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040421209&fileKind=4 |
| wage_2025_c_mie-yamaguchi_excl-positions.xlsx | 2025 参考表4 (excluding position holders) | Mie to Yamaguchi | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040421210&fileKind=4 |
| wage_2025_d_tokushima-okinawa_excl-positions.xlsx | 2025 参考表4 (excluding position holders) | Tokushima to Okinawa | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040421211&fileKind=4 |

## Raw files: `data/raw/mhlw_minwage/`

Credit line: 出典：「平成14年度から令和８年度までの地域別最低賃金改定状況」（厚生労働省）. The table in `data/clean/` is edited from this file (「地域別最低賃金改定状況」（厚生労働省）を加工して作成) and is not an official MHLW product.

| File | Original URL |
|---|---|
| minwage_FY2002-FY2026.xlsx | https://www.mhlw.go.jp/content/11200000/001756130.xlsx |
