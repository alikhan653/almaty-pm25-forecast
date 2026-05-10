"""Model evaluation: metrics and walk-forward train/test split.

Evaluation strategy
-------------------
Temporal 80/20 split (no random shuffling — shuffling causes data leakage in
time series). The last 20% of hours forms the held-out test set.

Metrics reported: RMSE, MAE, R², MAPE (with ε=5 μg/m³ floor to avoid
division-by-near-zero at low concentration hours).

Models evaluated per horizon (6, 12, 24 h):
  - Persistence (y_t → y_{t+h})
  - Ridge regression (same feature set as XGBoost)
  - CAMS global forecast (external baseline, no training required)
  - XGBoost (primary model)
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from src.features.pipeline import build_feature_matrix
from src.models.baselines import persistence_forecast, train_ridge
from src.models.xgboost_model import HORIZONS, train

# Columns that must not be used as input features
_NON_FEATURES = {"pm25", "cams_pm25"}

TRAIN_RATIO = 0.8
MAPE_EPS = 5.0  # μg/m³; ignore near-zero hours in MAPE calculation


# ---------------------------------------------------------------------------
# Metric helpers
# ---------------------------------------------------------------------------


def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(np.sqrt(mean_squared_error(y_true, y_pred)))


def mape(y_true: np.ndarray, y_pred: np.ndarray, eps: float = MAPE_EPS) -> float:
    mask = y_true > eps
    if mask.sum() == 0:
        return float("nan")
    return float(np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100)


def _metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    return {
        "RMSE": round(rmse(y_true, y_pred), 2),
        "MAE": round(float(mean_absolute_error(y_true, y_pred)), 2),
        "R2": round(float(r2_score(y_true, y_pred)), 4),
        "MAPE": round(mape(y_true, y_pred), 2),
    }


# ---------------------------------------------------------------------------
# Per-horizon evaluation
# ---------------------------------------------------------------------------


def evaluate_horizon(df: pd.DataFrame, horizon: int) -> tuple[dict, object]:
    """Evaluate all models for one forecast horizon.

    Returns (results_dict, trained_xgb_model).
    """
    df = df.copy()
    target = f"pm25_h{horizon}"
    df[target] = df["pm25"].shift(-horizon)
    df = df.dropna(subset=[target])

    split = int(len(df) * TRAIN_RATIO)
    train_df = df.iloc[:split]
    test_df = df.iloc[split:]

    feature_cols = [c for c in df.columns if c not in _NON_FEATURES and not c.startswith("pm25_h")]
    X_train, y_train = train_df[feature_cols], train_df[target]
    X_test, y_test = test_df[feature_cols], test_df[target]
    y_arr = y_test.values

    results: dict[str, dict] = {}

    # Persistence
    y_pers = test_df["pm25"].values
    results["Persistence"] = _metrics(y_arr, y_pers)

    # Ridge regression
    ridge = train_ridge(X_train, y_train)
    results["Linear"] = _metrics(y_arr, ridge.predict(X_test))

    # CAMS external baseline
    y_cams = test_df["cams_pm25"].values
    valid = ~np.isnan(y_cams)
    if valid.sum() > 100:
        results["CAMS"] = _metrics(y_arr[valid], y_cams[valid])
    else:
        results["CAMS"] = {"RMSE": float("nan"), "MAE": float("nan"), "R2": float("nan"), "MAPE": float("nan")}

    # XGBoost
    xgb = train(X_train, y_train)
    y_xgb = xgb.predict(X_test)
    results["XGBoost"] = _metrics(y_arr, y_xgb)

    return results, xgb


# ---------------------------------------------------------------------------
# Full evaluation run
# ---------------------------------------------------------------------------


def run_evaluation(db_path=None) -> pd.DataFrame:
    """Build feature matrix, evaluate all models across all horizons.

    Returns a tidy DataFrame with columns [horizon, model, RMSE, MAE, R2, MAPE].
    """
    kwargs = {"db_path": db_path} if db_path else {}
    print("Building feature matrix...")
    df = build_feature_matrix(**kwargs)
    n_hours = len(df)
    n_features = len(df.columns) - 2  # exclude pm25 + cams_pm25
    print(f"  {n_hours:,} hours  |  {n_features} features")
    print(f"  {df.index.min().date()} → {df.index.max().date()}")

    n_train = int(n_hours * TRAIN_RATIO)
    n_test = n_hours - n_train
    print(f"  Train: {n_train:,} h  |  Test: {n_test:,} h\n")

    rows = []
    for h in HORIZONS:
        print(f"Horizon +{h}h ...")
        res, _ = evaluate_horizon(df, h)
        for model_name, metrics in res.items():
            rows.append({"horizon": h, "model": model_name, **metrics})
        xgb = res["XGBoost"]
        print(f"  XGBoost  RMSE={xgb['RMSE']:.2f}  MAE={xgb['MAE']:.2f}  R²={xgb['R2']:.4f}  MAPE={xgb['MAPE']:.1f}%")

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main() -> None:
    results = run_evaluation()
    print("\n=== Model Comparison ===")
    print(results.to_string(index=False))

    out = "data/processed/model_results.csv"
    results.to_csv(out, index=False)
    print(f"\nSaved → {out}")


if __name__ == "__main__":
    main()
