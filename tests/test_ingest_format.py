"""Minimal ingest-format tests (plan §10 policy).

Run with: uv run pytest tests/ -q

These tests validate that the local parquet snapshots produced by
`src/ingest/*.py` have the schemas expected by downstream code. They do not
hit the network; bigger end-to-end checks live in notebooks/EDA.
"""

from __future__ import annotations

import pandas as pd
import pytest

from src.config import RAW_DIR
from src.ingest import cams_baseline, meteo, openaq

LOCATIONS_COLUMNS = {
    "location_id", "name", "locality", "country", "country_code", "provider",
    "owner", "is_mobile", "is_monitor", "latitude", "longitude", "timezone",
    "datetime_first", "datetime_last", "sensor_count",
}
SENSORS_COLUMNS = {
    "sensor_id", "location_id", "parameter_id", "parameter_name", "units",
    "display_name",
}
MEASUREMENT_COLUMNS = {
    "sensor_id", "datetime_utc", "value", "coverage_expected", "coverage_observed",
}


def _skip_if_missing(path):
    if not path.exists():
        pytest.skip(f"{path} missing; run ingest first")


def test_locations_schema():
    _skip_if_missing(openaq.LOCATIONS_PARQUET)
    df = pd.read_parquet(openaq.LOCATIONS_PARQUET)
    assert LOCATIONS_COLUMNS.issubset(df.columns)
    assert len(df) > 0
    assert df["country"].eq("Kazakhstan").all()


def test_sensors_has_pm25():
    _skip_if_missing(openaq.SENSORS_PARQUET)
    df = pd.read_parquet(openaq.SENSORS_PARQUET)
    assert SENSORS_COLUMNS.issubset(df.columns)
    assert (df["parameter_id"] == 2).any(), "no PM2.5 sensors found"


def test_pm25_measurement_sample_schema():
    sample = next(openaq.MEASUREMENTS_DIR.rglob("sensor_*.parquet"), None)
    if sample is None:
        pytest.skip("no measurement files yet")
    df = pd.read_parquet(sample)
    if df.empty:
        return
    assert MEASUREMENT_COLUMNS.issubset(df.columns)
    assert df["value"].dtype.kind in "fi"


def test_meteo_has_blh_no_nulls():
    sample = next(meteo.METEO_DIR.glob("*.parquet"), None)
    _skip_if_missing(sample if sample else RAW_DIR / "meteo" / "_missing_")
    df = pd.read_parquet(sample)
    assert "boundary_layer_height" in df.columns
    assert df.isna().sum().sum() == 0, "meteo should be gap-free over the window"


def test_cams_has_pm25():
    sample = next(cams_baseline.CAMS_DIR.glob("*.parquet"), None)
    _skip_if_missing(sample if sample else RAW_DIR / "cams" / "_missing_")
    df = pd.read_parquet(sample)
    assert "pm2_5" in df.columns
    assert df["pm2_5"].notna().any()
