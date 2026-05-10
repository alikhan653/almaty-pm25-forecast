"""Temporal feature engineering: lags, rolling stats, cyclical encodings."""

from __future__ import annotations

import numpy as np
import pandas as pd

LAG_HOURS = [1, 3, 6, 12, 24]
ROLL_WINDOWS = [3, 6, 24]


def add_lags(df: pd.DataFrame, col: str = "pm25") -> pd.DataFrame:
    for h in LAG_HOURS:
        df[f"{col}_lag{h}"] = df[col].shift(h)
    return df


def add_rolling(df: pd.DataFrame, col: str = "pm25") -> pd.DataFrame:
    # shift(1) ensures no data leakage: rolling window ends at t-1
    base = df[col].shift(1)
    for w in ROLL_WINDOWS:
        df[f"{col}_roll{w}"] = base.rolling(w, min_periods=1).mean()
    return df


def add_cyclical(df: pd.DataFrame) -> pd.DataFrame:
    h = df.index.hour
    dow = df.index.dayofweek
    doy = df.index.dayofyear
    df["hour_sin"] = np.sin(2 * np.pi * h / 24)
    df["hour_cos"] = np.cos(2 * np.pi * h / 24)
    df["dow_sin"] = np.sin(2 * np.pi * dow / 7)
    df["dow_cos"] = np.cos(2 * np.pi * dow / 7)
    df["doy_sin"] = np.sin(2 * np.pi * doy / 365)
    df["doy_cos"] = np.cos(2 * np.pi * doy / 365)
    return df


def add_heating_season(df: pd.DataFrame) -> pd.DataFrame:
    """Binary indicator: 1 during Oct-15 through Mar-31 (Almaty heating season)."""
    m = df.index.month
    d = df.index.day
    in_season = (m > 10) | (m < 4) | ((m == 10) & (d >= 15))
    df["is_heating_season"] = in_season.astype(int)
    return df
