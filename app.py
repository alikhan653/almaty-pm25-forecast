"""Almaty PM2.5 Forecast — Streamlit web application.

Fetches live data from OpenAQ v3 + Open-Meteo, builds a feature vector,
and serves 6/12/24-hour PM2.5 forecasts from pre-trained models.

Deploy: Streamlit Community Cloud
Secrets: OPENAQ_API_KEY (set in Streamlit Cloud secrets or .streamlit/secrets.toml)
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Ensure project root is on sys.path for `src` imports on Streamlit Cloud
_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st

# ── Config ────────────────────────────────────────────────────────────────────
LAT, LON = 43.2389, 76.8897
SEARCH_RADIUS_M = 25_000
MODELS_DIR = Path(__file__).parent / "models"
REFRESH_SEC = 60

# Kazakhstan AQI breakpoints for PM2.5 (μg/m³)
AQI_LEVELS = [
    (15,  "Good",        "#2ECC71"),
    (35,  "Moderate",    "#F1C40F"),
    (75,  "Unhealthy",   "#E67E22"),
    (150, "Very Unhealthy", "#E74C3C"),
    (float("inf"), "Hazardous", "#8E44AD"),
]


def aqi_color(val: float) -> str:
    for threshold, _, color in AQI_LEVELS:
        if val <= threshold:
            return color
    return "#8E44AD"


def aqi_label(val: float) -> str:
    for threshold, label, _ in AQI_LEVELS:
        if val <= threshold:
            return label
    return "Hazardous"


# ── Model loading ─────────────────────────────────────────────────────────────
@st.cache_resource
def load_models():
    feat_cols = json.loads((MODELS_DIR / "feature_cols.json").read_text())
    models = {
        6:  joblib.load(MODELS_DIR / "xgb_h6.joblib"),
        12: joblib.load(MODELS_DIR / "ridge_h12.joblib"),
        24: joblib.load(MODELS_DIR / "ridge_h24.joblib"),
    }
    return models, feat_cols


# ── Live data fetching ────────────────────────────────────────────────────────
def _openaq_key() -> str | None:
    try:
        return st.secrets["OPENAQ_API_KEY"]
    except Exception:
        import os
        return os.getenv("OPENAQ_API_KEY")


_OPENAQ_BASE = "https://api.openaq.org/v3"


@st.cache_data(ttl=REFRESH_SEC)
def fetch_pm25_history(hours: int = 48) -> pd.DataFrame | None:
    """Fetch recent city-median PM2.5 from OpenAQ v3 REST API."""
    key = _openaq_key()
    if not key:
        st.warning(
            "OPENAQ_API_KEY is not set. "
            "Add it in Streamlit Cloud → App settings → Secrets."
        )
        return None

    headers = {"X-API-Key": key}
    try:
        now = pd.Timestamp.now("UTC")
        date_from = (now - pd.Timedelta(hours=hours)).strftime("%Y-%m-%dT%H:%M:%SZ")
        date_to = now.strftime("%Y-%m-%dT%H:%M:%SZ")

        # 1. Find PM2.5 locations near Almaty, sorted by most recently updated
        r = requests.get(
            f"{_OPENAQ_BASE}/locations",
            headers=headers,
            params={
                "coordinates": f"{LAT},{LON}",
                "radius": SEARCH_RADIUS_M,
                "parameters_id": 2,
                "limit": 200,
            },
            timeout=20,
        )
        r.raise_for_status()
        locations = r.json().get("results", [])

        if not locations:
            st.warning("No OpenAQ sensors found near Almaty.")
            return None

        # Sort locations by datetimeLast descending so active sensors come first
        locations.sort(
            key=lambda loc: (loc.get("datetimeLast") or {}).get("utc") or "2000-01-01",
            reverse=True,
        )

        # Collect sensor IDs (most-recent-first order)
        sensor_ids = []
        for loc in locations:
            for sensor in loc.get("sensors", []):
                param = sensor.get("parameter", {})
                if param.get("id") == 2:
                    sensor_ids.append(sensor["id"])

        if not sensor_ids:
            return None

        # 2. Fetch hourly measurements for up to 30 most-recently-active sensors
        records = []
        for sid in sensor_ids[:30]:
            try:
                mr = requests.get(
                    f"{_OPENAQ_BASE}/sensors/{sid}/hours",
                    headers=headers,
                    params={"datetime_from": date_from, "datetime_to": date_to, "limit": hours},
                    timeout=15,
                )
                if mr.status_code != 200:
                    continue
                for m in mr.json().get("results", []):
                    val = m.get("value")
                    period = m.get("period", {})
                    dt = (period.get("datetimeFrom") or {}).get("utc")
                    if dt and val is not None:
                        records.append({"datetime_utc": dt, "value": val})
            except Exception:
                continue

        if not records:
            return None

        df = pd.DataFrame(records)
        df["datetime_utc"] = pd.to_datetime(df["datetime_utc"], utc=True).dt.floor("h")
        df = df[df["value"].between(0, 500)]
        median = (
            df.groupby("datetime_utc")["value"]
            .agg(["median", "count"])
            .query("count >= 3")["median"]
            .rename("pm25")
            .sort_index()
        )
        return median.to_frame() if not median.empty else None

    except Exception as e:
        st.warning(f"OpenAQ fetch error: {e}")
        return None


@st.cache_data(ttl=REFRESH_SEC)
def fetch_meteo(hours_back: int = 48) -> pd.DataFrame | None:
    """Fetch meteorological data from Open-Meteo (no API key required)."""
    try:
        r = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": LAT,
                "longitude": LON,
                "hourly": ",".join([
                    "temperature_2m",
                    "relative_humidity_2m",
                    "pressure_msl",
                    "wind_speed_10m",
                    "wind_direction_10m",
                    "boundary_layer_height",
                    "precipitation",
                ]),
                "past_days": 2,
                "forecast_days": 2,
                "timezone": "UTC",
                "wind_speed_unit": "ms",
            },
            timeout=15,
        )
        r.raise_for_status()
        data = r.json()["hourly"]
        df = pd.DataFrame(data)
        df["datetime_utc"] = pd.to_datetime(df["time"], utc=True)
        df = df.drop(columns=["time"]).set_index("datetime_utc")
        return df
    except Exception as e:
        st.warning(f"Open-Meteo fetch error: {e}")
        return None


# ── Feature building ──────────────────────────────────────────────────────────
def build_live_features(pm25_df: pd.DataFrame, meteo_df: pd.DataFrame) -> pd.DataFrame:
    """Reproduce the training pipeline feature set on live data."""
    from src.features.meteorological import add_blh_features, add_temp_gradient, add_wind_components
    from src.features.temporal import add_cyclical, add_heating_season, add_lags, add_rolling

    df = pm25_df.join(meteo_df, how="inner").sort_index()
    df = add_blh_features(df)
    df = add_wind_components(df)
    df = add_temp_gradient(df)
    df = add_lags(df, col="pm25")
    df = add_rolling(df, col="pm25")
    df = add_cyclical(df)
    df = add_heating_season(df)
    df = df.dropna()
    return df


# ── Forecast ──────────────────────────────────────────────────────────────────
def make_forecasts(
    feat_df: pd.DataFrame,
    models: dict,
    feat_cols: list[str],
) -> dict[int, float]:
    row = feat_df.iloc[[-1]][feat_cols]
    return {h: float(max(0, model.predict(row)[0])) for h, model in models.items()}


# ── UI ─────────────────────────────────────────────────────────────────────────
def main():
    st.set_page_config(
        page_title="Almaty PM2.5 Forecast",
        page_icon="🌫️",
        layout="wide",
    )

    # Auto-refresh
    try:
        from streamlit_autorefresh import st_autorefresh
        st_autorefresh(interval=REFRESH_SEC * 1000, key="autorefresh")
    except ImportError:
        pass

    st.title("🌫️ Almaty PM2.5 Forecast")
    st.caption(
        f"Real-time air quality forecasts for Almaty, Kazakhstan · "
        f"Updated every {REFRESH_SEC}s · "
        f"Data: OpenAQ LCS network + Open-Meteo"
    )

    # Load models
    try:
        models, feat_cols = load_models()
    except FileNotFoundError:
        st.error(
            "Trained model files not found in `models/`. "
            "Run `uv run python scripts/train_models.py` first."
        )
        st.stop()

    # Fetch data
    with st.spinner("Fetching live data…"):
        pm25_df = fetch_pm25_history(hours=48)
        meteo_df = fetch_meteo(hours_back=48)

    if pm25_df is None or pm25_df.empty:
        st.warning(
            "Could not retrieve live PM2.5 data from OpenAQ. "
            "Check that OPENAQ_API_KEY is set in Streamlit secrets."
        )
        st.stop()

    if meteo_df is None or meteo_df.empty:
        st.warning("Could not retrieve meteorological data from Open-Meteo.")
        st.stop()

    # Build features
    try:
        feat_df = build_live_features(pm25_df, meteo_df)
    except Exception as e:
        st.error(f"Feature building failed: {e}")
        st.stop()

    if feat_df.empty:
        st.warning("Not enough overlapping data to build features. Try again shortly.")
        st.stop()

    # Make forecasts
    forecasts = make_forecasts(feat_df, models, feat_cols)
    current_pm25 = float(pm25_df["pm25"].iloc[-1])
    last_ts = pm25_df.index[-1].astimezone(timezone.utc)

    # ── Current reading row ───────────────────────────────────────────────────
    st.markdown("---")
    col_now, col_6, col_12, col_24 = st.columns(4)

    with col_now:
        color = aqi_color(current_pm25)
        label = aqi_label(current_pm25)
        st.markdown(
            f"<div style='text-align:center'>"
            f"<div style='font-size:0.9rem;color:#888'>Current (observed)</div>"
            f"<div style='font-size:3rem;font-weight:bold;color:{color}'>{current_pm25:.0f}</div>"
            f"<div style='font-size:0.85rem;color:{color}'>{label}</div>"
            f"<div style='font-size:0.75rem;color:#888'>μg/m³ · {last_ts.strftime('%H:%M UTC')}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

    for col, (h, label_prefix, model_name) in zip(
        [col_6, col_12, col_24],
        [(6, "+6 h", "XGBoost"), (12, "+12 h", "Ridge"), (24, "+24 h", "Ridge")],
    ):
        val = forecasts[h]
        color = aqi_color(val)
        label = aqi_label(val)
        delta = val - current_pm25
        delta_str = f"{'▲' if delta >= 0 else '▼'} {abs(delta):.0f}"
        with col:
            st.markdown(
                f"<div style='text-align:center'>"
                f"<div style='font-size:0.9rem;color:#888'>{label_prefix} ({model_name})</div>"
                f"<div style='font-size:3rem;font-weight:bold;color:{color}'>{val:.0f}</div>"
                f"<div style='font-size:0.85rem;color:{color}'>{label}</div>"
                f"<div style='font-size:0.75rem;color:#888'>{delta_str} μg/m³ vs now</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

    # ── Time series chart ────────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("Observed & forecast PM2.5")

    obs = pm25_df["pm25"].last("24h")

    # Forecast points
    fc_times = [
        last_ts + pd.Timedelta(hours=h) for h in [6, 12, 24]
    ]
    fc_vals = [forecasts[h] for h in [6, 12, 24]]

    who_guideline = 15.0
    unhealthy_threshold = 75.0

    fig = go.Figure()

    # Observed
    fig.add_trace(go.Scatter(
        x=obs.index, y=obs.values,
        mode="lines",
        name="Observed",
        line=dict(color="#56B4E9", width=2),
    ))

    # Forecast
    fig.add_trace(go.Scatter(
        x=fc_times, y=fc_vals,
        mode="markers+lines",
        name="Forecast",
        line=dict(color="#E69F00", width=2, dash="dash"),
        marker=dict(size=10, color="#E69F00"),
    ))

    # Connector from last obs to first forecast
    fig.add_trace(go.Scatter(
        x=[last_ts, fc_times[0]],
        y=[current_pm25, fc_vals[0]],
        mode="lines",
        line=dict(color="#E69F00", width=1.5, dash="dot"),
        showlegend=False,
    ))

    # WHO guideline
    fig.add_hline(y=who_guideline, line_dash="dot", line_color="#2ECC71",
                  annotation_text="WHO 24h (15)", annotation_position="bottom right")
    fig.add_hline(y=unhealthy_threshold, line_dash="dot", line_color="#E74C3C",
                  annotation_text="Unhealthy (75)", annotation_position="top right")

    fig.update_layout(
        xaxis_title="Time (UTC)",
        yaxis_title="PM2.5 (μg/m³)",
        yaxis=dict(rangemode="tozero"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=380,
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FAFAFA"),
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Info footer ──────────────────────────────────────────────────────────
    st.markdown("---")
    with st.expander("About this forecast"):
        st.markdown(
            """
**Models:** XGBoost (6-hour horizon), Ridge regression (12- and 24-hour horizons).
Trained on 9,242 hours of OpenAQ LCS data and Open-Meteo meteorology
(October 2024 – April 2026).

**Key features:** boundary-layer height (BLH), PM2.5 lag features (1–24 h),
wind components, temperature gradient, and heating-season indicator.

**Test-set performance (winter 2025–26, 2,311 h):**
| Horizon | Model | RMSE | R² |
|---------|-------|------|-----|
| +6 h | XGBoost | 23.4 μg/m³ | 0.545 |
| +12 h | Ridge | 25.9 μg/m³ | 0.446 |
| +24 h | Ridge | 27.2 μg/m³ | 0.383 |

**Data sources:** [OpenAQ](https://openaq.org) (CC BY 4.0) ·
[Open-Meteo](https://open-meteo.com)

**Source code:** KBTU Master's thesis — *Development of an intelligent system
for investigating and solving ecological problems*, 2026.
            """
        )
    st.caption(
        f"Last updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} · "
        "No authentication required · Free to use"
    )


if __name__ == "__main__":
    main()
