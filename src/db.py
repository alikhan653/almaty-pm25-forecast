"""SQLite schema and loader for Almaty AQ data.

Tables
------
locations  — station metadata (from OpenAQ).
sensors    — sensor -> location + parameter.
pm25       — hourly PM2.5 observations (from OpenAQ).
meteo      — hourly Open-Meteo weather for Almaty centre.
cams       — hourly CAMS PM2.5 forecast (Open-Meteo air-quality API).

Loader is idempotent: `load_all(replace=True)` wipes and reloads the tables;
parquet files on disk remain the source of truth.
"""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

import pandas as pd

from src.config import DB_PATH, RAW_DIR

LOCATIONS_PARQUET = RAW_DIR / "locations.parquet"
SENSORS_PARQUET = RAW_DIR / "sensors.parquet"
PM25_DIR = RAW_DIR / "measurements_pm25"
METEO_DIR = RAW_DIR / "meteo"
CAMS_DIR = RAW_DIR / "cams"

SCHEMA = """
CREATE TABLE IF NOT EXISTS locations (
    location_id    INTEGER PRIMARY KEY,
    name           TEXT,
    locality       TEXT,
    country        TEXT,
    country_code   TEXT,
    provider       TEXT,
    owner          TEXT,
    is_mobile      INTEGER,
    is_monitor     INTEGER,
    latitude       REAL,
    longitude      REAL,
    timezone       TEXT,
    datetime_first TEXT,
    datetime_last  TEXT,
    sensor_count   INTEGER
);

CREATE TABLE IF NOT EXISTS sensors (
    sensor_id       INTEGER PRIMARY KEY,
    location_id     INTEGER,
    parameter_id    INTEGER,
    parameter_name  TEXT,
    units           TEXT,
    display_name    TEXT,
    FOREIGN KEY (location_id) REFERENCES locations(location_id)
);
CREATE INDEX IF NOT EXISTS sensors_location_idx ON sensors(location_id);
CREATE INDEX IF NOT EXISTS sensors_parameter_idx ON sensors(parameter_id);

CREATE TABLE IF NOT EXISTS pm25 (
    sensor_id          INTEGER NOT NULL,
    datetime_utc       TEXT NOT NULL,
    value              REAL,
    coverage_expected  INTEGER,
    coverage_observed  INTEGER,
    PRIMARY KEY (sensor_id, datetime_utc)
);
CREATE INDEX IF NOT EXISTS pm25_dt_idx ON pm25(datetime_utc);

CREATE TABLE IF NOT EXISTS meteo (
    datetime_utc            TEXT PRIMARY KEY,
    temperature_2m          REAL,
    relative_humidity_2m    REAL,
    pressure_msl            REAL,
    wind_speed_10m          REAL,
    wind_direction_10m      REAL,
    boundary_layer_height   REAL,
    precipitation           REAL,
    latitude                REAL,
    longitude               REAL
);

CREATE TABLE IF NOT EXISTS cams (
    datetime_utc   TEXT PRIMARY KEY,
    pm2_5          REAL,
    pm10           REAL,
    european_aqi   REAL,
    us_aqi         REAL,
    latitude       REAL,
    longitude      REAL
);
"""


def connect(db_path: Path = DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA)
    conn.commit()


def _load_parquet_table(
    conn: sqlite3.Connection,
    table: str,
    df: pd.DataFrame,
    replace: bool = True,
) -> int:
    if df.empty:
        return 0
    if replace:
        conn.execute(f"DELETE FROM {table}")
    df.to_sql(table, conn, if_exists="append", index=False)
    conn.commit()
    return len(df)


def load_locations(conn: sqlite3.Connection) -> int:
    if not LOCATIONS_PARQUET.exists():
        return 0
    df = pd.read_parquet(LOCATIONS_PARQUET)
    df["is_mobile"] = df["is_mobile"].astype("Int64")
    df["is_monitor"] = df["is_monitor"].astype("Int64")
    return _load_parquet_table(conn, "locations", df)


def load_sensors(conn: sqlite3.Connection) -> int:
    if not SENSORS_PARQUET.exists():
        return 0
    df = pd.read_parquet(SENSORS_PARQUET)
    return _load_parquet_table(conn, "sensors", df)


def _collect_pm25() -> pd.DataFrame:
    if not PM25_DIR.exists():
        return pd.DataFrame()
    frames = []
    for f in sorted(PM25_DIR.rglob("sensor_*.parquet")):
        df = pd.read_parquet(f)
        if not df.empty:
            frames.append(df)
    if not frames:
        return pd.DataFrame()
    df = pd.concat(frames, ignore_index=True)
    df["datetime_utc"] = pd.to_datetime(df["datetime_utc"], utc=True).dt.strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    return df.drop_duplicates(subset=["sensor_id", "datetime_utc"])


def load_pm25(conn: sqlite3.Connection) -> int:
    df = _collect_pm25()
    return _load_parquet_table(conn, "pm25", df)


def _collect_dir(directory: Path) -> pd.DataFrame:
    if not directory.exists():
        return pd.DataFrame()
    frames = [pd.read_parquet(f) for f in sorted(directory.glob("*.parquet"))]
    if not frames:
        return pd.DataFrame()
    df = pd.concat(frames, ignore_index=True)
    df["datetime_utc"] = pd.to_datetime(df["datetime_utc"], utc=True).dt.strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    return df.drop_duplicates(subset=["datetime_utc"])


def load_meteo(conn: sqlite3.Connection) -> int:
    return _load_parquet_table(conn, "meteo", _collect_dir(METEO_DIR))


def load_cams(conn: sqlite3.Connection) -> int:
    return _load_parquet_table(conn, "cams", _collect_dir(CAMS_DIR))


def load_all(db_path: Path = DB_PATH) -> dict[str, int]:
    conn = connect(db_path)
    try:
        init_schema(conn)
        # Disable FK checks during bulk reload so child tables can be wiped
        # before parents without ordering the DELETEs manually.
        conn.execute("PRAGMA foreign_keys = OFF")
        counts = {
            "locations": load_locations(conn),
            "sensors": load_sensors(conn),
            "pm25": load_pm25(conn),
            "meteo": load_meteo(conn),
            "cams": load_cams(conn),
        }
        conn.execute("PRAGMA foreign_keys = ON")
    finally:
        conn.close()
    return counts


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Load parquet snapshots into SQLite.")
    p.add_argument("--db", type=Path, default=DB_PATH)
    return p


def main() -> None:
    args = _build_parser().parse_args()
    counts = load_all(args.db)
    for table, n in counts.items():
        print(f"{table:12s} {n:>10,} rows")
    print(f"db -> {args.db}")


if __name__ == "__main__":
    main()
