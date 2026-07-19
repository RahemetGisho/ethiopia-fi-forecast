import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path

plt.rcParams["figure.dpi"] = 110
plt.rcParams["font.size"] = 10
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False

ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = ROOT / "reports" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

COLORS = {
    "ACCESS": "#2563eb",
    "USAGE": "#16a34a",
    "GENDER": "#db2777",
    "AFFORDABILITY": "#d97706",
    "QUALITY": "#7c3aed",
    "TRUST": "#0891b2",
    "DEPTH": "#64748b",
}


def load_data():
    xl = pd.ExcelFile(
        ROOT / "data" / "processed" / "ethiopia_fi_unified_data_enriched.xlsx"
    )
    main = xl.parse("ethiopia_fi_unified_data")
    impact = xl.parse("Impact_sheet")
    main["observation_date"] = pd.to_datetime(main["observation_date"], errors="coerce")
    main["year"] = main["observation_date"].dt.year
    return main, impact


def fig_record_overview(df):
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    df["record_type"].value_counts().plot(kind="bar", ax=axes[0], color="#334155")
    axes[0].set_title("Records by record_type")
    axes[0].tick_params(axis="x", rotation=30)

    df[df["record_type"] == "observation"]["pillar"].value_counts().plot(
        kind="bar",
        ax=axes[1],
        color=[
            COLORS.get(p, "#94a3b8")
            for p in df[df["record_type"] == "observation"]["pillar"]
            .value_counts()
            .index
        ],
    )
    axes[1].set_title("Observations by pillar")
    axes[1].tick_params(axis="x", rotation=30)

    df["confidence"].value_counts().reindex(
        ["high", "medium", "low", "estimated"]
    ).dropna().plot(kind="bar", ax=axes[2], color="#0f766e")
    axes[2].set_title("Records by confidence level")
    axes[2].tick_params(axis="x", rotation=30)
    fig.suptitle(
        "Dataset Overview (enriched: 58 main records)", y=1.03, fontweight="bold"
    )
    fig.tight_layout()
    fig.savefig(FIG_DIR / "01_dataset_overview.png", bbox_inches="tight")
    plt.close(fig)


def fig_temporal_coverage(df):
    obs = df[df["record_type"].isin(["observation", "target"])].dropna(subset=["year"])
    pivot = obs.pivot_table(
        index="indicator_code", columns="year", values="value_numeric", aggfunc="count"
    ).fillna(0)
    pivot = pivot.reindex(sorted(pivot.columns), axis=1)
    fig, ax = plt.subplots(figsize=(12, 9))
    im = ax.imshow(pivot.values, cmap="Blues", aspect="auto", vmin=0, vmax=2)
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels([int(c) for c in pivot.columns], rotation=45)
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index, fontsize=8)
    ax.set_title(
        "Temporal Coverage by Indicator (cell = # records that year)", fontweight="bold"
    )
    fig.colorbar(im, ax=ax, shrink=0.6, label="# records")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "02_temporal_coverage.png", bbox_inches="tight")
    plt.close(fig)


def fig_access_trajectory(df):
    acc = df[
        (df["indicator_code"] == "ACC_OWNERSHIP") & (df["gender"] == "all")
    ].sort_values("year")
    target = df[
        (df["indicator_code"] == "ACC_OWNERSHIP") & (df["record_type"] == "target")
    ]

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.plot(
        acc["year"],
        acc["value_numeric"],
        marker="o",
        linewidth=2.5,
        color=COLORS["ACCESS"],
        label="Account Ownership Rate (all adults)",
    )
    for _, r in acc.iterrows():
        ax.annotate(
            f"{r['value_numeric']:.0f}%",
            (r["year"], r["value_numeric"]),
            textcoords="offset points",
            xytext=(0, 10),
            ha="center",
            fontsize=9,
        )
    if len(target):
        ax.scatter(
            target["year"],
            target["value_numeric"],
            color="#dc2626",
            zorder=5,
            s=70,
            marker="*",
            label="NFIS-II 2025 Target",
        )
        ax.annotate(
            f"Target: {target['value_numeric'].values[0]:.0f}%",
            (target["year"].values[0], target["value_numeric"].values[0]),
            textcoords="offset points",
            xytext=(-10, 10),
            ha="right",
            color="#dc2626",
            fontsize=9,
        )

    events = df[df["record_type"] == "event"].sort_values("year")
    for _, e in events.iterrows():
        ax.axvline(
            e["year"] + (e["observation_date"].dayofyear / 365),
            color="grey",
            linestyle=":",
            alpha=0.5,
            linewidth=1,
        )
    ax.set_title(
        "Ethiopia Account Ownership Rate Trajectory (Global Findex, 2014-2024)",
        fontweight="bold",
    )
    ax.set_ylabel("% of adults with an account")
    ax.set_xlabel("Year")
    ax.legend(loc="upper left")
    ax.set_ylim(0, 75)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "03_access_trajectory.png", bbox_inches="tight")
    plt.close(fig)


def fig_growth_rates(df):
    acc = df[
        (df["indicator_code"] == "ACC_OWNERSHIP")
        & (df["gender"] == "all")
        & (df["record_type"] == "observation")
    ].sort_values("year")
    acc = acc.reset_index(drop=True)
    periods, pp_change, ann_rate = [], [], []
    for i in range(1, len(acc)):
        y0, y1 = acc.loc[i - 1, "year"], acc.loc[i, "year"]
        v0, v1 = acc.loc[i - 1, "value_numeric"], acc.loc[i, "value_numeric"]
        periods.append(f"{int(y0)}-{int(y1)}")
        pp_change.append(v1 - v0)
        ann_rate.append((v1 - v0) / (y1 - y0))

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(
        periods, pp_change, color=["#16a34a" if p > 3 else "#dc2626" for p in pp_change]
    )
    for b, r in zip(bars, ann_rate):
        ax.annotate(
            f"{r:.1f} pp/yr",
            (b.get_x() + b.get_width() / 2, b.get_height()),
            textcoords="offset points",
            xytext=(0, 5),
            ha="center",
            fontsize=9,
        )
    ax.set_title(
        "Account Ownership Growth Between Findex Survey Waves", fontweight="bold"
    )
    ax.set_ylabel("Percentage-point change")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "04_growth_rates.png", bbox_inches="tight")
    plt.close(fig)


def fig_gender_gap(df):
    acc21 = df[
        (df["indicator_code"] == "ACC_OWNERSHIP")
        & (df["year"] == 2021)
        & (df["gender"].isin(["male", "female"]))
    ]
    gap = df[df["indicator_code"] == "GEN_GAP_ACC"].sort_values("year")
    gap_usage = df[df["indicator_code"] == "GEN_GAP_USAGE"]
    skill = df[df["indicator_code"] == "GEN_MM_SKILL_GAP"]

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    axes[0].bar(acc21["gender"], acc21["value_numeric"], color=["#2563eb", "#db2777"])
    axes[0].set_title("Account Ownership by Gender (2021)")
    axes[0].set_ylabel("%")
    for i, v in enumerate(acc21["value_numeric"]):
        axes[0].text(i, v + 1, f"{v:.0f}%", ha="center")

    labels = ["Access gap\n(2021)", "Access gap\n(2024)", "Usage gap\n(2025)"]
    values = [
        (
            gap[gap["year"] == 2021]["value_numeric"].values[0]
            if len(gap[gap["year"] == 2021])
            else np.nan
        ),
        (
            gap[gap["year"] == 2024]["value_numeric"].values[0]
            if len(gap[gap["year"] == 2024])
            else np.nan
        ),
        gap_usage["value_numeric"].values[0] if len(gap_usage) else np.nan,
    ]
    axes[1].bar(labels, values, color=["#db2777", "#db2777", "#9333ea"])
    for i, v in enumerate(values):
        axes[1].text(i, v + 0.3, f"{v:.0f}pp", ha="center")
    axes[1].set_title("Gender Gap: Access vs. Usage")
    axes[1].set_ylabel("Percentage points")

    axes[2].bar(skill["gender"], skill["value_numeric"], color=["#db2777", "#2563eb"])
    axes[2].set_title("Adults Lacking Mobile-Money\nDigital Skills (2025)")
    axes[2].set_ylabel("%")
    for i, v in enumerate(skill["value_numeric"]):
        axes[2].text(i, v + 1, f"{v:.0f}%", ha="center")

    fig.suptitle(
        "Gender Dynamics in Ethiopia's Financial Inclusion", fontweight="bold", y=1.04
    )
    fig.tight_layout()
    fig.savefig(FIG_DIR / "05_gender_analysis.png", bbox_inches="tight")
    plt.close(fig)


def fig_usage_trends(df):
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    mm = df[(df["indicator_code"] == "ACC_MM_ACCOUNT")].sort_values("year")
    axes[0].plot(
        mm["year"],
        mm["value_numeric"],
        marker="o",
        color=COLORS["USAGE"],
        linewidth=2.5,
    )
    for _, r in mm.iterrows():
        axes[0].annotate(
            f"{r['value_numeric']:.1f}%",
            (r["year"], r["value_numeric"]),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center",
        )
    axes[0].set_title("Mobile Money Account Ownership Rate")
    axes[0].set_ylabel("% of adults")

    p2p = df[df["indicator_code"] == "USG_P2P_COUNT"].sort_values("year")
    atm = df[df["indicator_code"] == "USG_ATM_COUNT"].sort_values("year")
    axes[1].plot(
        p2p["year"],
        p2p["value_numeric"] / 1e6,
        marker="o",
        label="P2P transactions",
        color="#16a34a",
        linewidth=2.5,
    )
    axes[1].plot(
        atm["year"],
        atm["value_numeric"] / 1e6,
        marker="s",
        label="ATM transactions",
        color="#f59e0b",
        linewidth=2.5,
    )
    axes[1].set_title("P2P vs. ATM Transaction Volume")
    axes[1].set_ylabel("Millions of transactions")
    axes[1].legend()
    fig.tight_layout()
    fig.savefig(FIG_DIR / "06_usage_trends.png", bbox_inches="tight")
    plt.close(fig)


def fig_registered_vs_active(df):
    fig, ax = plt.subplots(figsize=(8, 5.5))
    labels = [
        "Registered\n(sector-wide, 2025)",
        "Active\n(sector-wide, 2025)",
        "M-Pesa self-reported\nactive rate (2024)",
    ]
    total = df[
        (df["indicator_code"] == "USG_MM_ACCOUNTS_TOTAL") & (df["year"] == 2025)
    ]["value_numeric"].values[0]
    active_share = df[df["indicator_code"] == "USG_ACTIVE_ACCOUNT_SHARE"][
        "value_numeric"
    ].values[0]
    mpesa_rate = df[df["indicator_code"] == "USG_ACTIVE_RATE"]["value_numeric"].values[
        0
    ]
    values = [100, active_share, mpesa_rate]
    bars = ax.bar(labels, values, color=["#94a3b8", "#dc2626", "#16a34a"])
    for b, v in zip(bars, values):
        ax.text(
            b.get_x() + b.get_width() / 2,
            v + 1,
            f"{v:.0f}%",
            ha="center",
            fontweight="bold",
        )
    ax.set_ylabel("% (normalized to registered = 100)")
    ax.set_title(
        f"The Registered-vs-Active Gap\n(sector-wide {total/1e6:.0f}M registered mobile money accounts, but only ~15% active)",
        fontweight="bold",
        fontsize=10,
    )
    fig.tight_layout()
    fig.savefig(FIG_DIR / "07_registered_vs_active.png", bbox_inches="tight")
    plt.close(fig)


def fig_infrastructure(df):
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    g4 = df[df["indicator_code"] == "ACC_4G_COV"].sort_values("year")
    axes[0].bar(
        g4["year"].astype(int).astype(str), g4["value_numeric"], color=COLORS["ACCESS"]
    )
    axes[0].set_title("4G Population Coverage")
    axes[0].set_ylabel("%")
    for i, v in enumerate(g4["value_numeric"]):
        axes[0].text(i, v + 1, f"{v:.1f}%", ha="center")

    enablers = df[
        df["indicator_code"].isin(
            ["ACC_ELECTRICITY", "ACC_LITERACY", "ACC_INTERNET_PEN", "ACC_MOBILE_PEN"]
        )
    ]
    enablers = enablers.sort_values("indicator_code")
    axes[1].barh(
        enablers["indicator"].str.replace(" Rate", ""),
        enablers["value_numeric"],
        color="#64748b",
    )
    for i, v in enumerate(enablers["value_numeric"]):
        axes[1].text(v + 1, i, f"{v:.1f}%", va="center")
    axes[1].set_title("Enabling Infrastructure Indicators")
    axes[1].set_xlabel("%")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "08_infrastructure.png", bbox_inches="tight")
    plt.close(fig)


def fig_event_timeline(df):
    events = df[df["record_type"] == "event"].sort_values("observation_date")
    fig, ax = plt.subplots(figsize=(13, 5))
    cat_colors = {
        "product_launch": "#16a34a",
        "market_entry": "#2563eb",
        "infrastructure": "#7c3aed",
        "policy": "#dc2626",
        "milestone": "#f59e0b",
        "partnership": "#0891b2",
        "pricing": "#64748b",
        "regulation": "#db2777",
    }
    y_positions = np.arange(len(events))
    for y, (_, e) in zip(y_positions, events.iterrows()):
        color = cat_colors.get(e["category"], "#334155")
        ax.scatter(e["observation_date"], y, color=color, s=90, zorder=3)
        ax.text(
            e["observation_date"],
            y,
            "  " + e["indicator"][:48] + ("..." if len(e["indicator"]) > 48 else ""),
            va="center",
            fontsize=8.5,
        )
    ax.set_yticks([])
    ax.set_title("Timeline of Cataloged Events (2021-2025)", fontweight="bold")
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    handles = [
        plt.Line2D(
            [0], [0], marker="o", color="w", markerfacecolor=c, markersize=9, label=k
        )
        for k, c in cat_colors.items()
        if k in events["category"].values
    ]
    ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(1.0, 1.0), fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "09_event_timeline.png", bbox_inches="tight")
    plt.close(fig)


def fig_events_overlay(df):
    fig, ax = plt.subplots(figsize=(11, 6))
    telebirr = df[df["indicator_code"] == "USG_TELEBIRR_USERS"].sort_values("year")
    mm = df[df["indicator_code"] == "ACC_MM_ACCOUNT"].sort_values("year")

    ax2 = ax.twinx()
    ax.plot(
        telebirr["year"],
        telebirr["value_numeric"] / 1e6,
        marker="o",
        color="#16a34a",
        linewidth=2.5,
        label="Telebirr registered users (M)",
    )
    ax2.plot(
        mm["year"],
        mm["value_numeric"],
        marker="s",
        color=COLORS["ACCESS"],
        linewidth=2.5,
        label="Mobile Money Account Rate (%, Findex)",
    )

    events = df[df["record_type"] == "event"]
    for _, e in events.iterrows():
        ax.axvline(
            e["observation_date"].year + e["observation_date"].dayofyear / 365,
            color="grey",
            linestyle=":",
            alpha=0.6,
        )
        ax.annotate(
            e["indicator"][:22],
            (
                e["observation_date"].year + e["observation_date"].dayofyear / 365,
                ax.get_ylim()[1] * 0.92,
            ),
            rotation=90,
            fontsize=7,
            color="#475569",
            ha="right",
            va="top",
        )

    ax.set_ylabel("Telebirr users (millions)", color="#16a34a")
    ax2.set_ylabel("Mobile Money Account Rate (%)", color=COLORS["ACCESS"])
    ax.set_title("Events Overlaid on Usage/Access Indicators", fontweight="bold")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "10_events_overlay.png", bbox_inches="tight")
    plt.close(fig)


def fig_correlation(df):
    obs = df[df["record_type"] == "observation"].dropna(
        subset=["year", "value_numeric"]
    )
    pivot = obs.pivot_table(
        index="year", columns="indicator_code", values="value_numeric", aggfunc="mean"
    )
    # Data is a sparse time series (most indicators have 1-2 observed years) -
    # keep indicators with at least 2 non-null years so a directional pairwise
    # read is still possible, and call this limitation out explicitly in the title.
    pivot = pivot.loc[:, pivot.notna().sum() >= 2]
    corr = pivot.corr()
    fig, ax = plt.subplots(figsize=(11, 9))
    im = ax.imshow(corr.values, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=90, fontsize=8)
    ax.set_yticks(range(len(corr.columns)))
    ax.set_yticklabels(corr.columns, fontsize=8)
    fig.colorbar(im, ax=ax, shrink=0.7, label="Pearson correlation (year-aligned)")
    ax.set_title(
        "Correlation Matrix - Indicators with >=3 Years of Data\n(year-level aggregation; small-N, directional read only)",
        fontweight="bold",
        fontsize=10,
    )
    fig.tight_layout()
    fig.savefig(FIG_DIR / "11_correlation_matrix.png", bbox_inches="tight")
    plt.close(fig)
    return corr


def main():
    df, impact = load_data()
    fig_record_overview(df)
    fig_temporal_coverage(df)
    fig_access_trajectory(df)
    fig_growth_rates(df)
    fig_gender_gap(df)
    fig_usage_trends(df)
    fig_registered_vs_active(df)
    fig_infrastructure(df)
    fig_event_timeline(df)
    fig_events_overlay(df)
    corr = fig_correlation(df)
    print("All figures saved to", FIG_DIR)
    print("\nTop correlations with ACC_OWNERSHIP:")
    if "ACC_OWNERSHIP" in corr.columns:
        print(corr["ACC_OWNERSHIP"].sort_values(ascending=False))


if __name__ == "__main__":
    main()
