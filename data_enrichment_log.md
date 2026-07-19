# Data Enrichment Log

**Collected by:** Rahmet
**Collection date:** 2026-07-19
**Task:** 10 Academy Week 11 - Ethiopia Financial Inclusion Forecasting

This log documents every record added to `ethiopia_fi_unified_data.xlsx` during Task 1.
Fifteen new rows were added to the main sheet (12 observations + 2 events, record IDs
`REC_0034`-`REC_0046` and `EVT_0011`-`EVT_0012`) and four new rows to `Impact_sheet`
(`IMP_0015`-`IMP_0018`). The enrichment script that generates these programmatically is
`src/enrich_dataset.py`; outputs are written to `data/processed/`.

## Why these additions

Guided by the _Additional Data Points Guide_:

- **Sheet B (Direct Correlation):** bank branch/ATM density, active-account and active-agent
  shares.
- **Sheet C (Indirect Correlation / Enablers):** electricity access, adult literacy, internet
  penetration, mobile-money digital-skill gap.
- **Sheet D (Market Nuances):** the registered-vs-active gap is exactly the "P2P dominance /
  mobile-money-only users are rare" nuance the guide flags - Ethiopia's sector-wide active-account
  share (15%) is far below what operator-level self-reported activity rates (e.g., 66% for M-Pesa)
  would suggest, which matters for interpreting any Usage-pillar forecast.

Two new **events** were added because they were legally/operationally foundational but missing
from the original event catalogue: the 2023 proclamation that legally opened the market to
foreign providers (a precondition for the already-catalogued Safaricom/M-Pesa entry events), and
the 2025 interoperability-mandate directive (the regulatory precursor to the already-catalogued
EthSwitch/M-Pesa technical integration).

## New Observations

| record_id | Indicator                                           | Value  | Date       | Source                                       | Confidence |
| --------- | --------------------------------------------------- | ------ | ---------- | -------------------------------------------- | ---------- |
| REC_0034  | Commercial Bank Branches per 100k Adults            | 14.26  | 2023-12-31 | IMF FAS (via FRED)                           | high       |
| REC_0035  | ATMs per 100k Adults                                | 10.23  | 2023-12-31 | IMF FAS (via TheGlobalEconomy.com)           | high       |
| REC_0036  | Access to Electricity Rate                          | 55.4%  | 2023-12-31 | World Bank / ESMAP                           | high       |
| REC_0037  | Adult Literacy Rate                                 | 51.8%  | 2017-12-31 | UNESCO Institute for Statistics / World Bank | medium     |
| REC_0038  | Internet Penetration Rate                           | 21.3%  | 2025-01-01 | DataReportal Digital 2025: Ethiopia          | high       |
| REC_0039  | Total Registered Mobile Money Accounts (baseline)   | 12.2M  | 2020-12-31 | NBE - NDPS 2.0                               | high       |
| REC_0040  | Total Registered Mobile Money Accounts              | 139.5M | 2025-12-30 | NBE - NDPS 2.0                               | high       |
| REC_0041  | Active Mobile Money Account Share (sector-wide)     | 15%    | 2025-12-30 | NBE - NDPS 2.0                               | high       |
| REC_0042  | Active Mobile Money Agent Share                     | 25%    | 2025-12-30 | NBE - NDPS 2.0                               | high       |
| REC_0043  | Rural-Urban Digital Usage Gap                       | 24 pp  | 2025-12-30 | NBE - NDPS 2.0                               | high       |
| REC_0044  | Gender Gap in Digital Payment/MM Usage              | 10 pp  | 2025-12-30 | NBE - NDPS 2.0                               | high       |
| REC_0045  | Adults Lacking Mobile-Money Digital Skills (female) | 66%    | 2025-12-30 | NBE - NDPS 2.0                               | high       |
| REC_0046  | Adults Lacking Mobile-Money Digital Skills (male)   | 60%    | 2025-12-30 | NBE - NDPS 2.0                               | high       |

For each record's `source_url`, `original_text`, and detailed `notes` (why it's useful), see the
corresponding row in `data/processed/ethiopia_fi_unified_data_enriched.xlsx` - reproduced in full
in `src/enrich_dataset.py` for traceability.

**Note on REC_0037 (literacy):** flagged `medium` confidence deliberately - it is the latest
value World Bank/UNESCO has published for Ethiopia (2017), a seven-year-old figure by the time of
NDPS 2.0's later (unverifiable, un-cited) reference to "digital literacy" rates. We kept the
verifiable UNESCO figure rather than the unsourced newer estimate, and call out the gap as a data
limitation in the EDA notebook.

**Note on REC_0041 vs. existing REC_0025:** REC*0025 (`USG_ACTIVE_RATE`, 66%, Safaricom Results)
and REC_0041 (`USG_ACTIVE_ACCOUNT_SHARE`, 15%, NBE sector-wide) are \_not* duplicates - they use
different denominators (M-Pesa's own base vs. the entire sector's registered accounts) and are
kept as separate indicator codes on purpose. Conflating them would overstate national mobile-money
engagement.

## New Events

| record_id | Event                                                                                                   | Category   | Date       | Source                        | Confidence |
| --------- | ------------------------------------------------------------------------------------------------------- | ---------- | ---------- | ----------------------------- | ---------- |
| EVT_0011  | National Payment System (Amendment) Proclamation No. 1282/2023                                          | policy     | 2023-02-03 | Federal Negarit Gazette / NBE | high       |
| EVT_0012  | Payment Instrument Issuer (Amendment) Directive No. NPS/10/2025 (mobile money interoperability mandate) | regulation | 2025-05-27 | National Bank of Ethiopia     | high       |

Pillar left empty for both, per the schema convention that events are not pre-assigned to a
pillar - their effects are captured only through `impact_link` records (see below).

## New Impact Links

| record_id | parent_id                    | Related Indicator | Direction | Magnitude | Lag (months) | Evidence              | Confidence |
| --------- | ---------------------------- | ----------------- | --------- | --------- | ------------ | --------------------- | ---------- |
| IMP_0015  | EVT_0011                     | USG_MPESA_USERS   | increase  | high      | 6            | empirical             | high       |
| IMP_0016  | EVT_0011                     | ACC_MM_ACCOUNT    | increase  | medium    | 12           | theoretical           | medium     |
| IMP_0017  | EVT_0012                     | USG_P2P_COUNT     | increase  | medium    | 6            | literature (Tanzania) | medium     |
| IMP_0018  | EVT_0009 (NFIS-II, existing) | GEN_MM_SKILL_GAP  | decrease  | medium    | 36           | theoretical           | low        |

IMP*0015 and IMP_0016 formalize a causal chain that was implicit but undocumented in the starter
data: the 2023 proclamation (new) legally enabled the already-catalogued Safaricom/M-Pesa entry
events (EVT_0002/EVT_0003). IMP_0017 links the new interoperability directive to P2P transaction
growth, using Tanzania as comparable-country evidence per the schema's `evidence_basis`/
`comparable_country` fields. IMP_0018 links an \_existing* event (NFIS-II) to a _newly added_
indicator (the digital-skill gap), as encouraged by the task instructions.

## Data NOT added (considered and rejected)

- **Gender/urban-rural disaggregation of the headline 2024 Findex Account Ownership Rate:** the
  publicly available Findex 2024 country snapshot does not break Ethiopia's 49% figure down by
  urban/rural in the free summary; only the microdata (paid/registration-gated) would allow this.
  Flagged as a data gap in the EDA notebook rather than estimated.
- **GSMA Mobile Connectivity Index score for Ethiopia:** GSMA's index site did not surface a
  specific, citable current-year Ethiopia score in search results, so it was left out rather than
  guessed.
- **Newer (post-2017) Ethiopian adult literacy estimates (~66%)** found in secondary blog sources:
  excluded because we could not trace them to a primary UNESCO/World Bank/CSA release.

## Corrections to existing data

None - the original 43 main records and 14 impact_link records were reviewed but no
inconsistencies were found that warranted correction.
