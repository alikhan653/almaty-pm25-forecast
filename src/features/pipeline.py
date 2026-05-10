"""Build the hourly feature matrix for Almaty PM2.5 forecasting.

Pipeline:
1. Load pm25 table, filter outliers, compute city-wide hourly median.
2. Inner-join with meteo; left-join CAMS.
3. Add meteorological derived features (BLH, wind components, temp gradient).
4. Add PM2.5 lag features (1, 3, 6, 12, 24 h).
5. Add PM2.5 rolling means (3, 6, 24 h).
6. Add cyclical time encodings (hour, day-of-week, day-of-year).
7. Add heating-season indicator.
8. Drop rows with any NaN (removes first 24 h and post-gap rows).

Returns a DataFrame indexed by UTC hour; 'pm25' is the target column.
"""

from __future__ import annotations

import sqlite3

import pandas as pd

from src.config import DB_PATH
from src.features.meteorological import (
    add_blh_features,
    add_temp_gradient,
    add_wind_components,
)
from src.features.temporal import (
    add_cyclical,
    add_heating_season,
    add_lags,
    add_rolling,
)

PM25_MIN = 0.0
PM25_MAX = 500.0        # μg/m³ hard cap; values above this are LCS malfunction
MIN_SENSORS = 3         # require ≥ 3 sensors per hour for a stable median

METEO_COLS = [
    "temperature_2m",
    "relative_humidity_2m",
    "pressure_msl",
    "wind_speed_10m",
    "wind_direction_10m",
    "boundary_layer_height",
    "precipitation",
]


def _load_hourly_pm25(conn: sqlite3.Connection) -> pd.Series:
    df = pd.read_sql(
        f"SELECT datetime_utc, value FROM pm25 "
        f"WHERE value >= {PM25_MIN} AND value <= {PM25_MAX}",
        conn,
        parse_dates=["datetime_utc"],
    )
    df["datetime_utc"] = pd.to_datetime(df["datetime_utc"], utc=True).dt.floor("h")
    grouped = df.groupby("datetime_utc")["value"]
    median = grouped.median()
    count = grouped.count()
    return median[count >= MIN_SENSORS].rename("pm25")


def _load_meteo(conn: sqlite3.Connection) -> pd.DataFrame:
    df = pd.read_sql(
        f"SELECT datetime_utc, {', '.join(METEO_COLS)} FROM meteo",
        conn,
        parse_dates=["datetime_utc"],
    )
    df["datetime_utc"] = pd.to_datetime(df["datetime_utc"], utc=True).dt.floor("h")
    return df.set_index("datetime_utc")


def _load_cams(conn: sqlite3.Connection) -> pd.Series:
    df = pd.read_sql(
        "SELECT datetime_utc, pm2_5 FROM cams",
        conn,
        parse_dates=["datetime_utc"],
    )
    df["datetime_utc"] = pd.to_datetime(df["datetime_utc"], utc=True).dt.floor("h")
    return df.set_index("datetime_utc")["pm2_5"].rename("cams_pm25")


def build_feature_matrix(db_path=DB_PATH) -> pd.DataFrame:
    conn = sqlite3.connect(db_path)
    try:
        pm25 = _load_hourly_pm25(conn)
        meteo = _load_meteo(conn)
        cams = _load_cams(conn)
    finally:
        conn.close()

    df = pm25.to_frame().join(meteo, how="inner").join(cams, how="left")
    df = df.sort_index()

    df = add_blh_features(df)
    df = add_wind_components(df)
    df = add_temp_gradient(df)
    df = add_lags(df, col="pm25")
    df = add_rolling(df, col="pm25")
    df = add_cyclical(df)
    df = add_heating_season(df)

    df = df.dropna()
    return df
