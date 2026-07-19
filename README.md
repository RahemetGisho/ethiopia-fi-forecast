# Data Exploration & Enrichment

Enriches Selam Analytics' starter dataset (`data/raw/ethiopia_fi_unified_data.xlsx`) —
43 records, 14 impact links — with independently-sourced data to strengthen the
Access/Usage forecasting base.

## Run

```bash
python src/enrich_dataset.py
```

Reads `data/raw/`, writes the enriched workbook + CSVs to `data/processed/`. Idempotent —
re-running regenerates the same output from the same source additions defined in the
script.

## What was added

|              | Count | Examples                                                                                                               |
| ------------ | ----- | ---------------------------------------------------------------------------------------------------------------------- |
| Observations | +12   | Bank/ATM density, electricity access, literacy, active-account share, gender & digital-skill gaps                      |
| Events       | +2    | NBE Proclamation 1282/2023 (opened market to foreign providers); Directive NPS/10/2025 (interoperability mandate)      |
| Impact links | +4    | Proclamation → M-Pesa entry; interoperability directive → P2P growth; existing NFIS-II event → new skill-gap indicator |

**58 main records, 18 impact links total.** No original record was altered — additions
only. Every figure traces to a primary source (IMF FAS, World Bank/ESMAP, UNESCO,
DataReportal, NBE); nothing was estimated. Two candidates (an unsourced literacy
estimate, a GSMA index score) were evaluated and **rejected** for lack of a citable
source — see log for reasoning.

## Why these, specifically

The starter dataset had no enabling-infrastructure indicators and no sector-wide
"active account" figures. Both turned out load-bearing in Task 2: infrastructure
(electricity, literacy) explains why Access growth stalled despite telecom launches,
and the sector-wide active-account figure exposed a registered-vs-active gap that a
single operator's self-reported number was masking.

## Reference

Full per-record citations, exact source quotes, and confidence ratings:
**`data_enrichment_log.md`**. Schema/valid-values: `data/raw/reference_codes.xlsx`.

## Output

- `data/processed/ethiopia_fi_unified_data_enriched.xlsx` (+ `.csv`)
- `data/processed/impact_links_enriched.csv`
