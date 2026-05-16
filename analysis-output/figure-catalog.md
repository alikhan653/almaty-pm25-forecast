# Figure Catalog — Almaty PM2.5 Forecasting

**Date:** 2026-05-11  
**Output directory:** `analysis-output/figures/`  
**Format:** PDF (vector) + PNG (200 dpi raster)  
**Palette:** Okabe-Ito colourblind-safe  

---

## Figure 1 — Main Comparison: RMSE and R² by Model and Horizon

**File:** `figure-01-main-comparison.pdf / .png`  
**Type:** Grouped bar chart (2 panels)

**Purpose:** Provide a single overview of model performance across all horizons on
both primary metrics. This is the thesis "headline" figure.

**Plotted variables:**
- Left panel: RMSE (μg/m³) — lower is better
- Right panel: R² — higher is better
- x-axis: forecast horizon (+6 h, +12 h, +24 h)
- Bars grouped by model (4 models, Okabe-Ito colours)

**Error bars:** None (N=1 run; error bars are not applicable)

**Caption requirements:**
> Figure 1. Comparison of four forecasting models on the held-out test set
> (2,311 h, winter 2025–26). Left: RMSE (μg/m³), lower is better. Right: R²,
> higher is better. CAMS exhibits negative R² at all horizons. Colours follow
> the Okabe-Ito colourblind-safe palette.

**What to notice:**
- XGBoost (green) achieves the lowest RMSE at +6 h; Ridge (blue) achieves the
  lowest RMSE at +12 h and +24 h.
- CAMS (pink) shows uniformly the worst RMSE and negative R² at all horizons.
- R² for XGBoost drops sharply from 0.545 (+6 h) to 0.175 (+24 h); Ridge is
  more stable (0.508 → 0.383).

**Interpretation:** The ranking crossover between XGBoost and Ridge is visible
in the left panel as the green bar overtakes the blue bar when moving from +6 h
to +12 h. This directly motivates horizon-specific model selection.

**Caveats:** No error bars due to N=1.

---

## Figure 2 — RMSE Horizon Profiles (Crossover)

**File:** `figure-02-rmse-profiles.pdf / .png`  
**Type:** Line chart

**Purpose:** Show how RMSE evolves with forecast horizon for each model and
highlight the XGBoost→Ridge crossover region. More effective than grouped bars
for showing trajectory.

**Plotted variables:**
- y-axis: RMSE (μg/m³)
- x-axis: forecast horizon (+6 h, +12 h, +24 h)
- One line per model; CAMS shown as dashed to distinguish baseline
- Grey shaded band (9–15 h): crossover zone annotation

**Error bars:** None

**Caption requirements:**
> Figure 2. RMSE as a function of forecast horizon. XGBoost (green solid)
> achieves the lowest RMSE at +6 h but is surpassed by Ridge (blue solid)
> beyond approximately +9 h. The grey band marks the crossover region.
> CAMS (pink dashed) is shown for reference; its RMSE remains the highest at
> all horizons.

**What to notice:**
- XGBoost line has the steepest positive slope (fastest degradation).
- Ridge line is nearly linear and has the shallowest slope (most stable).
- The two lines intersect between +6 h and +12 h — exactly in the crossover zone.
- Persistence (orange) shows non-monotonic behaviour (+6 h: 30.13 → +12 h: 35.46
  → +24 h: 32.92), consistent with autocorrelation structure of PM2.5 series.

**Interpretation:** The crossover is the paper's most actionable finding: a
production system should switch from XGBoost (short horizon) to Ridge (longer
horizon) to minimise RMSE. The flat CAMS trajectory confirms it lacks the
dynamic sensitivity that benefits local models.

**Caveats:** Only 3 horizon points; the crossover zone boundary (9–15 h) is
illustrative, not empirically localised.

---

## Figure 3 — Relative RMSE Improvement over CAMS (%)

**File:** `figure-03-cams-improvement.pdf / .png`  
**Type:** Grouped bar chart

**Purpose:** Quantify the practical value of local calibration over the freely
available CAMS global forecast. Answers Q3 directly.

**Plotted variables:**
- y-axis: RMSE improvement over CAMS (%), positive = better than CAMS
- x-axis: forecast horizon (+6 h, +12 h, +24 h)
- Bars for Persistence, Ridge, XGBoost (CAMS is the zero baseline)

**Error bars:** None

**Caption requirements:**
> Figure 3. Relative RMSE improvement of locally trained models over the CAMS
> global chemistry-transport model at each forecast horizon. Positive values
> indicate better performance than CAMS. All three local models outperform
> CAMS at all horizons, with XGBoost achieving the largest gain at +6 h (41%).

**What to notice:**
- All bars are positive — no local model is worse than CAMS at any horizon.
- XGBoost's advantage over CAMS shrinks from 41.2% at +6 h to 16.5% at +24 h.
- Ridge's advantage is more consistent: 38.8% → 36.5% → 27.8%.
- Even Persistence (naïve lag-1 baseline) beats CAMS at all horizons (13–24%).

**Interpretation:** CAMS provides no useful guidance for Almaty PM2.5 at any
horizon tested. Even a zero-parameter persistence forecast outperforms it,
confirming that local LCS calibration adds substantial value beyond freely
available global chemistry-transport output. This is the core practical
justification for the thesis system.

**Caveats:** Improvement is computed relative to the same test set for all
models; CAMS is not re-tuned to Almaty.

---

## Figure 4 — Full Metric Matrix Heatmap

**File:** `figure-04-metric-heatmap.pdf / .png`  
**Type:** Annotated heatmap (2 panels)

**Purpose:** Provide a compact, scannable summary of all 24 metric values (4 models
× 3 horizons × 2 metrics). Suitable for inclusion in a thesis appendix or
supplementary table.

**Plotted variables:**
- Left panel: RMSE heatmap (YlOrRd — yellow = low, red = high)
- Right panel: R² heatmap (RdYlGn — red = low/negative, green = high)
- Rows: models (consistent order: Persistence, Ridge, CAMS, XGBoost)
- Columns: horizons (+6 h, +12 h, +24 h)
- Cell text: exact numeric values

**Error bars:** Not applicable (heatmap)

**Caption requirements:**
> Figure 4. Full metric matrix for RMSE (μg/m³, left) and R² (right) across
> all models and forecast horizons. Cell values are exact point estimates from
> the held-out test set (2,311 h). Colour intensity indicates performance:
> for RMSE, darker red = worse; for R², darker red = worse (negative values
> indicate performance below the mean predictor).

**What to notice:**
- CAMS row is uniformly the darkest in the RMSE heatmap and the reddest in R².
- Ridge row is uniformly light in RMSE and green in R²: the most consistent model.
- XGBoost shows high contrast — top-left cell (best: RMSE 23.44) to bottom-right
  (worst local: RMSE 31.48), illustrating horizon sensitivity.

**Interpretation:** The heatmap confirms at a glance that Ridge is the safest
choice if a single model must cover all horizons. The R² heatmap makes the
CAMS failure (all negative R²) immediately visible without needing to read numbers.

**Caveats:** Color rendering may differ in greyscale print; numeric cell labels
ensure readability without colour.

---

## Summary Table

| Figure | File prefix | Type | Primary claim illustrated |
|--------|-------------|------|--------------------------|
| 1 | figure-01-main-comparison | Grouped bar | XGBoost best at +6 h; Ridge best at +12/+24 h |
| 2 | figure-02-rmse-profiles   | Line chart  | Crossover between XGBoost and Ridge ~+9–15 h |
| 3 | figure-03-cams-improvement| Grouped bar | All local models beat CAMS (16–41%) |
| 4 | figure-04-metric-heatmap  | Heatmap     | Full metric matrix; CAMS uniformly worst |
