"""Task 3 - Event Impact Modeling.

Turns the dataset's `impact_link` records (event -> indicator, direction,
magnitude, lag) into an actual quantitative model that can predict how an
indicator moves in response to one or more events, then validates that model
against real observed data and calibrates it.

Design mirrors src/eda_analysis.py: `fig_*` functions return a Figure for
inline notebook display; the notebook calls `save_fig` explicitly afterward.
"""

from __future__ import annotations
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from dataclasses import dataclass

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "processed" / "ethiopia_fi_unified_data_enriched.xlsx"
FIG_DIR = ROOT / "reports" / "figures"

plt.rcParams["figure.dpi"] = 110
plt.rcParams["font.size"] = 10
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False


def load_data(path: Path = DATA_PATH):
    xl = pd.ExcelFile(path)
    main = xl.parse("ethiopia_fi_unified_data")
    impact = xl.parse("Impact_sheet")
    main["observation_date"] = pd.to_datetime(main["observation_date"], errors="coerce")
    impact["observation_date"] = pd.to_datetime(
        impact["observation_date"], errors="coerce"
    )
    return main, impact


def save_fig(fig, filename: str, fig_dir: Path = FIG_DIR) -> Path:
    fig_dir.mkdir(parents=True, exist_ok=True)
    out = fig_dir / filename
    fig.savefig(out, bbox_inches="tight")
    return out


def build_impact_table(main: pd.DataFrame, impact: pd.DataFrame) -> pd.DataFrame:
    """Join impact_link records to their parent event's own details
    (name, category, date) via parent_id -> record_id. This is the
    'understand the impact data' join the task instructions ask for."""
    events = main[main["record_type"] == "event"][
        ["record_id", "indicator", "indicator_code", "category", "observation_date"]
    ].rename(
        columns={
            "record_id": "parent_id",
            "indicator": "event_name",
            "indicator_code": "event_code",
            "observation_date": "event_date",
            "category": "event_category",
        }
    )
    table = impact.merge(events, on="parent_id", how="left")
    return table[
        [
            "record_id",
            "parent_id",
            "event_name",
            "event_category",
            "event_date",
            "pillar",
            "related_indicator",
            "relationship_type",
            "impact_direction",
            "impact_magnitude",
            "impact_estimate",
            "lag_months",
            "evidence_basis",
            "comparable_country",
            "confidence",
        ]
    ].sort_values(["event_date", "related_indicator"])


# ---------------------------------------------------------------------------
# Functional form: how an event's effect accrues over time
# ---------------------------------------------------------------------------
# Assumption (documented): effects do NOT land instantly at the event date, nor
# do they appear as a single jump at `lag_months`. They ramp up smoothly along a
# logistic ("S") curve that starts near 0 right after the event and reaches ~95%
# of its full estimated size by `lag_months` after the event - a standard,
# defensible shape for real-world technology/policy adoption (slow start, fast
# middle, saturating tail) and strictly more realistic than either "instant" or
# "linear" ramps for financial-inclusion products (mirrors observed Telebirr /
# M-Pesa user-count growth curves in the raw data).


def logistic_ramp_fraction(
    months_since_event: np.ndarray, lag_months: float
) -> np.ndarray:
    """Fraction (0-1) of an event's full effect realized `months_since_event`
    after the event occurred, reaching ~95% by `lag_months`. Zero before the
    event (negative input)."""
    months_since_event = np.asarray(months_since_event, dtype=float)
    lag_months = max(lag_months, 1e-6)
    k = 2 * np.log(19) / lag_months  # solved so frac(0)=0.05, frac(lag)=0.95
    center = lag_months / 2
    frac = 1 / (1 + np.exp(-k * (months_since_event - center)))
    frac = np.where(months_since_event <= 0, 0.0, frac)
    return frac


MAGNITUDE_FALLBACK_PP = {"low": 3.0, "medium": 8.0, "high": 15.0}


def signed_effect_size(row: pd.Series):
    """The event's full (fully-ramped) effect size, sign-applied.
    Uses impact_estimate where the dataset provides one; otherwise falls back
    to a magnitude-band midpoint (documented assumption, used only for the
    three count-indicator links with no impact_estimate)."""
    if pd.notna(row.get("impact_estimate")):
        size = abs(float(row["impact_estimate"]))
    else:
        size = MAGNITUDE_FALLBACK_PP.get(str(row.get("impact_magnitude")).lower(), 5.0)
    sign = 1.0 if row.get("impact_direction") == "increase" else -1.0
    return sign * size


def indicator_value_kind(main: pd.DataFrame, indicator_code: str) -> str:
    """'pp' for %/rate-type indicators (effect applied additively in
    percentage points) vs 'relative' for count-type indicators (effect
    applied as a % multiplier) - see METHODOLOGY notes in the notebook."""
    vt = main.loc[main["indicator_code"] == indicator_code, "value_type"]
    if len(vt) and vt.iloc[0] in ("percentage", "rate", "gap_pp"):
        return "pp"
    return "relative"


def simulate_indicator(
    main: pd.DataFrame,
    impact_table: pd.DataFrame,
    indicator_code: str,
    date_range: pd.DatetimeIndex,
    calibration: float = 1.0,
    evidence_filter=None,
) -> pd.Series:
    """Sum every event's ramped effect on `indicator_code` over `date_range`.
    `calibration` uniformly scales all summed effects (see calibrate_pillar()).
    `evidence_filter`, if given, restricts to links with evidence_basis in the
    list (e.g. drop 'theoretical' links for a conservative variant).
    """
    links = impact_table[impact_table["related_indicator"] == indicator_code].copy()
    if evidence_filter:
        links = links[links["evidence_basis"].isin(evidence_filter)]
    total = pd.Series(0.0, index=date_range)
    for _, r in links.iterrows():
        months_since = (date_range.year - r["event_date"].year) * 12 + (
            date_range.month - r["event_date"].month
        )
        frac = logistic_ramp_fraction(months_since, r["lag_months"])
        size = signed_effect_size(r)
        if size is None:
            continue
        total += frac * size * calibration
    return total


# ---------------------------------------------------------------------------
# Association matrix
# ---------------------------------------------------------------------------
KEY_INDICATORS = [
    "ACC_OWNERSHIP",
    "ACC_MM_ACCOUNT",
    "ACC_4G_COV",
    "USG_DIGITAL_PAYMENT",
    "USG_P2P_COUNT",
    "USG_TELEBIRR_USERS",
    "USG_MPESA_USERS",
    "USG_MPESA_ACTIVE",
    "GEN_GAP_ACC",
    "GEN_MM_SKILL_GAP",
    "AFF_DATA_INCOME",
]


def association_matrix(
    impact_table: pd.DataFrame, indicators=KEY_INDICATORS
) -> pd.DataFrame:
    """Rows = events, columns = key indicators, values = signed full-effect
    size (impact_estimate with direction applied; NaN where no link exists)."""
    t = impact_table.copy()
    t["signed_estimate"] = t.apply(signed_effect_size, axis=1)
    pivot = t.pivot_table(
        index="event_name",
        columns="related_indicator",
        values="signed_estimate",
        aggfunc="sum",
    )
    pivot = pivot.reindex(columns=[c for c in indicators if c in pivot.columns])
    return pivot


def fig_association_matrix(
    matrix: pd.DataFrame, title: str = "Event -> Indicator Association Matrix"
):
    fig, ax = plt.subplots(figsize=(11, 6.5))
    data = matrix.values.astype(float)
    vmax = np.nanmax(np.abs(data)) if np.isfinite(data).any() else 1
    im = ax.imshow(data, cmap="RdBu_r", vmin=-vmax, vmax=vmax, aspect="auto")
    ax.set_xticks(range(len(matrix.columns)))
    ax.set_xticklabels(matrix.columns, rotation=45, ha="right", fontsize=8)
    ax.set_yticks(range(len(matrix.index)))
    ax.set_yticklabels(matrix.index, fontsize=8)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            v = data[i, j]
            if np.isfinite(v):
                ax.text(
                    j,
                    i,
                    f"{v:+.0f}",
                    ha="center",
                    va="center",
                    fontsize=8,
                    color="white" if abs(v) > vmax * 0.6 else "black",
                )
    ax.set_title(title, fontweight="bold")
    fig.colorbar(
        im,
        ax=ax,
        shrink=0.7,
        label="Estimated effect (pp, or % relative for count indicators)",
    )
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# Validation against historical data
# ---------------------------------------------------------------------------
@dataclass
class ValidationResult:
    indicator_code: str
    window_start: pd.Timestamp
    window_end: pd.Timestamp
    baseline_value: float
    observed_end_value: float
    observed_change: float
    predicted_change_raw: float
    calibration_factor: float

    @property
    def predicted_end_value_raw(self):
        return self.baseline_value + self.predicted_change_raw


def validate_indicator(
    main, impact_table, indicator_code, start: str, end: str, evidence_filter=None
) -> ValidationResult:
    obs = main[
        (main["indicator_code"] == indicator_code)
        & (main["record_type"] == "observation")
        & (main.get("gender", "all") == "all")
    ]
    obs = obs.sort_values("observation_date")
    start_ts, end_ts = pd.Timestamp(start), pd.Timestamp(end)
    baseline_row = obs[obs["observation_date"] <= start_ts].tail(1)
    end_row = obs[obs["observation_date"] <= end_ts].tail(1)
    baseline_value = float(baseline_row["value_numeric"].iloc[0])
    observed_end_value = float(end_row["value_numeric"].iloc[0])
    observed_change = observed_end_value - baseline_value

    date_range = pd.date_range(start_ts, end_ts, freq="MS")
    predicted_series = simulate_indicator(
        main, impact_table, indicator_code, date_range, evidence_filter=evidence_filter
    )
    predicted_change_raw = float(predicted_series.iloc[-1])

    calibration_factor = (
        observed_change / predicted_change_raw
        if predicted_change_raw not in (0, None) and not np.isnan(predicted_change_raw)
        else np.nan
    )
    return ValidationResult(
        indicator_code,
        start_ts,
        end_ts,
        baseline_value,
        observed_end_value,
        observed_change,
        predicted_change_raw,
        calibration_factor,
    )


def fig_validation(
    main, impact_table, indicator_code, start, end, calibration=1.0, label_suffix=""
):
    start_ts, end_ts = pd.Timestamp(start), pd.Timestamp(end)
    date_range = pd.date_range(start_ts, end_ts, freq="MS")
    obs = main[
        (main["indicator_code"] == indicator_code)
        & (main["record_type"] == "observation")
        & (main.get("gender", "all") == "all")
    ].sort_values("observation_date")
    baseline_value = float(
        obs[obs["observation_date"] <= start_ts].tail(1)["value_numeric"].iloc[0]
    )

    raw = (
        simulate_indicator(
            main, impact_table, indicator_code, date_range, calibration=1.0
        )
        + baseline_value
    )
    calibrated = (
        simulate_indicator(
            main, impact_table, indicator_code, date_range, calibration=calibration
        )
        + baseline_value
    )

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.plot(
        date_range,
        raw,
        "--",
        color="#dc2626",
        label="Model prediction (raw, literature-based)",
    )
    ax.plot(
        date_range,
        calibrated,
        "-",
        color="#16a34a",
        linewidth=2.5,
        label=f"Model prediction (Ethiopia-calibrated x{calibration:.2f})",
    )
    window_obs = obs[
        (obs["observation_date"] >= start_ts)
        & (obs["observation_date"] <= end_ts + pd.Timedelta(days=1))
    ]
    ax.scatter(
        window_obs["observation_date"],
        window_obs["value_numeric"],
        color="#1e293b",
        zorder=5,
        s=80,
        label="Actual observed (Findex)",
    )
    for _, r in window_obs.iterrows():
        ax.annotate(
            f"{r['value_numeric']:.1f}",
            (r["observation_date"], r["value_numeric"]),
            textcoords="offset points",
            xytext=(6, 6),
            fontsize=9,
        )
    ax.set_title(f"Model Validation: {indicator_code}{label_suffix}", fontweight="bold")
    ax.set_ylabel("% of adults")
    ax.legend(loc="best", fontsize=8)
    fig.tight_layout()
    return fig


def calibrate_pillar(
    main, impact_table, indicator_code, start, end, evidence_filter=None
) -> float:
    """Derive the multiplicative calibration factor that makes the raw
    literature-based model match observed reality for one indicator; see
    notebook for how pillar-level factors are then applied more broadly."""
    result = validate_indicator(
        main, impact_table, indicator_code, start, end, evidence_filter=evidence_filter
    )
    return result.calibration_factor
