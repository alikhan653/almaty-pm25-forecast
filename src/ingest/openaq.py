"""Fetch OpenAQ station metadata and historical measurements for Almaty.

Two subcommands:
  locations     — snapshot all stations within the search radius.
  measurements  — per-sensor hourly pulls across winter seasons.

Both are idempotent: re-running overwrites metadata, and per-sensor
measurement files are skipped if present unless --force is passed.
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path

import httpx
import pandas as pd
from openaq import OpenAQ
from openaq.shared.exceptions import (
    GatewayTimeoutError,
    HTTPRateLimitError,
    RateLimitError,
    ServerError,
    ServiceUnavailableError,
)

_TRANSIENT = (
    HTTPRateLimitError,
    RateLimitError,
    ServerError,
    ServiceUnavailableError,
    GatewayTimeoutError,
    httpx.ReadTimeout,
    httpx.ConnectTimeout,
    httpx.RemoteProtocolError,
    httpx.ReadError,
)

from src.config import (
    ALMATY_LAT,
    ALMATY_LON,
    DATA_WINDOWS,
    OPENAQ_PARAM_IDS,
    RAW_DIR,
    SEARCH_RADIUS_M,
    openaq_api_key,
)

LOCATIONS_PARQUET = RAW_DIR / "locations.parquet"
SENSORS_PARQUET = RAW_DIR / "sensors.parquet"
MEASUREMENTS_DIR = RAW_DIR / "measurements_pm25"


def _client() -> OpenAQ:
    return OpenAQ(api_key=openaq_api_key())


# ---------------------------------------------------------------------------
# Locations
# ---------------------------------------------------------------------------


def fetch_locations(
    radius_m: int = SEARCH_RADIUS_M,
    lat: float = ALMATY_LAT,
    lon: float = ALMATY_LON,
    parameter_ids: list[int] | None = None,
) -> list:
    client = _client()
    try:
        resp = client.locations.list(
            coordinates=(lat, lon),
            radius=radius_m,
            parameters_id=parameter_ids,
            limit=1000,
        )
    finally:
        client.close()
    return list(resp.results)


def locations_to_frames(locations: list) -> tuple[pd.DataFrame, pd.DataFrame]:
    loc_rows, sensor_rows = [], []
    for loc in locations:
        coords = loc.coordinates
        loc_rows.append(
            {
                "location_id": loc.id,
                "name": loc.name,
                "locality": loc.locality,
                "country": loc.country.name if loc.country else None,
                "country_code": loc.country.code if loc.country else None,
                "provider": loc.provider.name if loc.provider else None,
                "owner": loc.owner.name if loc.owner else None,
                "is_mobile": loc.is_mobile,
                "is_monitor": loc.is_monitor,
                "latitude": coords.latitude if coords else None,
                "longitude": coords.longitude if coords else None,
                "timezone": loc.timezone,
                "datetime_first": loc.datetime_first.utc if loc.datetime_first else None,
                "datetime_last": loc.datetime_last.utc if loc.datetime_last else None,
                "sensor_count": len(loc.sensors or []),
            }
        )
        for sensor in loc.sensors or []:
            param = sensor.parameter
            sensor_rows.append(
                {
                    "sensor_id": sensor.id,
                    "location_id": loc.id,
                    "parameter_id": param.id if param else None,
                    "parameter_name": param.name if param else None,
                    "units": param.units if param else None,
                    "display_name": param.display_name if param else None,
                }
            )
    return pd.DataFrame(loc_rows), pd.DataFrame(sensor_rows)


def save_location_snapshot(locations_df: pd.DataFrame, sensors_df: pd.DataFrame) -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    locations_df.to_parquet(LOCATIONS_PARQUET, index=False)
    sensors_df.to_parquet(SENSORS_PARQUET, index=False)


def run_locations(radius_m: int = SEARCH_RADIUS_M, pm25_only: bool = False) -> tuple[Path, Path]:
    param_ids = [OPENAQ_PARAM_IDS["pm25"]] if pm25_only else None
    locations = fetch_locations(radius_m=radius_m, parameter_ids=param_ids)
    locations_df, sensors_df = locations_to_frames(locations)
    save_location_snapshot(locations_df, sensors_df)
    return LOCATIONS_PARQUET, SENSORS_PARQUET


# ---------------------------------------------------------------------------
# Measurements
# ---------------------------------------------------------------------------


def _season_label(date_from: str, date_to: str) -> str:
    return f"{date_from[:7]}__{date_to[:7]}".replace("-", "")


def _sensor_file(sensor_id: int, season_label: str) -> Path:
    return MEASUREMENTS_DIR / season_label / f"sensor_{sensor_id}.parquet"


def _fetch_sensor_page(
    client: OpenAQ,
    sensor_id: int,
    datetime_from: str,
    datetime_to: str,
    page: int,
    limit: int = 1000,
    max_retries: int = 8,
    base_wait_s: float = 5.0,
):
    """One page of hourly measurements, with retry on rate-limit / transient errors."""
    for attempt in range(max_retries):
        try:
            return client.measurements.list(
                sensors_id=sensor_id,
                data="hours",
                datetime_from=datetime_from,
                datetime_to=datetime_to,
                page=page,
                limit=limit,
            )
        except _TRANSIENT as exc:
            wait = base_wait_s * (2 ** attempt)
            print(
                f"  transient {type(exc).__name__} on sensor {sensor_id} page {page}; "
                f"sleeping {wait:.0f}s (attempt {attempt + 1}/{max_retries})"
            )
            time.sleep(wait)
    raise RuntimeError(f"giving up on sensor {sensor_id} after {max_retries} retries")


def fetch_sensor_measurements(
    sensor_id: int,
    datetime_from: str,
    datetime_to: str,
    client: OpenAQ | None = None,
) -> pd.DataFrame:
    """Paginated hourly pull for one sensor over [datetime_from, datetime_to)."""
    own_client = client is None
    if own_client:
        client = _client()
    rows: list[dict] = []
    try:
        page = 1
        while True:
            resp = _fetch_sensor_page(client, sensor_id, datetime_from, datetime_to, page)
            results = list(resp.results)
            if not results:
                break
            for m in results:
                period = m.period
                dt_utc = None
                if period and period.datetime_from:
                    dt_utc = period.datetime_from.utc
                rows.append(
                    {
                        "sensor_id": sensor_id,
                        "datetime_utc": dt_utc,
                        "value": m.value,
                        "coverage_expected": (m.coverage.expected_count if m.coverage else None),
                        "coverage_observed": (m.coverage.observed_count if m.coverage else None),
                    }
                )
            if len(results) < 1000:
                break
            page += 1
    finally:
        if own_client:
            client.close()
    return pd.DataFrame(rows)


_MEAS_COLUMNS = ["sensor_id", "datetime_utc", "value", "coverage_expected", "coverage_observed"]


def pm25_sensor_ids_with_lifetime() -> pd.DataFrame:
    """Return DataFrame[sensor_id, location_id, datetime_first, datetime_last] for PM2.5 sensors."""
    if not SENSORS_PARQUET.exists() or not LOCATIONS_PARQUET.exists():
        raise RuntimeError("Run 'locations' subcommand first.")
    sensors = pd.read_parquet(SENSORS_PARQUET)
    locs = pd.read_parquet(LOCATIONS_PARQUET)
    pm25 = sensors.loc[sensors["parameter_id"] == OPENAQ_PARAM_IDS["pm25"]].merge(
        locs[["location_id", "datetime_first", "datetime_last"]], on="location_id"
    )
    pm25["first_utc"] = pd.to_datetime(pm25["datetime_first"], utc=True, errors="coerce")
    pm25["last_utc"] = pd.to_datetime(pm25["datetime_last"], utc=True, errors="coerce")
    return pm25.sort_values("sensor_id").reset_index(drop=True)


def run_measurements(
    windows: list[tuple[str, str]] = DATA_WINDOWS,
    force: bool = False,
    limit_sensors: int | None = None,
    sleep_s: float = 0.5,
) -> None:
    lifetime = pm25_sensor_ids_with_lifetime()
    MEASUREMENTS_DIR.mkdir(parents=True, exist_ok=True)
    client = _client()
    try:
        for date_from, date_to in windows:
            win = _season_label(date_from, date_to)
            (MEASUREMENTS_DIR / win).mkdir(parents=True, exist_ok=True)
            start = pd.Timestamp(date_from, tz="UTC")
            end = pd.Timestamp(date_to, tz="UTC")
            overlap = lifetime[
                (lifetime["first_utc"] <= end) & (lifetime["last_utc"] >= start)
            ].copy()
            total_overlap = len(overlap)
            if limit_sensors:
                overlap = overlap.head(limit_sensors)
            sensor_ids = overlap["sensor_id"].astype(int).tolist()
            print(
                f"[{win}] fetching {len(sensor_ids)} of {total_overlap} PM2.5 sensors "
                f"that overlap the window (total PM2.5 sensors: {len(lifetime)})"
            )
            total, skipped, saved, empty = 0, 0, 0, 0
            failed: list[int] = []
            for sid in sensor_ids:
                total += 1
                out = _sensor_file(sid, win)
                if out.exists() and not force:
                    skipped += 1
                    continue
                try:
                    df = fetch_sensor_measurements(sid, date_from, date_to, client=client)
                except Exception as exc:  # noqa: BLE001 — per-sensor isolation
                    print(f"  FAILED sensor {sid}: {type(exc).__name__}: {exc}")
                    failed.append(sid)
                    continue
                if df.empty:
                    pd.DataFrame(columns=_MEAS_COLUMNS).to_parquet(out, index=False)
                    empty += 1
                else:
                    df.to_parquet(out, index=False)
                    saved += 1
                if sleep_s:
                    time.sleep(sleep_s)
                if total % 10 == 0:
                    print(
                        f"  [{win}] {total}/{len(sensor_ids)} "
                        f"saved={saved} empty={empty} skipped={skipped} failed={len(failed)}"
                    )
            print(
                f"[{win}] done: saved={saved} empty={empty} skipped={skipped} "
                f"failed={len(failed)} total_sensors={len(sensor_ids)}"
            )
            if failed:
                print(f"[{win}] failed sensor ids: {failed[:20]}{'...' if len(failed)>20 else ''}")
    finally:
        client.close()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="OpenAQ ingest for Almaty.")
    sub = p.add_subparsers(dest="cmd", required=True)

    loc = sub.add_parser("locations", help="Snapshot station metadata.")
    loc.add_argument("--radius", type=int, default=SEARCH_RADIUS_M)
    loc.add_argument("--pm25-only", action="store_true")

    meas = sub.add_parser("measurements", help="Hourly PM2.5 pulls per sensor.")
    meas.add_argument("--force", action="store_true", help="Refetch existing files.")
    meas.add_argument("--limit-sensors", type=int, default=None)
    meas.add_argument("--sleep", type=float, default=0.5, help="Sleep between sensors (s).")
    return p


def main() -> None:
    args = _build_parser().parse_args()
    if args.cmd == "locations":
        loc_path, sensor_path = run_locations(radius_m=args.radius, pm25_only=args.pm25_only)
        locations_df = pd.read_parquet(loc_path)
        sensors_df = pd.read_parquet(sensor_path)
        print(f"Saved {len(locations_df)} locations -> {loc_path}")
        print(f"Saved {len(sensors_df)} sensors   -> {sensor_path}")
        pm25_id = OPENAQ_PARAM_IDS["pm25"]
        pm25_stations = sensors_df.loc[
            sensors_df["parameter_id"] == pm25_id, "location_id"
        ].nunique()
        print(f"Stations reporting PM2.5: {pm25_stations}")
    elif args.cmd == "measurements":
        run_measurements(
            windows=DATA_WINDOWS,
            force=args.force,
            limit_sensors=args.limit_sensors,
            sleep_s=args.sleep,
        )


if __name__ == "__main__":
    main()
