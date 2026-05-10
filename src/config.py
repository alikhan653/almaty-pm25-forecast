"""Central config: coordinates, parameter IDs, paths, env loading."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

ALMATY_LAT = 43.2389
ALMATY_LON = 76.8897
SEARCH_RADIUS_M = 25_000

OPENAQ_PARAM_IDS = {
    "pm25": 2,
    "pm10": 1,
    "pm1": 19,
    "temperature": 100,
    "relative_humidity": 98,
}

# Expanded data window: Oct 2024 — present. Day-2 decision (2026-04-20):
# OpenAQ has data for only ~1/192 PM2.5 sensors for the original 2023-24 winter
# and 38/192 for 2024-25, because most AirGradient stations came online in 2025.
# We keep the winter focus for error analysis but train over the full window to
# get cross-seasonal variance. See plan.md §7/§8.
DATA_WINDOW_START = "2024-10-01"
DATA_WINDOW_END = "2026-04-15"
DATA_WINDOWS = [(DATA_WINDOW_START, DATA_WINDOW_END)]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
DB_PATH = Path(os.getenv("ALMATY_AQ_DB_PATH", DATA_DIR / "almaty_aq.db"))


def openaq_api_key() -> str:
    key = os.getenv("OPENAQ_API_KEY")
    if not key:
        raise RuntimeError(
            "OPENAQ_API_KEY is not set. Copy .env.example to .env and add your key."
        )
    return key
