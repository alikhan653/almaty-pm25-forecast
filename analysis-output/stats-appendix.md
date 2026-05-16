# Statistical Appendix — Almaty PM2.5 Forecasting

**Date:** 2026-05-11  
**Dataset:** `data/processed/model_results.csv`  

---

## ⚠ Inferential Statistics: BLOCKED

**Reason:** N = 1 experimental run with no repeated seeds or cross-validation folds.  
Each cell in the results table represents a single point estimate, not a distribution.

**Consequence:** No confidence intervals, no significance tests, no p-values can be
reported. All statistics below are **descriptive only**. Effect sizes are reported as
relative differences (% reduction) which are interpretable without repeated runs.

This limitation is documented explicitly per the analysis-skill protocol and is
acknowledged in the thesis Discussion chapter.

---

## 1. Descriptive Statistics — RMSE (μg/m³)

| Model       | +6 h  | +12 h | +24 h | Mean  | Range |
|-------------|-------|-------|-------|-------|-------|
| Persistence | 30.13 | 35.46 | 32.92 | 32.84 | 5.33  |
| Ridge       | 24.37 | 25.85 | 27.24 | 25.82 | 2.87  |
| CAMS        | 39.83 | 40.73 | 37.72 | 39.43 | 3.01  |
| XGBoost     | 23.44 | 28.67 | 31.48 | 27.86 | 8.04  |

**Cross-model spread at +6 h:** 39.83 − 23.44 = **16.39 μg/m³** (70% of best)  
**Cross-model spread at +24 h:** 37.72 − 27.24 = **10.48 μg/m³** (38% of best)  
Spread narrows at longer horizons as all models regress toward similar performance.

---

## 2. Descriptive Statistics — R²

| Model       | +6 h   | +12 h  | +24 h  | Mean   |
|-------------|--------|--------|--------|--------|
| Persistence |  0.248 | −0.043 |  0.098 |  0.101 |
| Ridge       |  0.508 |  0.446 |  0.383 |  0.446 |
| CAMS        | −0.314 | −0.376 | −0.184 | −0.291 |
| XGBoost     |  0.545 |  0.318 |  0.175 |  0.346 |

**Interpretation:** CAMS R² < 0 at all horizons — predicting CAMS output is worse
than predicting the test-set mean PM2.5. All locally trained models achieve R² > 0.

**XGBoost R² decay:** 0.545 → 0.318 → 0.175 (−68% relative over three horizons)  
**Ridge R² decay:** 0.508 → 0.446 → 0.383 (−25% relative over three horizons)

---

## 3. Descriptive Statistics — MAE (μg/m³)

| Model       | +6 h  | +12 h | +24 h | Mean  |
|-------------|-------|-------|-------|-------|
| Persistence | 19.61 | 24.04 | 23.15 | 22.27 |
| Ridge       | 16.68 | 18.20 | 18.88 | 17.92 |
| CAMS        | 28.45 | 28.82 | 27.08 | 28.12 |
| XGBoost     | 16.81 | 20.68 | 23.02 | 20.17 |

MAE patterns mirror RMSE: XGBoost leads at +6 h (16.81 vs Ridge 16.68, near-tie),
Ridge leads at +12 h (18.20 vs 20.68) and +24 h (18.88 vs 23.02).

---

## 4. Descriptive Statistics — MAPE (%)

| Model       | +6 h  | +12 h | +24 h | Mean  |
|-------------|-------|-------|-------|-------|
| Persistence | 55.41 | 70.19 | 69.60 | 65.07 |
| Ridge       | 48.31 | 53.61 | 54.37 | 52.10 |
| CAMS        | 60.26 | 62.62 | 57.84 | 60.24 |
| XGBoost     | 45.16 | 52.80 | 59.87 | 52.61 |

**Caveat:** MAPE is inflated when true values approach zero. Spring PM2.5 clean
episodes (10–20 μg/m³) produce disproportionate percentage errors. MAPE is
reported for completeness but RMSE/R² are the primary evaluation metrics.

---

## 5. Effect Sizes — RMSE Improvement over CAMS (%)

Formula: `(RMSE_CAMS − RMSE_model) / RMSE_CAMS × 100`

| Model       | +6 h   | +12 h  | +24 h  | Mean   |
|-------------|--------|--------|--------|--------|
| Persistence | +24.4% | +12.9% |  +12.7% | +16.7% |
| Ridge       | +38.8% | +36.5% | +27.8%  | +34.4% |
| XGBoost     | +41.2% | +29.6% | +16.5%  | +29.1% |

All local models show positive improvement (CAMS is worse), confirming Q1.
Ridge is the most consistent improver across horizons (narrowest range: 27.8–38.8%).
XGBoost has the largest single improvement (+41.2% at +6 h) but degrades faster.

---

## 6. Horizon Sensitivity — RMSE Degradation (Δ from +6 h to +24 h)

| Model       | RMSE +6 h | RMSE +24 h | Absolute Δ | Relative Δ |
|-------------|-----------|------------|------------|------------|
| Persistence | 30.13     | 32.92      | +2.79      | +9.3%      |
| Ridge       | 24.37     | 27.24      | +2.87      | +11.8%     |
| CAMS        | 39.83     | 37.72      | −2.11      | −5.3%      |
| XGBoost     | 23.44     | 31.48      | +8.04      | +34.3%     |

XGBoost degrades 3× faster than Ridge (34.3% vs 11.8%). This horizon-sensitivity
difference is the empirical basis for the model-crossover finding.

---

## 7. Test Choices (Blocked)

The following tests would apply if repeated runs were available:

| Comparison | Appropriate test | Status |
|---|---|---|
| XGBoost vs Ridge at +6 h | Paired t-test or Wilcoxon (on seed runs) | BLOCKED — N=1 |
| CAMS vs best local (any horizon) | One-sample t-test vs 0 improvement | BLOCKED — N=1 |
| Horizon effect within model | Repeated-measures ANOVA | BLOCKED — N=1 |

**Recommendation for future work:** Re-run with ≥5 random seeds and report
mean ± std. With N≥5, Wilcoxon signed-rank tests would be appropriate given
the small sample size.

---

## 8. Assumptions and Limitations

| Limitation | Impact | Mitigation |
|---|---|---|
| N = 1 run | No inferential statistics possible | Report % effect sizes; flag in Discussion |
| Single winter window (2,311 h) | May not generalise to warmer seasons | Acknowledged in Limitations §4.3 |
| No hyperparameter sweep | Ridge/XGBoost comparison may shift with tuning | Noted as future work |
| CAMS comparison is non-paired | Cannot claim within-sample dominance | Appropriate for benchmark comparison |
| MAPE instability at low PM2.5 | MAPE should not be used for ranking | RMSE/R² used as primary metrics |
