# Event Impact Modeling

Turns the dataset's 18 `impact_link` records into a quantitative model of how events
move Access/Usage indicators, validates it against real history, and calibrates it.

## Run

```bash
python -c "import sys; sys.path.insert(0,'src'); import impact_model as im; im.load_data()"  # sanity check
jupyter nbconvert --to notebook --execute --inplace notebooks/impact_modeling.ipynb
```

`src/impact_model.py` holds the reusable logic (ramp function, association matrix,
validation); `notebooks/impact_modeling.ipynb` carries the narrative and ships
pre-executed.

## Method

Each event's effect ramps up along a **logistic curve** reaching ~95% of its full size
by `lag_months` after the event (not instant, not a single jump). Multiple events
affecting the same indicator are **summed**. `impact_estimate` is read as percentage
points for rate-type indicators and as % relative change for count-type indicators.
Where `impact_estimate` is missing, a magnitude-band fallback (low=3/medium=8/high=15)
is used.

## The headline finding

The task brief asks directly: does the model's predicted impact match what actually
happened after Telebirr's 2021 launch? **No — badly, and in an informative way:**

| Indicator              | Predicted (raw, literature-based) | Actual (2021→2024) | Calibration factor |
| ---------------------- | --------------------------------- | ------------------ | ------------------ |
| ACC_OWNERSHIP (Access) | +18.8pp                           | +3.0pp             | **×0.16**          |
| ACC_MM_ACCOUNT (Usage) | +10.0pp                           | +4.75pp            | **×0.48**          |

The raw model — built on comparable-country evidence (mostly Kenya's M-Pesa
experience) — overpredicts Access growth ~6x and Usage growth ~2x. This isn't a bug;
it's the quantitative version of Task 2's "2021–2024 slowdown" finding: Kenya's
Access playbook doesn't transfer 1:1 to Ethiopia, which lacked Kenya's electrification
and literacy levels when its own mobile money boom started.

## Outputs

- `reports/association_matrix_raw.csv` / `_calibrated.csv` — event × indicator matrices
- `reports/figures/12–16_*.png` — ramp function, both matrices, both validation charts
- Calibration factors by pillar (Access ×0.16, Usage ×0.48, Gender ×0.5 _unvalidated_,
  Affordability ×1.0) — full reasoning and confidence level for each in the notebook §6
