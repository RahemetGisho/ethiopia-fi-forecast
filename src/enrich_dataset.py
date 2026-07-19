import pandas as pd
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
PROCESSED_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

COLLECTED_BY = "Rahmet"
COLLECTION_DATE = "2026-07-19"

MAIN_COLS = [
    "record_id",
    "record_type",
    "category",
    "pillar",
    "indicator",
    "indicator_code",
    "indicator_direction",
    "value_numeric",
    "value_text",
    "value_type",
    "unit",
    "observation_date",
    "period_start",
    "period_end",
    "fiscal_year",
    "gender",
    "location",
    "region",
    "source_name",
    "source_type",
    "source_url",
    "confidence",
    "related_indicator",
    "relationship_type",
    "impact_direction",
    "impact_magnitude",
    "impact_estimate",
    "lag_months",
    "evidence_basis",
    "comparable_country",
    "collected_by",
    "collection_date",
    "original_text",
    "notes",
]
IMPACT_COLS = ["parent_id"] + MAIN_COLS  # record_id repeated at front of MAIN_COLS too


def base_row(**kwargs):
    row = {c: None for c in MAIN_COLS}
    row["collected_by"] = COLLECTED_BY
    row["collection_date"] = COLLECTION_DATE
    row["gender"] = "all"
    row["location"] = "national"
    row.update(kwargs)
    return row


# ---------------------------------------------------------------------------
# NEW OBSERVATIONS (record_type = observation)
# ---------------------------------------------------------------------------
new_observations = [
    base_row(
        record_id="REC_0034",
        record_type="observation",
        pillar="ACCESS",
        indicator="Commercial Bank Branches per 100,000 Adults",
        indicator_code="ACC_BANK_BRANCHES",
        indicator_direction="higher_better",
        value_numeric=14.26,
        value_type="rate",
        unit="per 100k adults",
        observation_date="2023-12-31",
        source_name="IMF Financial Access Survey (via FRED)",
        source_type="research",
        source_url="https://fred.stlouisfed.org/series/ETHFCBODCANUM",
        confidence="high",
        original_text="Geographical Outreach: Key Indicators Commercial Bank Branches Per 100,000 Adults for Ethiopia: 2023: 14.26221",
        notes="Direct-correlation supply-side indicator (Guide Sheet B). Complements Findex account-ownership survey data with physical access-point density; useful as an Access-pillar predictor and to contextualize the 2021-2024 account growth slowdown.",
    ),
    base_row(
        record_id="REC_0035",
        record_type="observation",
        pillar="ACCESS",
        indicator="ATMs per 100,000 Adults",
        indicator_code="ACC_ATM_DENSITY",
        indicator_direction="higher_better",
        value_numeric=10.23,
        value_type="rate",
        unit="per 100k adults",
        observation_date="2023-12-31",
        source_name="IMF Financial Access Survey (via TheGlobalEconomy.com)",
        source_type="research",
        source_url="https://www.theglobaleconomy.com/Ethiopia/ATM_machines/",
        confidence="high",
        original_text="Ethiopia: ATMs per 100,000 adults: The latest value from 2023 is 10.23 ATMs per 100,000 adults, an increase from 9.27 in 2022.",
        notes="Cross-checked against existing REC_0018/0019 ATM transaction volume figures; low ATM density relative to world average (52.8) helps explain why P2P mobile rails overtook ATM cash withdrawal (EVT_0006).",
    ),
    base_row(
        record_id="REC_0036",
        record_type="observation",
        pillar="ACCESS",
        indicator="Access to Electricity Rate",
        indicator_code="ACC_ELECTRICITY",
        indicator_direction="higher_better",
        value_numeric=55.4,
        value_type="percentage",
        unit="% of population",
        observation_date="2023-12-31",
        source_name="World Bank / ESMAP Tracking SDG7",
        source_type="research",
        source_url="https://data.worldbank.org/indicator/EG.ELC.ACCS.ZS?locations=ET",
        confidence="high",
        original_text="Access to electricity (% of population) in Ethiopia was reported at 55.4% in 2023.",
        notes="Indirect enabler/proxy variable (Guide Sheet C). Electrification is a hard constraint on smartphone charging, agent point operation, and network uptime, especially in rural areas.",
    ),
    base_row(
        record_id="REC_0037",
        record_type="observation",
        pillar="ACCESS",
        indicator="Adult Literacy Rate",
        indicator_code="ACC_LITERACY",
        indicator_direction="higher_better",
        value_numeric=51.8,
        value_type="percentage",
        unit="% of adults 15+",
        observation_date="2017-12-31",
        source_name="UNESCO Institute for Statistics / World Bank",
        source_type="research",
        source_url="https://data.worldbank.org/indicator/SE.ADT.LITR.ZS?locations=ET",
        confidence="medium",
        original_text="Literacy rate, adult total (% of people ages 15 and above) - Ethiopia: latest UNESCO/World Bank published value is 51.8% (2017).",
        notes="Indirect enabler (Guide Sheet C). Confidence set to medium: this is the latest year World Bank/UNESCO has published for Ethiopia as of data collection (known reporting lag) and it predates several more recent unofficial estimates (~66%) that could not be independently verified.",
    ),
    base_row(
        record_id="REC_0038",
        record_type="observation",
        pillar="ACCESS",
        indicator="Internet Penetration Rate",
        indicator_code="ACC_INTERNET_PEN",
        indicator_direction="higher_better",
        value_numeric=21.3,
        value_type="percentage",
        unit="% of population",
        observation_date="2025-01-01",
        source_name="DataReportal Digital 2025: Ethiopia (GSMA Intelligence / We Are Social)",
        source_type="research",
        source_url="https://datareportal.com/reports/digital-2025-ethiopia",
        confidence="high",
        original_text="There were 28.6 million internet users in Ethiopia in January 2025... Ethiopia's internet penetration rate stood at 21.3 percent of the total population.",
        notes="Indirect enabler (Guide Sheet C, mobile internet usage). Useful leading indicator for Usage-pillar forecasts and to contextualize the gap between 4G population coverage (REC_0010, 70.8%) and actual internet use.",
    ),
    base_row(
        record_id="REC_0039",
        record_type="observation",
        pillar="USAGE",
        indicator="Total Registered Mobile Money Accounts (All Providers)",
        indicator_code="USG_MM_ACCOUNTS_TOTAL",
        indicator_direction="higher_better",
        value_numeric=12200000,
        value_type="count",
        unit="accounts",
        observation_date="2020-12-31",
        source_name="National Bank of Ethiopia - NDPS 2.0",
        source_type="regulator",
        source_url="https://nbe.gov.et/ndps/",
        confidence="high",
        original_text="Mobile money accounts grew from 12.2 million (2020) to 139.5 million (2025).",
        notes="Baseline pre-Telebirr-era figure for sector-wide (all-provider) registered mobile money accounts; enables before/after comparison around EVT_0001 (Telebirr launch, May 2021).",
    ),
    base_row(
        record_id="REC_0040",
        record_type="observation",
        pillar="USAGE",
        indicator="Total Registered Mobile Money Accounts (All Providers)",
        indicator_code="USG_MM_ACCOUNTS_TOTAL",
        indicator_direction="higher_better",
        value_numeric=139500000,
        value_type="count",
        unit="accounts",
        observation_date="2025-12-30",
        source_name="National Bank of Ethiopia - NDPS 2.0",
        source_type="regulator",
        source_url="https://nbe.gov.et/ndps/",
        confidence="high",
        original_text="Mobile money accounts grew from 12.2 million (2020) to 139.5 million (2025). Annual transaction volumes grew at 146% CAGR and values at 161% CAGR.",
        notes="Sector-wide (all-provider) total, useful as the denominator context for REC_0041/REC_0042 (active-account and active-agent shares) which reveal a large registered-vs-active gap.",
    ),
    base_row(
        record_id="REC_0041",
        record_type="observation",
        pillar="USAGE",
        indicator="Active Mobile Money Account Share (Sector-wide)",
        indicator_code="USG_ACTIVE_ACCOUNT_SHARE",
        indicator_direction="higher_better",
        value_numeric=15.0,
        value_type="percentage",
        unit="% of registered accounts",
        observation_date="2025-12-30",
        source_name="National Bank of Ethiopia - NDPS 2.0",
        source_type="regulator",
        source_url="https://nbe.gov.et/ndps/",
        confidence="high",
        original_text="Only 15% of accounts and 25% of agents are active.",
        notes="Sector-wide (regulator) registered-vs-active gap. Notably lower than the 66% activity rate reported for M-Pesa alone (REC_0025, Safaricom Results), highlighting how operator self-reported activity rates and NBE sector-wide figures use different definitions/denominators - an important data-quality caveat for the Usage pillar.",
    ),
    base_row(
        record_id="REC_0042",
        record_type="observation",
        pillar="USAGE",
        indicator="Active Mobile Money Agent Share",
        indicator_code="USG_ACTIVE_AGENT_SHARE",
        indicator_direction="higher_better",
        value_numeric=25.0,
        value_type="percentage",
        unit="% of registered agents",
        observation_date="2025-12-30",
        source_name="National Bank of Ethiopia - NDPS 2.0",
        source_type="regulator",
        source_url="https://nbe.gov.et/ndps/",
        confidence="high",
        original_text="Only 15% of accounts and 25% of agents are active.",
        notes="Direct-correlation indicator (Guide Sheet B - agent network activity). Low active-agent share is a plausible supply-side explanation for weak cash-in/cash-out access outside Telebirr's own network.",
    ),
    base_row(
        record_id="REC_0043",
        record_type="observation",
        pillar="USAGE",
        indicator="Rural-Urban Digital Usage Gap",
        indicator_code="USG_RURAL_URBAN_GAP",
        indicator_direction="lower_better",
        value_numeric=24.0,
        value_type="gap_pp",
        unit="percentage points",
        observation_date="2025-12-30",
        source_name="National Bank of Ethiopia - NDPS 2.0",
        source_type="regulator",
        source_url="https://nbe.gov.et/ndps/",
        confidence="high",
        original_text="A 24-percentage-point rural-urban usage gap persists.",
        notes="New geographic-disaggregation indicator (Task instructions call out urban vs rural comparison). NBE only publishes this as a gap, not separate urban/rural levels, so it is recorded at national location scope like the existing gender-gap indicators (GEN_GAP_ACC).",
    ),
    base_row(
        record_id="REC_0044",
        record_type="observation",
        pillar="GENDER",
        indicator="Gender Gap in Digital Payment/Mobile Money Usage",
        indicator_code="GEN_GAP_USAGE",
        indicator_direction="lower_better",
        value_numeric=10.0,
        value_type="gap_pp",
        unit="percentage points",
        observation_date="2025-12-30",
        source_name="National Bank of Ethiopia - NDPS 2.0",
        source_type="regulator",
        source_url="https://nbe.gov.et/ndps/",
        confidence="high",
        original_text="Gender gap remains at 10 points.",
        notes="Companion metric to existing GEN_GAP_ACC (18-20pp Access gender gap). Usage gender gap (10pp) is narrower than the Access gender gap, suggesting that once women open an account they use it at a more comparable rate to men - an insight worth flagging.",
    ),
    base_row(
        record_id="REC_0045",
        record_type="observation",
        pillar="GENDER",
        gender="female",
        indicator="Adults Lacking Mobile-Money Digital Skills",
        indicator_code="GEN_MM_SKILL_GAP",
        indicator_direction="lower_better",
        value_numeric=66.0,
        value_type="percentage",
        unit="% of gender group",
        observation_date="2025-12-30",
        source_name="National Bank of Ethiopia - NDPS 2.0",
        source_type="regulator",
        source_url="https://nbe.gov.et/ndps/",
        confidence="high",
        original_text="Low digital literacy: 66% of women and 60% of men lack mobile-money skills.",
        notes="Indirect enabler (Guide Sheet C, digital literacy). Female record; see REC_0046 for the paired male figure. Directly relevant to the NFIS-II strategy's inclusion goals (EVT_0009) and to explaining why account ownership can rise while active usage lags.",
    ),
    base_row(
        record_id="REC_0046",
        record_type="observation",
        pillar="GENDER",
        gender="male",
        indicator="Adults Lacking Mobile-Money Digital Skills",
        indicator_code="GEN_MM_SKILL_GAP",
        indicator_direction="lower_better",
        value_numeric=60.0,
        value_type="percentage",
        unit="% of gender group",
        observation_date="2025-12-30",
        source_name="National Bank of Ethiopia - NDPS 2.0",
        source_type="regulator",
        source_url="https://nbe.gov.et/ndps/",
        confidence="high",
        original_text="Low digital literacy: 66% of women and 60% of men lack mobile-money skills.",
        notes="Male-gender companion record to REC_0045. Both genders show majority lacking mobile-money digital skills, indicating this is a broad-based (not purely gendered) constraint on Usage-pillar growth.",
    ),
]

# ---------------------------------------------------------------------------
# NEW EVENTS (record_type = event, pillar left empty per schema rule)
# ---------------------------------------------------------------------------
new_events = [
    base_row(
        record_id="EVT_0011",
        record_type="event",
        category="policy",
        indicator="National Payment System (Amendment) Proclamation No. 1282/2023",
        indicator_code="EVT_NPS_AMENDMENT_2023",
        value_text="Enacted",
        value_type="categorical",
        observation_date="2023-02-03",
        source_name="Federal Negarit Gazette / National Bank of Ethiopia",
        source_type="regulator",
        source_url="https://digitalpolicyalert.org/event/25718-implemented-national-payment-system-amendment-proclamation-no-12822023-amending-the-national-payment-system-proclamation-no-7182011-including-licensing-and-authorisation-requirements",
        confidence="high",
        original_text="On 3 February 2023, the National Payment System (Amendment) Proclamation No. 1282/2023 entered into force... Proclamation No. 1282/2023 opened entry to foreign providers.",
        notes="Foundational regulatory event not previously catalogued: this is the legal amendment that opened Ethiopia's payment system to foreign-owned entities, directly enabling Safaricom/M-Pesa's market entry (EVT_0002/EVT_0003) roughly 6 months later. Left pillar empty per schema convention; effects modeled via impact_links.",
    ),
    base_row(
        record_id="EVT_0012",
        record_type="event",
        category="regulation",
        indicator="Payment Instrument Issuer (Amendment) Directive No. NPS/10/2025 - Mobile Money Interoperability Mandate",
        indicator_code="EVT_NPS10_2025",
        value_text="Issued",
        value_type="categorical",
        observation_date="2025-05-27",
        source_name="National Bank of Ethiopia",
        source_type="regulator",
        source_url="https://nbe.gov.et/nbe_news/the-national-bank-of-ethiopia-has-issued-a-revised-directive-for-mobile-money-providers-to-promote-safety-competition-and-innovation/",
        confidence="high",
        original_text="The National Bank of Ethiopia issues the Licensing and Authorization of Payment Instrument Issuer (amendment) Directive No. NPS/10/2025... Mandates mandatory interoperability between mobile money wallets... Raising the daily electronic money transaction limits to 300,000 Birr and 150,000 Birr daily electronic money balance.",
        notes="Regulatory precursor to the M-Pesa/EthSwitch interoperability integration already catalogued as EVT_0007 (Oct 2025) - this is the enabling directive rather than the technical implementation, so both are kept as distinct, linked events.",
    ),
]

# ---------------------------------------------------------------------------
# NEW IMPACT LINKS (record_type = impact_link, sits in Impact_sheet with parent_id)
# ---------------------------------------------------------------------------
new_impact_links = [
    base_row(
        record_id="IMP_0015",
        record_type="impact_link",
        pillar="USAGE",
        related_indicator="USG_MPESA_USERS",
        relationship_type="enabling",
        impact_direction="increase",
        impact_magnitude="high",
        impact_estimate=None,
        lag_months=6,
        evidence_basis="empirical",
        confidence="high",
        source_name="Derived from EVT_0011 + EVT_0003 timing",
        source_type="calculated",
        notes="Proclamation No. 1282/2023 (Feb 2023) is the legal precondition that allowed the foreign-owned M-Pesa Ethiopia to be licensed; M-Pesa launched ~6 months later (Aug 2023, EVT_0003), matching the lag observed.",
    )
    | {"parent_id": "EVT_0011"},
    base_row(
        record_id="IMP_0016",
        record_type="impact_link",
        pillar="ACCESS",
        related_indicator="ACC_MM_ACCOUNT",
        relationship_type="enabling",
        impact_direction="increase",
        impact_magnitude="medium",
        impact_estimate=5.0,
        lag_months=12,
        evidence_basis="theoretical",
        confidence="medium",
        source_name="Analyst estimate",
        source_type="calculated",
        notes="By opening the market to foreign, well-capitalized entrants, the proclamation is theorized to have indirectly supported the rise in mobile money account ownership (ACC_MM_ACCOUNT rose from 4.7% in 2021 to 9.45% in 2024) via increased competition and marketing spend.",
    )
    | {"parent_id": "EVT_0011"},
    base_row(
        record_id="IMP_0017",
        record_type="impact_link",
        pillar="USAGE",
        related_indicator="USG_P2P_COUNT",
        relationship_type="direct",
        impact_direction="increase",
        impact_magnitude="medium",
        impact_estimate=10.0,
        lag_months=6,
        evidence_basis="literature",
        comparable_country="Tanzania",
        confidence="medium",
        source_name="Comparable-country evidence (Tanzania mobile money interoperability)",
        source_type="research",
        notes="Mandatory wallet interoperability has historically boosted P2P transaction counts in comparable East African markets (e.g., Tanzania's 2014 interoperability mandate); NPS/10/2025 (May 2025) is expected to have an analogous effect on Ethiopia's already-fast-growing P2P volumes (USG_P2P_COUNT).",
    )
    | {"parent_id": "EVT_0012"},
    base_row(
        record_id="IMP_0018",
        record_type="impact_link",
        pillar="GENDER",
        related_indicator="GEN_MM_SKILL_GAP",
        relationship_type="enabling",
        impact_direction="decrease",
        impact_magnitude="medium",
        impact_estimate=-10.0,
        lag_months=36,
        evidence_basis="theoretical",
        confidence="low",
        source_name="Analyst estimate based on NFIS-II strategy objectives",
        source_type="calculated",
        notes="NFIS-II (EVT_0009, launched Sep 2021) includes digital and financial literacy targets; expected over the multi-year strategy horizon to narrow the mobile-money digital-skill gap (GEN_MM_SKILL_GAP, currently 66% female / 60% male lacking skills), though this is a low-confidence theoretical link since no interim literacy survey has been run since the strategy launch.",
    )
    | {"parent_id": "EVT_0009"},
]


def main():
    xl = pd.ExcelFile(RAW_DIR / "ethiopia_fi_unified_data.xlsx")
    main_df = xl.parse("ethiopia_fi_unified_data")
    impact_df = xl.parse("Impact_sheet")

    new_main_df = pd.DataFrame(new_observations + new_events)[MAIN_COLS]
    enriched_main = pd.concat([main_df, new_main_df], ignore_index=True)

    new_impact_df = pd.DataFrame(new_impact_links)[["parent_id"] + MAIN_COLS]
    enriched_impact = pd.concat([impact_df, new_impact_df], ignore_index=True)

    out_xlsx = PROCESSED_DIR / "ethiopia_fi_unified_data_enriched.xlsx"
    with pd.ExcelWriter(out_xlsx, engine="openpyxl") as writer:
        enriched_main.to_excel(
            writer, sheet_name="ethiopia_fi_unified_data", index=False
        )
        enriched_impact.to_excel(writer, sheet_name="Impact_sheet", index=False)

    enriched_main.to_csv(
        PROCESSED_DIR / "ethiopia_fi_unified_data_enriched.csv", index=False
    )
    enriched_impact.to_csv(PROCESSED_DIR / "impact_links_enriched.csv", index=False)

    print(
        f"Original main records: {len(main_df)} -> Enriched: {len(enriched_main)} (+{len(new_main_df)})"
    )
    print(
        f"Original impact_links: {len(impact_df)} -> Enriched: {len(enriched_impact)} (+{len(new_impact_df)})"
    )
    print(f"Record type breakdown:\n{enriched_main['record_type'].value_counts()}")
    print(f"Saved: {out_xlsx}")


if __name__ == "__main__":
    main()
