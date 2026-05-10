"""Fetch hourly historical weather for Almaty from Open-Meteo.

Uses the archive API (https://archive-api.open-meteo.com/v1/archive), no API key.
One HTTP call per season. Idempotent: re-runs overwrite season parquet.

BLH (boundary_layer_height) is the critical feature for Almaty winter inversion.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import requests

from src.config import ALMATY_LAT, ALMATY_LON, RAW_DIR, DATA_WINDOWS

METEO_DIR = RAW_DIR / "meteo"
ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"

HOURLY_VARS = [
    "temperature_2m",
    "relative_humidity_2m",
    "pressure_msl",
    "wind_speed_10m",
    "wind_direction_10m",
    "boundary_layer_height",
    "precipitation",
]


def _season_label(date_from: str, date_to: str) -> str:
    return f"{date_from[:7]}__{date_to[:7]}".replace("-", "")


def _season_file(season_label: str) -> Path:
    return METEO_DIR / f"almaty_{season_label}.parquet"


def fetch_season(
    date_from: str,
    date_to: str,
    lat: float = ALMATY_LAT,
    lon: float = ALMATY_LON,
    hourly_vars: list[str] = HOURLY_VARS,
    timeout_s: float = 60.0,
) -> pd.DataFrame:
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": date_from,
        "end_date": date_to,
        "hourly": ",".join(hourly_vars),
        "timezone": "UTC",
    }
    resp = requests.get(ARCHIVE_URL, params=params, timeout=timeout_s)
    resp.raise_for_status()
    payload = resp.json()
    hourly = payload.get("hourly", {})
    if "time" not in hourly:
        return pd.DataFrame()
    df = pd.DataFrame(hourly)
    df = df.rename(columns={"time": "datetime_utc"})
    df["datetime_utc"] = pd.to_datetime(df["datetime_utc"], utc=True)
    df["latitude"] = lat
    df["longitude"] = lon
    return df


def run(
    windows: list[tuple[str, str]] = DATA_WINDOWS,
    force: bool = False,
) -> list[Path]:
    METEO_DIR.mkdir(parents=True, exist_ok=True)
    saved: list[Path] = []
    for date_from, date_to in windows:
        out = _season_file(_season_label(date_from, date_to))
        if out.exists() and not force:
            print(f"skip {out.name} (exists)")
            saved.append(out)
            continue
        print(f"fetching {date_from} -> {date_to}")
        df = fetch_season(date_from, date_to)
        df.to_parquet(out, index=False)
        print(f"  saved {len(df)} rows -> {out.name}")
        saved.append(out)
    return saved


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Open-Meteo archive pull for Almaty.")
    p.add_argument("--force", action="store_true", help="Refetch even if file exists.")
    return p


def main() -> None:
    args = _build_parser().parse_args()
    run(windows=DATA_WINDOWS, force=args.force)


if __name__ == "__main__":
    main()
