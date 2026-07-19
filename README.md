# Ethiopia Financial Inclusion Forecasting

Forecasting Ethiopia's **Access** (Account Ownership) and **Usage** (Digital Payment
Adoption) indicators — per the World Bank Global Findex framework — for Selam Analytics,
a consortium of development finance institutions, mobile money operators, and the
National Bank of Ethiopia.

Ethiopia is a useful/hard case: Telebirr alone has 54M+ registered users, yet Findex
puts account ownership at only 49% (2024), up just 3pp since 2021. This project
reconciles that gap and builds toward a 2025–2027 forecast.

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
jupyter notebook notebooks/eda.ipynb
```

## Data Enrichment

`src/enrich_dataset.py` extends the starter dataset (`data/raw/`) with 12 observations,
2 events, and 4 impact links — every one sourced from IMF FAS, World Bank/ESMAP,
UNESCO, DataReportal, or NBE (no estimated figures). Output lands in `data/processed/`.

```bash
python src/enrich_dataset.py
```

Full citations, exact quotes, and confidence ratings for each addition: **`data_enrichment_log.md`**.

**Why it matters:** the starter dataset had no enabling-infrastructure indicators
(electricity, literacy) and no sector-wide "active account" figures — both turned out
to be central to explaining the Access slowdown and the Usage registered-vs-active gap
found in Task 2.

## Exploratory Data Analysis

`src/eda_analysis.py` generates all 11 charts (`reports/figures/`); `notebooks/eda.ipynb`
carries the full narrative and is executed with outputs embedded.

```bash
python src/eda_analysis.py
jupyter nbconvert --to notebook --execute --inplace notebooks/eda.ipynb
```

**Top findings:**

1. Account ownership growth collapsed from +11pp (2017–21) to +3pp (2021–24) despite
   Telebirr, Safaricom, and NFIS-II all launching in that window.
2. Sector-wide, only ~15% of 139.5M registered mobile money accounts are active (NBE) —
   vs. 66% self-reported by a single operator. Not the same metric; don't conflate them.
3. The Access gender gap (18–20pp) is roughly double the Usage gender gap (10pp).
4. 4G coverage nearly doubled in two years; electricity (55%) and literacy (~52%) didn't
   — connectivity is no longer the binding constraint on Access.
5. ~85% of indicators have only 1–2 observed years — this is a sparse-series problem,
   not a trend-forecasting one. See `reports/interim_report.docx` for the full writeup.

## Repo layout

```
data/raw/            starter datasets, unmodified
data/processed/       enriched dataset
src/                  enrichment + analysis code (idempotent, re-runnable)
notebooks/            eda.ipynb
reports/              interim_report.docx/.md, figures/
```

## Data quality caveats

Read before modeling: three pillars (Quality, Trust, Depth) have zero coverage;
"active user" is defined inconsistently across sources; adult literacy is a stale
2017 figure. Full list in `reports/interim_report.docx` §4.
