"""Fetch CAMS PM2.5 (and friends) from Open-Meteo air-quality API for baseline comparison.

https://air-quality-api.open-meteo.com/v1/air-quality — no API key required.
The `pm2_5` field corresponds to the CAMS global atmospheric composition model;
we use it as a third baseline (alongside persistence and linear regression).

One HTTP call per window. Idempotent: re-runs overwrite the parquet.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import requests

from src.config import ALMATY_LAT, ALMATY_LON, DATA_WINDOWS, RAW_DIR

CAMS_DIR = RAW_DIR / "cams"
AQ_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

HOURLY_VARS = [
    "pm2_5",
    "pm10",
    "european_aqi",
    "us_aqi",
]


def _window_label(date_from: str, date_to: str) -> str:
    return f"{date_from[:7]}__{date_to[:7]}".replace("-", "")


def _window_file(label: str) -> Path:
    return CAMS_DIR / f"almaty_cams_{label}.parquet"


def fetch_window(
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
        "domains": "cams_global",
    }
    resp = requests.get(AQ_URL, params=params, timeout=timeout_s)
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
    CAMS_DIR.mkdir(parents=True, exist_ok=True)
    saved: list[Path] = []
    for date_from, date_to in windows:
        label = _window_label(date_from, date_to)
        out = _window_file(label)
        if out.exists() and not force:
            print(f"skip {out.name} (exists)")
            saved.append(out)
            continue
        print(f"fetching CAMS {date_from} -> {date_to}")
        df = fetch_window(date_from, date_to)
        df.to_parquet(out, index=False)
        print(f"  saved {len(df)} rows -> {out.name}")
        saved.append(out)
    return saved


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Open-Meteo CAMS PM2.5 pull for Almaty.")
    p.add_argument("--force", action="store_true", help="Refetch even if file exists.")
    return p


def main() -> None:
    args = _build_parser().parse_args()
    run(windows=DATA_WINDOWS, force=args.force)


if __name__ == "__main__":
    main()
