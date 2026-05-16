# Analysis Report — Almaty PM2.5 Multi-Horizon Forecasting

**Date:** 2026-05-11  
**Data source:** `data/processed/model_results.csv`  
**Evaluation set:** 2,311 hours, winter 2025–26 (December 2025 – April 2026)  
**Models evaluated:** Persistence, Ridge, CAMS, XGBoost  
**Horizons:** +6 h, +12 h, +24 h  

---

## 1. Analysis Question

Which model best forecasts hourly PM2.5 concentrations in Almaty across three
forecast horizons, and does the best model differ by horizon?

Subsidiary questions:
- (Q1) Does any locally trained model outperform the global CAMS benchmark at all horizons?
- (Q2) Does relative model ranking change with horizon (crossover)?
- (Q3) By how much do local models reduce error relative to CAMS?

---

## 2. Key Findings

### Finding 1 — XGBoost leads at +6 h; Ridge leads at +12 h and +24 h

| Horizon | Best model | RMSE (μg/m³) | R² |
|---------|------------|-------------|-----|
| +6 h    | XGBoost    | 23.44       | 0.545 |
| +12 h   | Ridge      | 25.85       | 0.446 |
| +24 h   | Ridge      | 27.24       | 0.383 |

XGBoost's advantage at +6 h vanishes by +12 h (RMSE rises to 28.67 vs Ridge 25.85).
This crossover is the single most important structural finding: model complexity
must be matched to forecast horizon and effective training-set size.

### Finding 2 — All local models substantially outperform CAMS at all horizons

CAMS achieves negative R² at every horizon (≤ −0.184), meaning it performs worse
than predicting the test-set mean. All three locally trained models — Persistence,
Ridge, and XGBoost — beat CAMS on both RMSE and R².

Largest RMSE improvement over CAMS:
- XGBoost at +6 h: **41.2%** reduction (39.83 → 23.44 μg/m³)
- Ridge at +12 h: **36.5%** reduction (40.73 → 25.85 μg/m³)
- Ridge at +24 h: **27.8%** reduction (37.72 → 27.24 μg/m³)

Even the naïve Persistence baseline beats CAMS at +6 h (RMSE 30.13 vs 39.83).

### Finding 3 — Degradation with horizon is model-specific

| Model       | RMSE +6 h | RMSE +12 h | RMSE +24 h | Δ(6→24) |
|-------------|-----------|------------|------------|---------|
| Persistence | 30.13     | 35.46      | 32.92      | +2.79   |
| Ridge       | 24.37     | 25.85      | 27.24      | +2.87   |
| CAMS        | 39.83     | 40.73      | 37.72      | −2.11   |
| XGBoost     | 23.44     | 28.67      | 31.48      | +8.04   |

XGBoost degrades 8.0 μg/m³ (+34%) from +6 h to +24 h. Ridge degrades only
2.87 μg/m³ (+12%). CAMS actually improves slightly (−2.1 μg/m³) from +6 h to
+24 h, suggesting it is not lag-sensitive but also not useful at any horizon.

### Finding 4 — MAPE is high for all models, reflecting low-concentration dominance

MAPE ranges from 45% (XGBoost +6 h) to 70% (Persistence +12 h). High MAPE values
are consistent with the presence of near-zero PM2.5 hours in the test set (spring
melt); these inflate percentage error disproportionately. RMSE and R² are the
primary evaluation metrics for this reason.

---

## 3. Strongest Supported Comparisons

| Comparison | Evidence | Strength |
|---|---|---|
| XGBoost > Persistence at +6 h | RMSE 23.44 vs 30.13 (22% better) | Strong |
| Ridge > XGBoost at +12 h | RMSE 25.85 vs 28.67 (10% better) | Moderate |
| Ridge > XGBoost at +24 h | RMSE 27.24 vs 31.48 (13% better) | Moderate |
| All local > CAMS (all horizons) | RMSE reduction 27–41%; R² flip from negative to positive | Strong |
| XGBoost degrades faster than Ridge | Δ(6→24) = +8.0 vs +2.9 μg/m³ | Moderate |

---

## 4. Main Caveats

1. **N = 1 run, no repeated seeds.** Inferential statistics (confidence intervals,
   significance tests) cannot be computed. All comparisons are descriptive.
   Effect sizes are reported as relative RMSE reduction (%).

2. **Single evaluation window.** The test set covers one winter (2,311 h). Results
   may not generalise to other winters or non-inversion seasons.

3. **No hyperparameter sensitivity analysis.** XGBoost was tuned with fixed
   hyperparameters; a different configuration might narrow or widen the
   XGBoost–Ridge gap at +12/+24 h.

4. **CAMS comparison is systematic, not paired.** CAMS output is from the global
   Copernicus Atmosphere Monitoring Service; local models were trained on a
   subset of the same test period but CAMS forecasts are independent. This is
   appropriate for a baseline comparison but not for matched-pair inference.

---

## 5. What Changed in Experimental Understanding

Prior assumption: XGBoost (the most complex model) would dominate all horizons.

Observed: Ridge regression outperforms XGBoost at +12 h and +24 h. The
mechanism is consistent with the bias–variance trade-off: the effective training
set for multi-step-ahead predictions is smaller than for +6 h, and the
regularised linear model generalises better under data scarcity. This finding
directly motivates the thesis recommendation that ensemble or model-switching
strategies (XGBoost at +6 h, Ridge at ≥12 h) should be explored in future work.

---

## 6. Figures Produced

| File | Purpose |
|------|---------|
| `figures/figure-01-main-comparison.pdf` | Grouped bar chart: RMSE and R² by model × horizon |
| `figures/figure-02-rmse-profiles.pdf`   | Line chart: RMSE degradation with horizon + crossover zone |
| `figures/figure-03-cams-improvement.pdf`| Bar chart: % RMSE improvement of local models over CAMS |
| `figures/figure-04-metric-heatmap.pdf`  | Heatmap: full RMSE and R² matrix |

See `figure-catalog.md` for detailed interpretation of each figure.
