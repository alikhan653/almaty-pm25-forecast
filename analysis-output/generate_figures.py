"""
Generate publication-quality figures for the Almaty PM2.5 model comparison.
Colourblind-safe Okabe-Ito palette. Output: figures/*.pdf + figures/*.png
Run: uv run python analysis-output/generate_figures.py
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from pathlib import Path

# ── Data ─────────────────────────────────────────────────────
DATA = {
    "horizon": [6,6,6,6, 12,12,12,12, 24,24,24,24],
    "model":   ["Persistence","Ridge","CAMS","XGBoost"] * 3,
    "RMSE":    [30.13, 24.37, 39.83, 23.44,
                35.46, 25.85, 40.73, 28.67,
                32.92, 27.24, 37.72, 31.48],
    "MAE":     [19.61, 16.68, 28.45, 16.81,
                24.04, 18.20, 28.82, 20.68,
                23.15, 18.88, 27.08, 23.02],
    "R2":      [0.248,  0.508, -0.314, 0.545,
               -0.043,  0.446, -0.376, 0.318,
                0.098,  0.383, -0.184, 0.175],
    "MAPE":    [55.41, 48.31, 60.26, 45.16,
                70.19, 53.61, 62.62, 52.80,
                69.60, 54.37, 57.84, 59.87],
}
df = pd.DataFrame(DATA)

OUT = Path(__file__).parent / "figures"
OUT.mkdir(exist_ok=True)

# ── Okabe-Ito palette (colourblind-safe) ─────────────────────
COLORS = {
    "Persistence": "#E69F00",  # orange
    "Ridge":       "#56B4E9",  # sky blue
    "CAMS":        "#CC79A7",  # pink
    "XGBoost":     "#009E73",  # green
}
MODELS = ["Persistence", "Ridge", "CAMS", "XGBoost"]
HORIZONS = [6, 12, 24]

plt.rcParams.update({
    "font.family":     "serif",
    "font.size":       11,
    "axes.titlesize":  12,
    "axes.labelsize":  11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.dpi":      150,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

# ═══════════════════════════════════════════════════════════════
# Figure 1 — Main comparison: RMSE and R² by model and horizon
# ═══════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
x = np.arange(len(HORIZONS))
w = 0.18
offsets = np.linspace(-1.5*w, 1.5*w, 4)

for ax, metric, ylabel, invert in [
    (axes[0], "RMSE", "RMSE (μg/m³)", False),
    (axes[1], "R2",   "R²",           False),
]:
    for i, model in enumerate(MODELS):
        vals = [df[(df.model==model) & (df.horizon==h)][metric].values[0]
                for h in HORIZONS]
        bars = ax.bar(x + offsets[i], vals, w,
                      label=model, color=COLORS[model],
                      edgecolor="white", linewidth=0.5)

    ax.set_xticks(x)
    ax.set_xticklabels([f"+{h} h" for h in HORIZONS])
    ax.set_xlabel("Forecast horizon")
    ax.set_ylabel(ylabel)
    ax.axhline(0, color="black", linewidth=0.6, linestyle="--", alpha=0.4)

axes[0].set_title("RMSE — lower is better")
axes[1].set_title("R² — higher is better")

handles = [mpatches.Patch(color=COLORS[m], label=m) for m in MODELS]
fig.legend(handles=handles, loc="lower center", ncol=4,
           bbox_to_anchor=(0.5, -0.02), frameon=False)
fig.suptitle(
    "Figure 1. Model comparison on held-out test set (2,311 h, winter 2025–26)",
    fontsize=11, y=1.01
)
fig.tight_layout()
fig.savefig(OUT / "figure-01-main-comparison.pdf", bbox_inches="tight")
fig.savefig(OUT / "figure-01-main-comparison.png", bbox_inches="tight", dpi=200)
plt.close()
print("✓ figure-01-main-comparison")

# ═══════════════════════════════════════════════════════════════
# Figure 2 — RMSE horizon profiles (line chart, model ranking crossover)
# ═══════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(6, 4.5))
for model in MODELS:
    vals = [df[(df.model==model) & (df.horizon==h)]["RMSE"].values[0]
            for h in HORIZONS]
    ls = "--" if model == "CAMS" else "-"
    ax.plot(HORIZONS, vals, marker="o", label=model,
            color=COLORS[model], linewidth=2, linestyle=ls)

# Annotate the crossover region
ax.axvspan(9, 15, alpha=0.07, color="gray",
           label="XGBoost→Ridge crossover zone")
ax.set_xticks(HORIZONS)
ax.set_xticklabels(["+6 h", "+12 h", "+24 h"])
ax.set_xlabel("Forecast horizon")
ax.set_ylabel("RMSE (μg/m³)")
ax.set_title(
    "Figure 2. RMSE vs. forecast horizon — model ranking crossover\n"
    "(XGBoost leads at +6 h; Ridge leads at +12 h and +24 h)"
)
ax.legend(frameon=False, loc="upper left")
fig.tight_layout()
fig.savefig(OUT / "figure-02-rmse-profiles.pdf", bbox_inches="tight")
fig.savefig(OUT / "figure-02-rmse-profiles.png", bbox_inches="tight", dpi=200)
plt.close()
print("✓ figure-02-rmse-profiles")

# ═══════════════════════════════════════════════════════════════
# Figure 3 — Relative improvement over CAMS (% RMSE reduction)
# ═══════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7, 4))
local_models = ["Persistence", "Ridge", "XGBoost"]
x = np.arange(len(HORIZONS))
w = 0.22
offsets3 = np.linspace(-w, w, 3)

for i, model in enumerate(local_models):
    improvements = []
    for h in HORIZONS:
        cams = df[(df.model=="CAMS") & (df.horizon==h)]["RMSE"].values[0]
        m    = df[(df.model==model) & (df.horizon==h)]["RMSE"].values[0]
        improvements.append((cams - m) / cams * 100)
    ax.bar(x + offsets3[i], improvements, w,
           label=model, color=COLORS[model],
           edgecolor="white", linewidth=0.5)

ax.axhline(0, color="black", linewidth=0.8)
ax.set_xticks(x)
ax.set_xticklabels([f"+{h} h" for h in HORIZONS])
ax.set_xlabel("Forecast horizon")
ax.set_ylabel("RMSE improvement over CAMS (%)")
ax.set_title(
    "Figure 3. Relative RMSE improvement of local models over CAMS\n"
    "(positive = better than CAMS)"
)
ax.legend(frameon=False)
fig.tight_layout()
fig.savefig(OUT / "figure-03-cams-improvement.pdf", bbox_inches="tight")
fig.savefig(OUT / "figure-03-cams-improvement.png", bbox_inches="tight", dpi=200)
plt.close()
print("✓ figure-03-cams-improvement")

# ═══════════════════════════════════════════════════════════════
# Figure 4 — Metric heatmap (all models × all horizons × RMSE/R²)
# ═══════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(10, 3.5))
for ax, metric, fmt, cmap in [
    (axes[0], "RMSE", ".1f", "YlOrRd"),
    (axes[1], "R2",   ".3f", "RdYlGn"),
]:
    pivot = df.pivot(index="model", columns="horizon", values=metric)
    pivot = pivot.loc[MODELS]  # consistent row order

    im = ax.imshow(pivot.values,
                   cmap=cmap,
                   aspect="auto",
                   vmin=pivot.values.min(),
                   vmax=pivot.values.max())
    ax.set_xticks(range(len(HORIZONS)))
    ax.set_xticklabels([f"+{h} h" for h in HORIZONS])
    ax.set_yticks(range(len(MODELS)))
    ax.set_yticklabels(MODELS)
    ax.set_title(f"{metric} heatmap")
    plt.colorbar(im, ax=ax, shrink=0.85)

    for r in range(len(MODELS)):
        for c in range(len(HORIZONS)):
            val = pivot.values[r, c]
            ax.text(c, r, format(val, fmt),
                    ha="center", va="center",
                    fontsize=9,
                    color="white" if (metric=="RMSE" and val > 35) else "black")

fig.suptitle(
    "Figure 4. Full metric matrix — RMSE (μg/m³) and R² across all models and horizons",
    fontsize=11
)
fig.tight_layout()
fig.savefig(OUT / "figure-04-metric-heatmap.pdf", bbox_inches="tight")
fig.savefig(OUT / "figure-04-metric-heatmap.png", bbox_inches="tight", dpi=200)
plt.close()
print("✓ figure-04-metric-heatmap")

print("\nAll figures saved to", OUT)
