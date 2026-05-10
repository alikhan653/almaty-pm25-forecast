"""Persistence and linear regression baselines for PM2.5 forecasting."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge


def persistence_forecast(y: pd.Series, horizon: int) -> pd.Series:
    """Naive persistence: predict y_{t+h} = y_t."""
    return y.copy()


def train_ridge(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    alpha: float = 1.0,
) -> Ridge:
    model = Ridge(alpha=alpha)
    model.fit(X_train, y_train)
    return model
