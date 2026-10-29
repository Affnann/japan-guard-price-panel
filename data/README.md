# Data

## Sources

| Source | Publisher | URL | Downloaded on | License / terms |
|---|---|---|---|---|
| 公共工事設計労務単価 (public works design labor rates), yearly press releases FY2012–FY2026 | Ministry of Land, Infrastructure, Transport and Tourism (MLIT), Japan | https://www.mlit.go.jp/totikensangyo/const/1_6_bt_000217.html | 2026-10-29 | Public Data License 1.0 (PDL1.0), per https://www.mlit.go.jp/link.html |

Credit line for the MLIT files: 出典：「公共工事設計労務単価」（国土交通省） https://www.mlit.go.jp/totikensangyo/const/1_6_bt_000217.html. Any table in `data/clean/` is edited from these files (「公共工事設計労務単価」（国土交通省）を加工して作成) and is not an official MLIT product.

## Clean files: `data/clean/`

- `guard_rates_by_prefecture.csv`: guard A and B daily rates by prefecture and table year, built by `code/01_extract_mlit_rates.py`. Column definitions are in the main README.
- `checks_report.md`: output of `code/02_check.py`.

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
