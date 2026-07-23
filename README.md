# Forecasting Access and Usage, 2025–2027

Forecasts Account Ownership (Access) and Digital Payment Usage (Usage) using a trend
regression + Task 3's calibrated event-impact model, under three scenarios.

## Run

```bash
jupyter nbconvert --to notebook --execute --inplace notebooks/forecasting.ipynb
```

`src/forecast_model.py` holds the reusable logic (trend fit, event-augmented
adjustment, scenario construction); `notebooks/forecasting.ipynb` carries the
narrative and ships pre-executed.

## Targets

|                    | Indicator        | History           | Note                                                                            |
| ------------------ | ---------------- | ----------------- | ------------------------------------------------------------------------------- |
| Access             | `ACC_OWNERSHIP`  | 5 pts (2011–2024) | 2011 point added for this task                                                  |
| Usage              | `USG_P2P_COUNT`  | 2 pts (2024–2025) | **entire series added for this task** — didn't exist in the dataset before      |
| Usage (supporting) | `ACC_MM_ACCOUNT` | 2 pts             | has direct `impact_link`s, used as a cross-check since the true target has none |

## Method

**Trend:** OLS on year → value, small-sample t-distribution prediction interval (not a
normal approximation) — honest given `dof` is as low as 1 for the 3-point Usage series.
No logistic/saturating curve was fit — an extra curvature parameter would fit noise
with this few points, not signal.

**Event-augmented adjustment:** the _incremental_ calibrated event effect still to land
after the last observation (continued ramp-up of pending events + anything dated after
Nov 2024), added on top of the trend — not the full event effect, to avoid
double-counting what the trend line already reflects.

**Scenarios:**
| | Trend component | Event component |
|---|---|---|
| Pessimistic | lower 95% bound | none |
| Base | point forecast | calibrated (Task 3 factors) |
| Optimistic | upper 95% bound | raw/uncalibrated |

## Results (2027, base scenario)

| Target | 2027 forecast | vs. NFIS-II target                   | Scenario range                                      |
| ------ | ------------- | ------------------------------------ | --------------------------------------------------- |
| Access | ~62%          | Falls short of the 70% (2025) target | ~48–80%                                             |
| Usage  | ~43%          | —                                    | Trend CI alone spans roughly −50% to +140%, clipped |

## The honest headline

**`USG_P2P_COUNT` — the brief's actual Usage target — has zero direct
`impact_link` records in the dataset.** The event-augmented model contributes nothing
to its forecast; only the 3-point trend line is doing any work. This is stated
explicitly in the notebook rather than papered over with the `ACC_MM_ACCOUNT` proxy,
which is carried alongside it precisely because it _does_ have event linkage.

## Key uncertainties

1. No event linkage at all for the primary Usage target.
2. The 2024 Usage anchor (35%) is itself disputed by independent analysis suggesting
   the true figure may be closer to ~21% — see `data_enrichment_log.md`.
3. Small-N trend fits (3–5 points) can't distinguish real deceleration from noise.
4. GENDER/AFFORDABILITY calibration factors feeding this indirectly were never
   independently validated (Task 3).
