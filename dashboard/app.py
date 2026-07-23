"""
Ethiopia Financial Inclusion Dashboard
Selam Analytics / 10 Academy Week 11

Run locally:
    streamlit run dashboard/app.py

See README.md "Running the Dashboard" section for setup details.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import impact_model as im  # noqa: E402
import forecast_model as fm  # noqa: E402

st.set_page_config(
    page_title="Ethiopia Financial Inclusion Dashboard",
    page_icon="📊",
    layout="wide",
)


# ---------------------------------------------------------------------------
# Data loading (cached)
# ---------------------------------------------------------------------------
@st.cache_data
def load_all():
    main, impact = im.load_data()
    impact_table = im.build_impact_table(main, impact)
    return main, impact, impact_table


main, impact, impact_table = load_all()

INDICATOR_LABELS = {
    "ACC_OWNERSHIP": "Account Ownership Rate (Access)",
    "ACC_MM_ACCOUNT": "Mobile Money Account Rate",
    "USG_DIGITAL_PAYMENT": "Digital Payment Usage Rate",
    "ACC_4G_COV": "4G Population Coverage",
    "ACC_MOBILE_PEN": "Mobile Phone Penetration",
    "USG_P2P_COUNT": "P2P Transaction Count",
    "USG_ATM_COUNT": "ATM Transaction Count",
    "USG_TELEBIRR_USERS": "Telebirr Registered Users",
    "USG_MPESA_USERS": "M-Pesa Registered Users",
    "USG_ACTIVE_RATE": "M-Pesa Active Rate (self-reported)",
    "USG_ACTIVE_ACCOUNT_SHARE": "Active Account Share (sector-wide, NBE)",
    "GEN_GAP_ACC": "Gender Gap - Access (pp)",
    "GEN_GAP_USAGE": "Gender Gap - Usage (pp)",
    "ACC_ELECTRICITY": "Electricity Access",
    "ACC_LITERACY": "Adult Literacy Rate",
    "ACC_INTERNET_PEN": "Internet Penetration",
    "USG_RURAL_URBAN_GAP": "Rural-Urban Usage Gap (pp)",
}


def get_obs(indicator_code, gender="all"):
    df = main[
        (main["indicator_code"] == indicator_code)
        & (main["record_type"] == "observation")
        & (main["gender"] == gender)
    ].copy()
    df["observation_date"] = pd.to_datetime(df["observation_date"])
    return df.sort_values("observation_date")


def latest_value(indicator_code, gender="all"):
    df = get_obs(indicator_code, gender)
    return df.iloc[-1] if len(df) else None


def download_button(df: pd.DataFrame, label: str, filename: str, key: str):
    st.download_button(
        label, df.to_csv(index=False).encode("utf-8"), filename, "text/csv", key=key
    )


# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------
st.sidebar.title("🇪🇹 Financial Inclusion")
st.sidebar.caption("Selam Analytics · 10 Academy")
page = st.sidebar.radio(
    "Navigate",
    ["Overview", "Trends", "Forecasts", "Inclusion Projections"],
    label_visibility="collapsed",
)
st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Data:** Global Findex, IMF FAS, World Bank, NBE, EthSwitch, operator reports "
    f"(58 main records, {main['record_type'].eq('observation').sum()} observations, "
    f"{len(impact)} modeled event-impact links)."
)
download_button(
    main, "⬇ Download full dataset (CSV)", "ethiopia_fi_dataset.csv", "dl_main_sidebar"
)

# ===========================================================================
# PAGE 1: OVERVIEW
# ===========================================================================
if page == "Overview":
    st.title("Ethiopia Financial Inclusion — Overview")
    st.caption(
        "Snapshot of the latest Access and Usage indicators, and where Ethiopia stands relative to its own targets."
    )

    acc = latest_value("ACC_OWNERSHIP")
    mm = latest_value("ACC_MM_ACCOUNT")
    dig_pay = latest_value("USG_DIGITAL_PAYMENT")
    crossover = latest_value("USG_CROSSOVER") if len(get_obs("USG_CROSSOVER")) else None
    active_share = latest_value("USG_ACTIVE_ACCOUNT_SHARE")
    gender_gap = latest_value("GEN_GAP_ACC")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(
        "Account Ownership (Access)", f"{acc['value_numeric']:.0f}%", "+3pp since 2021"
    )
    c2.metric(
        "Mobile Money Account Rate", f"{mm['value_numeric']:.2f}%", "+4.75pp since 2021"
    )

    if dig_pay is not None:
        c3.metric(
            "Digital Payment Usage",
            f"{dig_pay['value_numeric']:.0f}%",
            "+15pp since 2021*",
        )
    else:
        c3.metric(
            "Digital Payment Usage", "Not available", "No direct observation in dataset"
        )

    c4.metric(
        "Access Gender Gap",
        f"{gender_gap['value_numeric']:.0f}pp",
        "male − female",
        delta_color="inverse",
    )
    st.caption(
        "*2024 Digital Payment figure carries a documented source conflict — see Inclusion Projections page and `data_enrichment_log.md`."
    )

    st.markdown("---")
    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.subheader("📈 P2P / ATM Crossover Ratio")
        if crossover is not None:
            st.metric(
                "P2P transactions per ATM transaction",
                f"{crossover['value_numeric']:.2f}x",
                help="A ratio above 1.0 means peer-to-peer mobile transfers now exceed ATM cash withdrawals in volume.",
            )
        p2p = get_obs("USG_P2P_COUNT")
        atm = get_obs("USG_ATM_COUNT")
        fig = go.Figure()
        fig.add_bar(
            x=p2p["observation_date"].dt.year,
            y=p2p["value_numeric"] / 1e6,
            name="P2P transactions (M)",
            marker_color="#16a34a",
        )
        fig.add_bar(
            x=atm["observation_date"].dt.year,
            y=atm["value_numeric"] / 1e6,
            name="ATM transactions (M)",
            marker_color="#f59e0b",
        )
        fig.update_layout(
            barmode="group",
            height=320,
            margin=dict(t=20, b=20),
            yaxis_title="Millions of transactions",
            legend=dict(orientation="h", y=1.15),
        )
        st.plotly_chart(fig, width="stretch")
        st.caption(
            "For the first time, interoperable P2P mobile transfers have surpassed ATM cash withdrawals in transaction volume."
        )

    with col_b:
        st.subheader("🚀 Growth Rate Highlights")
        acc_series = get_obs("ACC_OWNERSHIP")
        acc_series = acc_series.assign(year=acc_series["observation_date"].dt.year)
        pp_change = acc_series["value_numeric"].diff()
        yr_gap = acc_series["year"].diff()
        rate = (pp_change / yr_gap).round(2)
        labels = [
            f"{int(y0)}-{int(y1)}"
            for y0, y1 in zip(acc_series["year"], acc_series["year"].shift(-1))
            if not pd.isna(y1)
        ]
        fig2 = go.Figure(
            go.Bar(
                x=labels,
                y=rate.dropna(),
                marker_color=[
                    "#16a34a" if r > 1.5 else "#dc2626" for r in rate.dropna()
                ],
                text=[f"{r:+.1f} pp/yr" for r in rate.dropna()],
                textposition="outside",
            )
        )
        fig2.update_layout(
            height=320,
            margin=dict(t=20, b=20),
            yaxis_title="Account ownership growth (pp/year)",
        )
        st.plotly_chart(fig2, width="stretch")
        st.caption(
            "Growth decelerated sharply after 2021 despite Telebirr, Safaricom, and NFIS-II all launching in that window — see Trends and Forecasts pages."
        )

    st.markdown("---")
    st.subheader("Active vs. Registered Mobile Money (sector-wide, NBE)")
    total = latest_value("USG_MM_ACCOUNTS_TOTAL")
    c5, c6, c7 = st.columns(3)
    c5.metric("Registered accounts", f"{total['value_numeric']/1e6:.0f}M")
    c6.metric(
        "Active account share",
        f"{active_share['value_numeric']:.0f}%",
        help="NBE sector-wide figure — notably lower than any single operator's self-reported activity rate.",
    )
    c7.metric(
        "Active agent share",
        f"{latest_value('USG_ACTIVE_AGENT_SHARE')['value_numeric']:.0f}%",
    )

# ===========================================================================
# PAGE 2: TRENDS
# ===========================================================================
elif page == "Trends":
    st.title("Trends Explorer")
    st.caption(
        "Interactive time series across all tracked indicators, with event overlays and channel comparisons."
    )

    all_obs = main[main["record_type"] == "observation"].copy()
    all_obs["observation_date"] = pd.to_datetime(all_obs["observation_date"])
    available_codes = [
        c for c in INDICATOR_LABELS if c in all_obs["indicator_code"].unique()
    ]

    col1, col2 = st.columns([2, 1])
    with col1:
        selected = st.multiselect(
            "Select indicators to plot",
            options=available_codes,
            default=["ACC_OWNERSHIP", "ACC_MM_ACCOUNT"],
            format_func=lambda c: INDICATOR_LABELS.get(c, c),
        )
    with col2:
        min_d, max_d = (
            all_obs["observation_date"].min().date(),
            all_obs["observation_date"].max().date(),
        )
        date_range = st.slider(
            "Date range", min_value=min_d, max_value=max_d, value=(min_d, max_d)
        )
    show_events = st.checkbox("Overlay cataloged events", value=True)

    if selected:
        fig = go.Figure()
        for code in selected:
            s = get_obs(code)
            s = s[
                (s["observation_date"].dt.date >= date_range[0])
                & (s["observation_date"].dt.date <= date_range[1])
            ]
            fig.add_scatter(
                x=s["observation_date"],
                y=s["value_numeric"],
                mode="lines+markers",
                name=INDICATOR_LABELS.get(code, code),
            )
        if show_events:
            events = main[main["record_type"] == "event"].copy()
            events["observation_date"] = pd.to_datetime(events["observation_date"])
            for _, e in events.iterrows():
                if date_range[0] <= e["observation_date"].date() <= date_range[1]:
                    fig.add_vline(
                        x=e["observation_date"].timestamp() * 1000,
                        line_dash="dot",
                        line_color="grey",
                        opacity=0.5,
                    )
        fig.update_layout(
            height=480,
            hovermode="x unified",
            yaxis_title="Value (% unless otherwise noted)",
            legend=dict(orientation="h", y=1.1),
        )
        st.plotly_chart(fig, width="stretch")
        download_button(
            all_obs[all_obs["indicator_code"].isin(selected)],
            "⬇ Download selected series (CSV)",
            "trends_selection.csv",
            "dl_trends",
        )
    else:
        st.info("Select at least one indicator above to plot.")

    st.markdown("---")
    st.subheader("Channel Comparison: Digital Payment Channels")
    channels = [
        "USG_P2P_COUNT",
        "USG_ATM_COUNT",
        "USG_TELEBIRR_USERS",
        "USG_MPESA_USERS",
    ]
    chan_df = all_obs[all_obs["indicator_code"].isin(channels)]
    fig3 = px.line(
        chan_df,
        x="observation_date",
        y="value_numeric",
        color="indicator_code",
        markers=True,
        labels={
            "value_numeric": "Count",
            "observation_date": "Date",
            "indicator_code": "Channel",
        },
    )
    fig3.for_each_trace(lambda t: t.update(name=INDICATOR_LABELS.get(t.name, t.name)))
    fig3.update_layout(height=420, legend=dict(orientation="h", y=1.15))
    st.plotly_chart(fig3, width="stretch")
    st.caption(
        "Telebirr dominates by registered-user count; P2P transaction volume overtook ATM volume in 2025 (see Overview page)."
    )

# ===========================================================================
# PAGE 3: FORECASTS
# ===========================================================================
elif page == "Forecasts":
    st.title("Forecasts: Access & Usage, 2025-2027")
    st.caption(
        "Trend regression + Ethiopia-calibrated event-impact model. See Task 4 notebook for full methodology."
    )

    target_map = {
        "Access — Account Ownership Rate": "ACC_OWNERSHIP",
        "Usage — Digital Payment Rate": "USG_DIGITAL_PAYMENT",
        "Usage (supporting) — Mobile Money Account Rate": "ACC_MM_ACCOUNT",
    }
    choice = st.selectbox("Select indicator to forecast", list(target_map.keys()))
    code = target_map[choice]

    model_choice = st.radio(
        "Model",
        ["Trend + calibrated events (recommended)", "Trend only (no event adjustment)"],
        horizontal=True,
    )

    series_check = fm.get_series(main, code)

    if len(series_check) >= 2:
        df, trend, series = fm.scenario_forecast(main, impact_table, code)
    else:
        df = pd.DataFrame()
        trend = None
        series = series_check
        st.warning(
            f"{INDICATOR_LABELS.get(code, code)} cannot be forecasted because "
            "there are fewer than 2 historical observations available."
        )

    fig = go.Figure()
    if df.empty:
        st.info(
            "Please select another indicator with sufficient historical data. "
            "USG_DIGITAL_PAYMENT requires additional validated observations "
            "before trend forecasting can be applied."
        )
        st.stop()
    fig.add_scatter(
        x=series["year_frac"],
        y=series["value_numeric"],
        mode="markers",
        name="Observed (Findex)",
        marker=dict(size=12, color="#1e293b"),
    )

    if model_choice.startswith("Trend +"):
        fig.add_scatter(
            x=df["year"],
            y=df["base_scenario"],
            mode="lines+markers",
            name="Base forecast",
            line=dict(color="#2563eb", width=3),
        )
        fig.add_scatter(
            x=df["year"],
            y=df["optimistic_scenario"],
            mode="lines+markers",
            name="Optimistic",
            line=dict(color="#16a34a", dash="dash"),
        )
        fig.add_scatter(
            x=df["year"],
            y=df["pessimistic_scenario"],
            mode="lines+markers",
            name="Pessimistic",
            line=dict(color="#dc2626", dash="dash"),
        )
        fig.add_scatter(
            x=list(df["year"]) + list(df["year"])[::-1],
            y=list(df["optimistic_scenario"]) + list(df["pessimistic_scenario"])[::-1],
            fill="toself",
            fillcolor="rgba(37,99,235,0.08)",
            line=dict(color="rgba(0,0,0,0)"),
            showlegend=False,
            hoverinfo="skip",
        )
    else:
        fig.add_scatter(
            x=df["year"],
            y=df["trend_point"],
            mode="lines+markers",
            name="Trend point forecast",
            line=dict(color="#2563eb", width=3),
        )
        fig.add_scatter(
            x=list(df["year"]) + list(df["year"])[::-1],
            y=list(df["trend_upper_95"]) + list(df["trend_lower_95"])[::-1],
            fill="toself",
            fillcolor="rgba(37,99,235,0.12)",
            line=dict(color="rgba(0,0,0,0)"),
            name="95% CI",
        )

    fig.update_layout(
        height=480,
        yaxis_title="% of adults",
        xaxis_title="Year",
        hovermode="x unified",
        legend=dict(orientation="h", y=1.12),
    )
    st.plotly_chart(fig, width="stretch")

    st.subheader("Key Projected Milestones")
    m1, m2, m3 = st.columns(3)
    m1.metric(
        f"2025 ({model_choice.split()[0]})",
        f"{df.loc[df.year==2025, 'base_scenario' if model_choice.startswith('Trend +') else 'trend_point'].values[0]:.1f}%",
    )
    m2.metric(
        "2026",
        f"{df.loc[df.year==2026, 'base_scenario' if model_choice.startswith('Trend +') else 'trend_point'].values[0]:.1f}%",
    )
    m3.metric(
        "2027",
        f"{df.loc[df.year==2027, 'base_scenario' if model_choice.startswith('Trend +') else 'trend_point'].values[0]:.1f}%",
    )

    if code == "ACC_OWNERSHIP":
        target = main[
            (main["indicator_code"] == "ACC_OWNERSHIP")
            & (main["record_type"] == "target")
        ]
        if len(target):
            gap = (
                target["value_numeric"].values[0]
                - df.loc[df.year == 2027, "base_scenario"].values[0]
            )
            st.warning(
                f"NFIS-II target: **{target['value_numeric'].values[0]:.0f}%** by end-2025. "
                f"Base-scenario 2027 forecast is **{gap:.0f}pp short** of that target."
            )

    st.dataframe(df, width="stretch")
    download_button(
        df, "⬇ Download forecast table (CSV)", f"forecast_{code}.csv", "dl_forecast"
    )

    with st.expander("⚠️ Key uncertainties — read before using these numbers"):
        st.markdown("""
- `USG_DIGITAL_PAYMENT` (the primary Usage target) has **no direct event linkage** in the impact model — its forecast rests on a 3-point trend line alone.
- The 2024 Usage anchor (35%) carries a **documented source conflict**; independent analysis suggests it could be closer to ~21%.
- Only 3-5 historical data points support each trend line — confidence intervals are wide by necessity, not by error.
- Event-effect calibration factors (Access ×0.16, Usage ×0.48) were validated against real 2021-2024 data; Gender/Affordability factors were not.
        """)

# ===========================================================================
# PAGE 4: INCLUSION PROJECTIONS
# ===========================================================================
elif page == "Inclusion Projections":
    st.title("Inclusion Projections & Scenario Planning")
    st.caption(
        "Progress toward financial inclusion targets, and direct answers to the consortium's guiding questions."
    )

    target_pct = st.slider(
        "Target Access rate (%) — adjust to compare against different policy goals",
        40,
        90,
        70,
        help="Ethiopia's own NFIS-II strategy target is 70% (loaded from the dataset). "
        "Move the slider to compare against a different benchmark, e.g. a round 60%.",
    )
    scenario = st.radio(
        "Scenario", ["Pessimistic", "Base", "Optimistic"], horizontal=True, index=1
    )
    scen_col = {
        "Pessimistic": "pessimistic_scenario",
        "Base": "base_scenario",
        "Optimistic": "optimistic_scenario",
    }[scenario]

    df_acc, _, series_acc = fm.scenario_forecast(main, impact_table, "ACC_OWNERSHIP")

    if len(fm.get_series(main, "USG_DIGITAL_PAYMENT")) >= 2:
        df_usg, _, series_usg = fm.scenario_forecast(
            main, impact_table, "USG_DIGITAL_PAYMENT"
        )
    else:
        df_usg = None
        series_usg = pd.DataFrame()

    current = series_acc["value_numeric"].iloc[-1]
    projected_2027 = df_acc.loc[df_acc.year == 2027, scen_col].values[0]

    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric("Current Access rate (2024)", f"{current:.0f}%")
        st.metric(f"Projected 2027 ({scenario.lower()})", f"{projected_2027:.0f}%")
        progress = min(projected_2027 / target_pct, 1.0)
        st.progress(
            progress,
            text=f"{progress*100:.0f}% of the way to a {target_pct}% target by 2027",
        )
        if projected_2027 >= target_pct:
            st.success(
                f"On the {scenario.lower()} path, Ethiopia reaches the {target_pct}% target by 2027."
            )
        else:
            st.error(
                f"On the {scenario.lower()} path, Ethiopia falls {target_pct - projected_2027:.0f}pp short of {target_pct}% by 2027."
            )

    with col2:
        fig = go.Figure()
        fig.add_scatter(
            x=series_acc["year_frac"],
            y=series_acc["value_numeric"],
            mode="markers+lines",
            name="Observed",
            marker=dict(size=10, color="#1e293b"),
            line=dict(color="#1e293b"),
        )
        fig.add_scatter(
            x=df_acc["year"],
            y=df_acc[scen_col],
            mode="lines+markers",
            name=f"{scenario} forecast",
            line=dict(color="#2563eb", width=3),
        )
        fig.add_hline(
            y=target_pct,
            line_dash="dash",
            line_color="#dc2626",
            annotation_text=f"Target: {target_pct}%",
            annotation_position="top left",
        )
        fig.update_layout(
            height=380, yaxis_title="% of adults with an account", margin=dict(t=30)
        )
        st.plotly_chart(fig, width="stretch")

    st.markdown("---")
    st.subheader("Answers to the Consortium's Key Questions")

    with st.expander("❓ What drives financial inclusion in Ethiopia?", expanded=True):
        st.markdown("""
Usage-side product launches (Telebirr, M-Pesa) drove *engagement*, not first-time *access*.
The real gate on Access growth is slower-moving enabling infrastructure — electricity access
(55.4%) and adult literacy (~52%) — not telecom coverage, which nearly doubled (37.5% → 70.8%
4G coverage) without a proportional Access response. See Task 2 EDA and Task 3 validation.
        """)

    with st.expander(
        "❓ How do events (policies, launches, infrastructure) affect indicators?"
    ):
        st.markdown("""
Quantified in the Task 3 association matrix: events reaching `ACC_MM_ACCOUNT` (M-Pesa launch,
the 2023 market-opening proclamation) have the most *validated* impact. Literature-based estimates
borrowed from comparable countries (Kenya, India) overpredict Ethiopia's actual Access response by
~6x — Ethiopia's own infrastructure constraints dampen the effect substantially versus its peers.
        """)

    with st.expander(
        "❓ How did financial inclusion change in 2025, and where is it headed 2026-2027?"
    ):
        st.markdown(f"""
Base-scenario forecast: Access reaches **{df_acc.loc[df_acc.year==2027,'base_scenario'].values[0]:.0f}%**
by 2027. Digital Payment Usage does not have sufficient historical observations in the dataset to
generate a forecast here. It requires additional validated historical data because the indicator has
no direct event linkage and cannot support trend regression. Treat the Access forecast as a planning
assumption, and the pessimistic scenario as a budget floor.
        """)

    st.markdown("---")
    st.caption(
        "Full methodology, validation, and all documented assumptions/limitations: see `notebooks/impact_modeling.ipynb`, "
        "`notebooks/forecasting.ipynb`, and the Final Report."
    )
