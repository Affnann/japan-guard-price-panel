# japan-guard-price-panel

Japan's official daily pay rates for traffic guards on public works, for all 47 prefectures, every year from FY2012 to FY2026.

Every year Japan's Ministry of Land, Infrastructure, Transport and Tourism (MLIT) sets the *public works design labor rates* (公共工事設計労務単価): the daily wage that government cost estimates assume for each construction trade in each prefecture. Two of the trades are traffic guards working for private security companies:

- **Guard A** (交通誘導警備員A): a security company guard doing traffic guarding who has passed the national grade 1 or grade 2 traffic-guarding exam.
- **Guard B** (交通誘導警備員B): any other security company guard directing traffic.

This repo turns the ministry's yearly PDF tables into one clean table.

**Status:** work in progress. The MLIT panel is built and checked; job-openings data is still to be added.

## The data

`data/clean/guard_rates_by_prefecture.csv` has 1,410 rows: 15 table years x 47 prefectures x 2 grades.

| Column | Meaning |
|---|---|
| `table_year` | The year the table is published for (FY2012-FY2026) |
| `effective_from` | Month the rates took effect (YYYY-MM) |
| `pref_code`, `prefecture_ja`, `prefecture_en` | Prefecture (standard codes 01-47) |
| `grade` | A or B |
| `daily_rate_yen` | Rate in yen for a regular 8-hour working day |
| `special_rate` | `yes` if the source marks the figure as a special rate (see below) |
| `note` | What the special rate is |
| `source_file`, `source_page` | Where the figure is in `data/raw/mlit/` |

## What the numbers are, and are not

- **They are wages, not prices.** MLIT states that the rates cover only the wage paid to the worker. They exclude the security company's overheads, employer social insurance, training and profit, so they are well below what a client pays a security company per guard-day.
- They are set from MLIT's yearly survey of wages actually paid on public works, and are used to estimate costs for public contracts.
- **Special rates.** In FY2012-FY2022, Iwate, Miyagi and Fukushima carry special rates (round brackets in the source) set to reflect failed tenders after the 2011 earthquake. In FY2021, five prefectures carry rates under a special COVID-19 measure (angle brackets). These are marked in `special_rate`.
- **FY2013 jump.** Almost every prefecture rises more than 15% between FY2012 and FY2013. This matches MLIT's own figure of a 15.1% rise across all trades that year; it is not a data error.
- FY2012 calls the two grades 交通誘導員A/B; from FY2014 they are called 交通誘導警備員A/B.
- Before FY2007 the two grades were not separated, so the panel starts at FY2012, the earliest year MLIT links online.

## How it was checked

`code/02_check.py` writes `data/clean/checks_report.md`:

1. Every PDF was read twice with two different PDF engines (PyMuPDF and pdfplumber). All 1,410 values agree.
2. Every table year has all 47 prefectures and both grades.
3. All falls and rises above 15% were listed and looked at (only the FY2013 jump, explained above).
4. The simple average of the 47 prefectures was compared with MLIT's printed nationwide average where the release gives one.
5. A random sample of rows was checked by eye against the PDF pages.

## Reproduce

```
pip install -r requirements.txt
python code/01_extract_mlit_rates.py
python code/02_check.py
```

## Sources and license

- Data source: 「公共工事設計労務単価」（国土交通省）, https://www.mlit.go.jp/totikensangyo/const/1_6_bt_000217.html, used under the Public Data License 1.0. The clean table is edited from MLIT's files (「公共工事設計労務単価」（国土交通省）を加工して作成) and is not an official MLIT product. Details in [`data/README.md`](data/README.md).
- Code: MIT (see `LICENSE`). The clean dataset: CC BY 4.0.

## Cite

See [`CITATION.cff`](CITATION.cff).
