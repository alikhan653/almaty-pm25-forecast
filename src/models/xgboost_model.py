"""XGBoost forecaster for multi-horizon PM2.5 prediction."""

from __future__ import annotations

import joblib
from pathlib import Path

import pandas as pd
from xgboost import XGBRegressor

HORIZONS = [6, 12, 24]

_DEFAULT_PARAMS: dict = {
    "n_estimators": 600,
    "learning_rate": 0.05,
    "max_depth": 6,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "min_child_weight": 5,
    "reg_alpha": 0.1,
    "reg_lambda": 1.0,
    "random_state": 42,
    "n_jobs": -1,
    "verbosity": 0,
}


def train(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    params: dict | None = None,
) -> XGBRegressor:
    p = {**_DEFAULT_PARAMS, **(params or {})}
    model = XGBRegressor(**p)
    model.fit(X_train, y_train)
    return model


def save(model: XGBRegressor, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)


def load(path: Path) -> XGBRegressor:
    return joblib.load(path)
