# Almaty PM2.5 Forecast

Short-term (6/12/24-hour) PM2.5 forecasting for Almaty, Kazakhstan, using gradient-boosted trees trained on the OpenAQ low-cost sensor network and Open-Meteo meteorology.

**Master's thesis** — KBTU programme 7M06106 Software Engineering, 2026.

## Results

| Horizon | Model | RMSE | R² |
|---------|-------|------|----|
| +6 h | XGBoost | 23.44 μg/m³ | 0.545 |
| +12 h | Ridge | 25.85 μg/m³ | 0.446 |
| +24 h | Ridge | 27.24 μg/m³ | 0.383 |
| CAMS (all) | — | — | ≤ −0.18 |

Test set: 2,311 hours, winter 2025–26. CAMS global forecast performs worse than a constant-mean predictor on Almaty data.

## Quick start

```bash
# Install dependencies
uv sync

# Train models (reads data/almaty_aq.db)
PYTHONPATH=. uv run python scripts/train_models.py

# Run the Streamlit app locally
PYTHONPATH=. uv run streamlit run app.py
```

Set `OPENAQ_API_KEY` in `.env` or Streamlit secrets for live data.

## Project structure

```
├── app.py                  # Streamlit web app (single screen)
├── scripts/
│   └── train_models.py     # Train and save models to models/
├── src/
│   ├── config.py           # Coordinates, constants
│   ├── ingest/             # OpenAQ, Open-Meteo, CAMS ingestion
│   ├── features/           # Feature engineering pipeline
│   └── models/             # XGBoost, Ridge, baselines, evaluation
├── models/                 # Saved joblib models + feature_cols.json
├── data/
│   └── almaty_aq.db        # SQLite: 578,993 PM2.5 obs, 190 sensors
├── notebooks/              # EDA and analysis notebooks
└── thesis/                 # LaTeX dissertation source
```

## Data sources

| Source | What | License |
|--------|------|---------|
| [OpenAQ v3](https://openaq.org) | PM2.5 from 192 LCS stations | CC BY 4.0 |
| [Open-Meteo](https://open-meteo.com) | Hourly met + boundary-layer height | CC BY 4.0 |
| [CAMS](https://atmosphere.copernicus.eu) | Global PM2.5 forecast baseline | Copernicus |

Training window: 2024-10-01 to 2026-04-15 (562 days, 11,553 hourly rows after QC).

## Key features

- **Boundary-layer height (BLH)** — primary inversion indicator; explains why Almaty's winter PM2.5 spikes when BLH collapses to < 50 m
- PM2.5 lag features (1, 3, 6, 12, 24 h) and rolling means
- Wind components, temperature gradient, pressure
- Heating-season binary flag (15 Oct – 31 Mar)

## Reproducing results

```bash
# 1. Ingest fresh data (requires OPENAQ_API_KEY)
PYTHONPATH=. uv run python -m src.ingest.openaq
PYTHONPATH=. uv run python -m src.ingest.meteo
PYTHONPATH=. uv run python -m src.ingest.cams_baseline

# 2. Retrain
PYTHONPATH=. uv run python scripts/train_models.py
```

## Citation

```
Alikhan (2026). Development of an intelligent system for investigating and
solving ecological problems. Master's thesis, KBTU, Almaty, Kazakhstan.
```

Data: OpenAQ (CC BY 4.0) · Open-Meteo (CC BY 4.0)
