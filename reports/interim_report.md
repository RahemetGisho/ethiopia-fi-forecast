# Interim Report — Ethiopia Financial Inclusion Forecasting

**10 Academy Week 11 — Selam Analytics**
**Author:** Rahmi &nbsp;|&nbsp; **Date:** 19 Jul 2026 &nbsp;|&nbsp; **Covers:** Task 1 (Data Enrichment) + Task 2 (EDA)

---

## 1. Data Enrichment Summary

Task 1 added **15 new rows to the main sheet** (12 observations + 2 events) and **4 new
`impact_link` rows**, growing the dataset from 43→58 main records and 14→18 impact links, while
leaving all original records unchanged (no corrections were needed).

**What was added, and why** (full citations in `data_enrichment_log.md`):

| Category                       | Additions                                                                                                                                                                                                                                                  | Purpose                                                                                                                  |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Direct-correlation supply-side | Bank branch density, ATM density, active-account share, active-agent share                                                                                                                                                                                 | Guide Sheet B — real Access/Usage predictors beyond Findex survey points                                                 |
| Indirect enablers/proxies      | Electricity access, adult literacy, internet penetration                                                                                                                                                                                                   | Guide Sheet C — explain _why_ Access can stall even when telecom products launch                                         |
| Gender & digital-skill detail  | Usage gender gap, mobile-money skill gap (M/F)                                                                                                                                                                                                             | Deepens the existing Access-only gender gap with a Usage-side and capability-side view                                   |
| Market-nuance evidence         | Sector-wide registered-vs-active mobile money figures (139.5M registered, only 15% active)                                                                                                                                                                 | Operationalizes Guide Sheet D's warning that headline registration numbers overstate real usage                          |
| New events                     | NBE Proclamation No. 1282/2023 (opened market to foreign providers); Directive NPS/10/2025 (interoperability mandate)                                                                                                                                      | Fill in the _legal preconditions_ for two already-catalogued events (Safaricom/M-Pesa entry; EthSwitch interoperability) |
| New impact_links               | 2 linking the new proclamation to M-Pesa entry/mobile-money account growth; 1 linking the interoperability directive to P2P growth (Tanzania comparable-country evidence); 1 linking the _existing_ NFIS-II event to the _new_ digital-skill-gap indicator | Makes an implicit causal chain in the starter data explicit and traceable                                                |

All additions came from IMF Financial Access Survey, World Bank/ESMAP, UNESCO, DataReportal
(GSMA Intelligence), and the National Bank of Ethiopia's own NDPS 2.0 strategy page — no figure
was estimated or invented. Two candidate additions (a newer, unsourced literacy estimate and a
GSMA Mobile Connectivity Index score) were considered and explicitly **rejected** for lack of a
traceable primary source; see the enrichment log's "Data NOT added" section.

---

## 2. Key Insights from EDA (with supporting evidence)

**1. Account ownership growth decelerated sharply after 2021.** +13pp (2014-17) and +11pp
(2017-21) growth slowed to just **+3pp over 2021-24** (46%→49%) despite Telebirr, Safaricom, and
NFIS-II all launching in that window. _(Figures 03-04)_

**2. There is a large, inconsistently-defined "registered vs. active" gap in Usage data.**
Sector-wide, ~139.5M mobile money accounts are registered but only **~15% are active** (NBE) —
compared with a self-reported **66% active rate for M-Pesa alone** (Safaricom). These are not
the same metric and should never be interchanged in a forecast. _(Figure 07)_

**3. The Access gender gap (18-20pp) is roughly double the Usage gender gap (10pp).** Once women
have an account, their usage looks close to parity; the bigger barrier is getting the account in
the first place. _(Figure 05)_

**4. Enabling infrastructure lags network coverage.** 4G coverage nearly doubled in two years
(37.5%→70.8%) while electricity access (55.4%) and literacy (~52%, 2017) barely moved — network
availability is no longer the binding constraint on Access; power and literacy plausibly are.
_(Figure 08)_

**5. Digital-skill gaps are large for both genders**, not just women (66% female / 60% male lack
mobile-money skills) — a broader capability constraint than the gender-gap figures alone suggest.
_(Figure 05)_

**6. The dataset is a genuinely sparse time series** — roughly 85% of indicators have only 1-2
observed years, which rules out conventional trend/seasonality forecasting and points toward the
task's suggested intervention/regression approach instead. _(Section 2 of the notebook)_

Full charts, code, and narrative: `notebooks/eda.ipynb` (executed, all outputs embedded).

---

## 3. Preliminary Event-Indicator Relationship Observations

- **Telebirr (May 2021) → Usage, fast:** Telebirr registered users grew explosively post-launch,
  consistent with the existing `IMP_0002` link (direct, high magnitude, 3-month lag).
- **Telebirr → Access, weak:** the Findex-measured Mobile Money Account _rate_ only reached 9.45%
  by 2024 — usage-product growth did not translate proportionally into Findex account ownership,
  reinforcing Insight 1 above.
- **Safaricom entry (Aug 2022) → 4G coverage:** timing lines up with the acceleration in 4G
  population coverage between the 2023 and 2025 observations, consistent with the starter
  dataset's own `IMP_0004` link.
- **New: Proclamation No. 1282/2023 (Feb 2023) → M-Pesa launch (Aug 2023):** a ~6-month lag between
  the legal market-opening and the actual product launch — now made explicit via `IMP_0015`.
- **M-Pesa entry (Aug 2023) → too recent for the 2024 Findex wave** to show an effect; a lag issue
  the forecasting model will need to handle explicitly (impact not yet "landed" in survey data).

**Caveat:** correlation analysis on this dataset is unreliable — most indicator pairs share only
1-2 overlapping years, so any correlation is close to definitionally ±1. The `impact_link` table
(expert/literature-based, now 18 records) is a more trustworthy signal than raw statistical
correlation at this stage; see Section 8 of the notebook for the pillar/relationship-type
breakdown.

---

## 4. Data Limitations Identified

- Sparse time series across nearly all indicators (1-2 observed years each).
- **Zero observations** for the QUALITY, TRUST, and DEPTH pillars, even after enrichment.
- Adult literacy figure is stale (2017); no verifiable, sourced update was found.
- No public urban/rural breakdown of the headline Access indicator (only Usage has a published
  rural-urban gap, from NBE).
- Definitional inconsistency between operator-reported and regulator-reported "active user" rates,
  previously undocumented in the dataset's `notes` field.

---
