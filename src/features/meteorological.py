"""Meteorological derived features for Almaty PM2.5 forecasting."""

from __future__ import annotations

import numpy as np
import pandas as pd


def add_blh_features(df: pd.DataFrame) -> pd.DataFrame:
    """Log-transform and hour-over-hour delta of boundary layer height.

    BLH is the primary physical proxy for winter inversion events in Almaty.
    Low BLH (<100 m) corresponds to surface-trapped pollution episodes.
    """
    blh = df["boundary_layer_height"].clip(lower=1.0)
    df["blh_log"] = np.log(blh)
    df["blh_delta"] = df["boundary_layer_height"].diff()
    return df


def add_wind_components(df: pd.DataFrame) -> pd.DataFrame:
    """Decompose wind into u (west→east) and v (south→north) components."""
    angle_rad = np.deg2rad(df["wind_direction_10m"])
    df["wind_u"] = -df["wind_speed_10m"] * np.sin(angle_rad)
    df["wind_v"] = -df["wind_speed_10m"] * np.cos(angle_rad)
    return df


def add_temp_gradient(df: pd.DataFrame) -> pd.DataFrame:
    """Hour-over-hour temperature change as a proxy for boundary-layer dynamics."""
    df["temp_gradient"] = df["temperature_2m"].diff()
    return df
