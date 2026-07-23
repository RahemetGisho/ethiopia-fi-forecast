"""Task 4 - Forecasting Access and Usage, 2025-2027.

Two layers, combined:
1. A trend regression fit on all available Findex waves for the target
   indicator (OLS on year -> value), with a small-sample t-distribution
   prediction interval - this is the "sparse data" case the brief calls out
   (5 points for Access, 3 for Usage).
2. An event-augmented adjustment: the *incremental* calibrated event effect
   (from Task 3's impact model) still to land after the last observed data
   point, added on top of the trend. Only the increment beyond what had
   already accrued by the last observation is added, to avoid double-
   counting effects the trend line already implicitly reflects.

Three scenarios (optimistic / base / pessimistic) combine the trend CI bound
with the event-effect calibration in a documented, consistent way - see
`scenario_forecast()`.
"""

from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import impact_model as im  # noqa: E402

FIG_DIR = ROOT / "reports" / "figures"

plt.rcParams["figure.dpi"] = 110
plt.rcParams["font.size"] = 10
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False


def save_fig(fig, filename: str, fig_dir: Path = FIG_DIR) -> Path:
    fig_dir.mkdir(parents=True, exist_ok=True)
    out = fig_dir / filename
    fig.savefig(out, bbox_inches="tight")
    return out


def get_series(main: pd.DataFrame, indicator_code: str) -> pd.DataFrame:
    df = main[
        (main["indicator_code"] == indicator_code)
        & (main["record_type"] == "observation")
        & (main["gender"] == "all")
    ].copy()
    df["observation_date"] = pd.to_datetime(df["observation_date"])
    df["year_frac"] = (
        df["observation_date"].dt.year
        + (df["observation_date"].dt.dayofyear - 1) / 365.25
    )
    return df.sort_values("year_frac")[
        ["observation_date", "year_frac", "value_numeric", "confidence"]
    ]


# ---------------------------------------------------------------------------
# 1. Trend regression with small-sample prediction interval
# ---------------------------------------------------------------------------
def fit_trend(series: pd.DataFrame):
    x = series["year_frac"].values
    y = series["value_numeric"].values
    n = len(x)
    if n < 2:
        raise ValueError("Need at least 2 points to fit a trend.")
    x_mean = x.mean()
    slope, intercept = np.polyfit(x, y, 1)
    y_hat = slope * x + intercept
    resid = y - y_hat
    dof = max(n - 2, 1)  # guard for n=2 (dof would be 0); widened CI is honest here
    if n > 2:
        s_err = np.sqrt(np.sum(resid**2) / dof)
    else:
        # n=2: no residual d.o.f. - fall back to a conservative fixed relative
        # uncertainty (10% of the observed range) so the interval isn't zero-width.
        s_err = 0.1 * (y.max() - y.min())
    sxx = np.sum((x - x_mean) ** 2)
    r2 = (
        1 - np.sum(resid**2) / np.sum((y - y.mean()) ** 2)
        if np.sum((y - y.mean()) ** 2) > 0
        else np.nan
    )
    return {
        "slope": slope,
        "intercept": intercept,
        "s_err": s_err,
        "sxx": sxx,
        "x_mean": x_mean,
        "n": n,
        "dof": dof,
        "r2": r2,
    }


def predict_trend(trend: dict, x_future: np.ndarray, alpha: float = 0.05):
    slope, intercept = trend["slope"], trend["intercept"]
    point = slope * x_future + intercept
    t_crit = stats.t.ppf(1 - alpha / 2, trend["dof"])
    se_pred = trend["s_err"] * np.sqrt(
        1 + 1 / trend["n"] + (x_future - trend["x_mean"]) ** 2 / trend["sxx"]
    )
    margin = t_crit * se_pred
    return point, point - margin, point + margin


# ---------------------------------------------------------------------------
# 2. Event-augmented incremental adjustment
# ---------------------------------------------------------------------------
def incremental_event_effect(
    main,
    impact_table,
    indicator_code,
    last_obs_date,
    future_dates,
    calibration=1.0,
    evidence_filter=None,
):
    """Effect still to land after `last_obs_date`, i.e. E(future) - E(last_obs),
    where E(t) is the cumulative calibrated effect of ALL catalogued events on
    `indicator_code` at time t. This is added on top of the trend forecast,
    which already implicitly reflects effects realized up to last_obs_date."""
    all_dates = pd.DatetimeIndex([last_obs_date]).append(pd.DatetimeIndex(future_dates))
    cum = im.simulate_indicator(
        main,
        impact_table,
        indicator_code,
        all_dates,
        calibration=calibration,
        evidence_filter=evidence_filter,
    )
    baseline_accrued = cum.iloc[0]
    return (cum.iloc[1:] - baseline_accrued).values


# ---------------------------------------------------------------------------
# 3. Scenarios
# ---------------------------------------------------------------------------
PILLAR_OF = {
    "ACC_OWNERSHIP": "ACCESS",
    "USG_DIGITAL_PAYMENT": "USAGE",
    "ACC_MM_ACCOUNT": "ACCESS",
}

CALIBRATION = {"ACCESS": 0.160, "USAGE": 0.475, "GENDER": 0.5, "AFFORDABILITY": 1.0}


def scenario_forecast(
    main,
    impact_table,
    indicator_code,
    years=(2025, 2026, 2027),
    calibration_factor=None,
):
    series = get_series(main, indicator_code)
    trend = fit_trend(series)
    last_obs_date = series["observation_date"].max()
    future_dates = pd.to_datetime([f"{y}-12-31" for y in years])
    x_future = np.array([d.year + (d.dayofyear - 1) / 365.25 for d in future_dates])

    point, lower, upper = predict_trend(trend, x_future)
    cal = (
        calibration_factor
        if calibration_factor is not None
        else CALIBRATION.get(PILLAR_OF.get(indicator_code, ""), 1.0)
    )

    inc_base = incremental_event_effect(
        main, impact_table, indicator_code, last_obs_date, future_dates, calibration=cal
    )
    inc_raw = incremental_event_effect(
        main, impact_table, indicator_code, last_obs_date, future_dates, calibration=1.0
    )

    last_value = series["value_numeric"].iloc[-1]
    rows = []
    for i, y in enumerate(years):
        base_val = np.clip(point[i] + inc_base[i], last_value * 0.97, 100)
        opt_val = np.clip(upper[i] + inc_raw[i], last_value * 0.97, 100)
        pes_val = np.clip(
            lower[i] + 0.0, last_value * 0.97, 100
        )  # pessimistic: no further event lift
        rows.append(
            {
                "year": y,
                "indicator_code": indicator_code,
                "trend_point": round(float(point[i]), 2),
                "trend_lower_95": round(float(lower[i]), 2),
                "trend_upper_95": round(float(upper[i]), 2),
                "event_effect_calibrated": round(float(inc_base[i]), 2),
                "event_effect_raw": round(float(inc_raw[i]), 2),
                "baseline_trend_only": round(
                    float(np.clip(point[i], last_value * 0.97, 100)), 2
                ),
                "base_scenario": round(float(base_val), 2),
                "optimistic_scenario": round(float(opt_val), 2),
                "pessimistic_scenario": round(float(pes_val), 2),
            }
        )
    return pd.DataFrame(rows), trend, series


def fig_forecast(
    df: pd.DataFrame, series: pd.DataFrame, indicator_code: str, title: str
):
    fig, ax = plt.subplots(figsize=(9.5, 6))
    ax.scatter(
        series["year_frac"],
        series["value_numeric"],
        color="#1e293b",
        s=70,
        zorder=5,
        label="Observed (Findex)",
    )
    ax.plot(
        series["year_frac"],
        series["value_numeric"],
        color="#1e293b",
        alpha=0.3,
        linewidth=1,
    )

    years = df["year"].values
    ax.plot(
        years,
        df["baseline_trend_only"],
        "--",
        color="#64748b",
        linewidth=2,
        label="Baseline (trend only)",
    )
    ax.plot(
        years,
        df["base_scenario"],
        "-",
        color="#2563eb",
        linewidth=2.5,
        marker="o",
        label="Base (trend + calibrated events)",
    )
    ax.plot(
        years,
        df["optimistic_scenario"],
        "-",
        color="#16a34a",
        linewidth=1.5,
        marker="^",
        label="Optimistic",
    )
    ax.plot(
        years,
        df["pessimistic_scenario"],
        "-",
        color="#dc2626",
        linewidth=1.5,
        marker="v",
        label="Pessimistic",
    )
    ax.fill_between(
        years,
        df["pessimistic_scenario"],
        df["optimistic_scenario"],
        color="#93c5fd",
        alpha=0.15,
    )

    last_x, last_y = series["year_frac"].iloc[-1], series["value_numeric"].iloc[-1]
    for scen_col in ["base_scenario"]:
        ax.plot(
            [last_x] + list(years),
            [last_y] + list(df[scen_col]),
            color="#2563eb",
            alpha=0.0,
        )  # keeps axis scaling sane

    ax.axvline(series["year_frac"].iloc[-1], color="grey", linestyle=":", alpha=0.5)
    ax.set_title(title, fontweight="bold")
    ax.set_ylabel("% of adults")
    ax.set_xlabel("Year")
    ax.legend(loc="upper left", fontsize=8.5)
    fig.tight_layout()
    return fig
