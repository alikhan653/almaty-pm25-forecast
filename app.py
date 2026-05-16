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

_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import folium
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st
from folium.plugins import HeatMap
from streamlit_folium import st_folium

# ── Config ────────────────────────────────────────────────────────────────────
LAT, LON = 43.2389, 76.8897
SEARCH_RADIUS_M = 25_000
MODELS_DIR = Path(__file__).parent / "models"
REFRESH_SEC = 60

# Almaty district bounding boxes: (name_en, name_ru, lat_min, lat_max, lon_min, lon_max)
DISTRICTS = [
    ("Bostandyk",  "Бостандыкский", 43.12, 43.25, 76.85, 76.98),
    ("Medeu",      "Медеуский",     43.18, 43.30, 76.98, 77.15),
    ("Almaly",     "Алмалинский",   43.24, 43.31, 76.86, 76.98),
    ("Auezel",     "Ауэзовский",    43.20, 43.28, 76.74, 76.87),
    ("Nauryzbay",  "Наурызбайский", 43.25, 43.36, 76.64, 76.82),
    ("Zhetysu",    "Жетысуский",    43.28, 43.37, 76.96, 77.12),
    ("Turksib",    "Турксибский",   43.32, 43.45, 77.05, 77.25),
    ("Alatau",     "Алатауский",    43.32, 43.48, 76.80, 77.05),
]

AQI_LEVELS = [
    (15,          "Good",           "#2ECC71"),
    (35,          "Moderate",       "#F1C40F"),
    (75,          "Unhealthy",      "#E67E22"),
    (150,         "Very Unhealthy", "#E74C3C"),
    (float("inf"), "Hazardous",     "#8E44AD"),
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


def district_for(lat: float, lon: float) -> str:
    for name_en, _, lat_min, lat_max, lon_min, lon_max in DISTRICTS:
        if lat_min <= lat <= lat_max and lon_min <= lon <= lon_max:
            return name_en
    return "Other"


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
    """Fetch city-median hourly PM2.5 from OpenAQ v3."""
    key = _openaq_key()
    if not key:
        st.warning("OPENAQ_API_KEY is not set. Add it in Streamlit Cloud → App settings → Secrets.")
        return None

    headers = {"X-API-Key": key}
    try:
        now = pd.Timestamp.now("UTC")
        date_from = (now - pd.Timedelta(hours=hours)).strftime("%Y-%m-%dT%H:%M:%SZ")
        date_to   = now.strftime("%Y-%m-%dT%H:%M:%SZ")

        r = requests.get(
            f"{_OPENAQ_BASE}/locations",
            headers=headers,
            params={"coordinates": f"{LAT},{LON}", "radius": SEARCH_RADIUS_M,
                    "parameters_id": 2, "limit": 200},
            timeout=20,
        )
        r.raise_for_status()
        locations = r.json().get("results", [])
        if not locations:
            return None

        locations.sort(
            key=lambda l: (l.get("datetimeLast") or {}).get("utc") or "2000-01-01",
            reverse=True,
        )

        sensor_ids = []
        for loc in locations:
            for s in loc.get("sensors", []):
                if (s.get("parameter") or {}).get("id") == 2:
                    sensor_ids.append(s["id"])

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
                    dt  = (m.get("period", {}).get("datetimeFrom") or {}).get("utc")
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


@st.cache_data(ttl=REFRESH_SEC * 5)
def fetch_stations_current() -> pd.DataFrame:
    """Return per-station current PM2.5 with lat/lon for the map and districts table."""
    key = _openaq_key()
    if not key:
        return pd.DataFrame()

    headers = {"X-API-Key": key}
    try:
        r = requests.get(
            f"{_OPENAQ_BASE}/locations",
            headers=headers,
            params={"coordinates": f"{LAT},{LON}", "radius": SEARCH_RADIUS_M,
                    "parameters_id": 2, "limit": 200},
            timeout=20,
        )
        r.raise_for_status()
        locations = r.json().get("results", [])
    except Exception:
        return pd.DataFrame()

    now = pd.Timestamp.now("UTC")
    cutoff = now - pd.Timedelta(hours=3)

    rows = []
    for loc in locations:
        coords = loc.get("coordinates") or {}
        lat = coords.get("latitude")
        lon = coords.get("longitude")
        if lat is None or lon is None:
            continue

        name = loc.get("name") or loc.get("locality") or "Unknown"

        for s in loc.get("sensors", []):
            if (s.get("parameter") or {}).get("id") != 2:
                continue
            sid = s.get("id")
            if not sid:
                continue

            last_dt_str = (loc.get("datetimeLast") or {}).get("utc")
            if last_dt_str:
                last_dt = pd.to_datetime(last_dt_str, utc=True)
                if last_dt < cutoff:
                    continue  # sensor not recently active

            # Fetch last 3 hours for this sensor
            try:
                mr = requests.get(
                    f"{_OPENAQ_BASE}/sensors/{sid}/hours",
                    headers=headers,
                    params={
                        "datetime_from": cutoff.strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "datetime_to":   now.strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "limit": 3,
                    },
                    timeout=10,
                )
                if mr.status_code != 200:
                    continue
                vals = [m["value"] for m in mr.json().get("results", [])
                        if m.get("value") is not None and 0 <= m["value"] <= 500]
                if not vals:
                    continue
                rows.append({"name": name, "lat": lat, "lon": lon,
                             "pm25": float(np.median(vals)),
                             "district": district_for(lat, lon)})
            except Exception:
                continue

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows)
    # One representative reading per station name
    df = df.groupby("name", as_index=False).agg(
        {"lat": "first", "lon": "first", "pm25": "median", "district": "first"}
    )
    return df.sort_values("pm25", ascending=False).reset_index(drop=True)


OTHER_CITIES = [
    ("Bishkek",  "Kyrgyzstan",   42.8700, 74.5900),
    ("Tashkent", "Uzbekistan",   41.2995, 69.2401),
    ("Astana",   "Kazakhstan",   51.1801, 71.4460),
]


@st.cache_data(ttl=300)
def fetch_city_stations(lat: float, lon: float) -> pd.DataFrame:
    """Fetch station locations for any city.

    Strategy: one fast /locations call returns all station lat/lon.
    Then fetch PM2.5 values from the 10 most-recently-active sensors only.
    All stations appear on the map; only the sample gets PM2.5 colours.
    """
    key = _openaq_key()
    if not key:
        return pd.DataFrame()

    headers = {"X-API-Key": key}
    try:
        r = requests.get(
            f"{_OPENAQ_BASE}/locations",
            headers=headers,
            params={"coordinates": f"{lat},{lon}", "radius": 25000,
                    "parameters_id": 2, "limit": 200},
            timeout=20,
        )
        r.raise_for_status()
        locations = r.json().get("results", [])
    except Exception:
        return pd.DataFrame()

    if not locations:
        return pd.DataFrame()

    now = pd.Timestamp.now("UTC")
    data_from = (now - pd.Timedelta(hours=48)).strftime("%Y-%m-%dT%H:%M:%SZ")
    data_to   = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Sort most-recently-active first
    locations.sort(
        key=lambda l: (l.get("datetimeLast") or {}).get("utc") or "2000-01-01",
        reverse=True,
    )

    # Step 1: collect ALL station rows with pm25=None (fast, no extra API calls)
    rows = []
    sensor_sample = []  # (sid, name) for the top-10 active sensors

    for loc in locations:
        coords = loc.get("coordinates") or {}
        slat   = coords.get("latitude")
        slon   = coords.get("longitude")
        if slat is None or slon is None:
            continue
        name = loc.get("name") or loc.get("locality") or "Unknown"
        rows.append({"name": name, "lat": slat, "lon": slon, "pm25": None})

        if len(sensor_sample) < 10:
            for s in (loc.get("sensors") or []):
                if isinstance(s, dict) and (s.get("parameter") or {}).get("id") == 2:
                    sensor_sample.append((s["id"], name, slat, slon))
                    break

    # Step 2: fetch PM2.5 for the sample of 10 sensors
    pm25_by_name: dict[str, list[float]] = {}
    for sid, sname, _, _ in sensor_sample:
        try:
            mr = requests.get(
                f"{_OPENAQ_BASE}/sensors/{sid}/hours",
                headers=headers,
                params={"datetime_from": data_from, "datetime_to": data_to, "limit": 6},
                timeout=8,
            )
            if mr.status_code != 200:
                continue
            vals = [m["value"] for m in mr.json().get("results", [])
                    if isinstance(m, dict) and m.get("value") is not None
                    and 0 <= m["value"] <= 500]
            if vals:
                pm25_by_name.setdefault(sname, []).extend(vals)
        except Exception:
            continue

    # Step 3: patch PM2.5 values into the rows that we sampled
    for row in rows:
        if row["name"] in pm25_by_name:
            row["pm25"] = float(np.median(pm25_by_name[row["name"]]))

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows)
    df = df.groupby("name", as_index=False).agg(
        {"lat": "first", "lon": "first", "pm25": "median"}
    )
    return df.sort_values("pm25", ascending=False, na_position="last").reset_index(drop=True)


@st.cache_data(ttl=REFRESH_SEC)
def fetch_meteo(hours_back: int = 48) -> pd.DataFrame | None:
    """Fetch meteorological data from Open-Meteo (no API key required)."""
    try:
        r = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": LAT, "longitude": LON,
                "hourly": ",".join([
                    "temperature_2m", "relative_humidity_2m", "pressure_msl",
                    "wind_speed_10m", "wind_direction_10m",
                    "boundary_layer_height", "precipitation",
                ]),
                "past_days": max(2, hours_back // 24 + 1),
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
        return df.drop(columns=["time"]).set_index("datetime_utc")
    except Exception as e:
        st.warning(f"Open-Meteo fetch error: {e}")
        return None


# ── Feature building ──────────────────────────────────────────────────────────
def build_live_features(pm25_df: pd.DataFrame, meteo_df: pd.DataFrame) -> pd.DataFrame:
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
    return df.dropna()


def make_forecasts(feat_df, models, feat_cols) -> dict[int, float]:
    row = feat_df.iloc[[-1]][feat_cols]
    return {h: float(max(0, m.predict(row)[0])) for h, m in models.items()}


# ── Map builder ───────────────────────────────────────────────────────────────
def build_map(stations_df: pd.DataFrame, current_pm25: float) -> folium.Map:
    m = folium.Map(location=[LAT, LON], zoom_start=11,
                   tiles="CartoDB dark_matter")

    if not stations_df.empty:
        # Heatmap layer
        heat_data = [[row.lat, row.lon, row.pm25]
                     for row in stations_df.itertuples() if row.pm25 > 0]
        if heat_data:
            HeatMap(heat_data, radius=20, blur=30, min_opacity=0.3,
                    gradient={0.0: "#2ECC71", 0.33: "#F1C40F",
                              0.66: "#E74C3C", 1.0: "#8E44AD"}).add_to(m)

        # Station markers
        for row in stations_df.itertuples():
            color = aqi_color(row.pm25)
            label = aqi_label(row.pm25)
            folium.CircleMarker(
                location=[row.lat, row.lon],
                radius=7,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.85,
                popup=folium.Popup(
                    f"<b>{row.name}</b><br>"
                    f"PM2.5: {row.pm25:.0f} μg/m³<br>"
                    f"Status: {label}<br>"
                    f"District: {row.district}",
                    max_width=200,
                ),
                tooltip=f"{row.name}: {row.pm25:.0f} μg/m³",
            ).add_to(m)
    else:
        # No per-station data - show city centre with current reading
        color = aqi_color(current_pm25)
        folium.CircleMarker(
            location=[LAT, LON], radius=18,
            color=color, fill=True, fill_color=color, fill_opacity=0.6,
            popup=f"Almaty median: {current_pm25:.0f} μg/m³",
            tooltip=f"Almaty: {current_pm25:.0f} μg/m³",
        ).add_to(m)

    return m


# ── Districts table ───────────────────────────────────────────────────────────
def build_districts_table(
    stations_df: pd.DataFrame, forecasts: dict[int, float], current_pm25: float
) -> pd.DataFrame:
    if stations_df.empty:
        rows = []
        for name_en, name_ru, *_ in DISTRICTS:
            fc6  = forecasts[6]
            diff = fc6 - current_pm25
            arrow = "↑" if diff > 2 else ("↓" if diff < -2 else "→")
            rows.append({
                "District": name_en,
                "Current (μg/m³)": f"{current_pm25:.0f}",
                "AQI": aqi_label(current_pm25),
                f"+6h forecast": f"{arrow} {fc6:.0f}",
            })
        return pd.DataFrame(rows)

    district_stats = (
        stations_df.groupby("district")["pm25"]
        .median()
        .reset_index()
        .rename(columns={"pm25": "current_pm25"})
    )

    rows = []
    for _, drow in district_stats.iterrows():
        curr = drow["current_pm25"]
        # Apply same city-level forecast ratio to per-district current
        ratio6  = forecasts[6]  / current_pm25 if current_pm25 > 0 else 1.0
        ratio12 = forecasts[12] / current_pm25 if current_pm25 > 0 else 1.0
        fc6  = max(0.0, curr * ratio6)
        fc12 = max(0.0, curr * ratio12)
        diff6 = fc6 - curr
        arrow6 = "↑" if diff6 > 2 else ("↓" if diff6 < -2 else "→")
        n_stations = len(stations_df[stations_df["district"] == drow["district"]])
        rows.append({
            "District":        drow["district"],
            "Stations":        n_stations,
            "Now (μg/m³)":     f"{curr:.0f}",
            "AQI":             aqi_label(curr),
            "+6h":             f"{arrow6} {fc6:.0f}",
            "+12h":            f"{fc12:.0f}",
        })

    return pd.DataFrame(rows).sort_values("Now (μg/m³)", ascending=False).reset_index(drop=True)


# ── UI ─────────────────────────────────────────────────────────────────────────
def main():
    st.set_page_config(
        page_title="Almaty PM2.5 Forecast",
        page_icon="🌫️",
        layout="wide",
    )

    try:
        from streamlit_autorefresh import st_autorefresh
        st_autorefresh(interval=REFRESH_SEC * 1000, key="autorefresh")
    except ImportError:
        pass

    st.title("🌫️ Almaty PM2.5 Forecast")
    st.caption(
        f"Real-time air quality forecasts · Almaty, Kazakhstan · "
        f"Auto-refreshes every {REFRESH_SEC}s · "
        "Data: OpenAQ LCS network + Open-Meteo"
    )

    # Load models
    try:
        models, feat_cols = load_models()
    except FileNotFoundError:
        st.error("Trained model files not found in `models/`. Run `uv run python scripts/train_models.py` first.")
        st.stop()

    # Fetch data
    with st.spinner("Fetching live data…"):
        pm25_df   = fetch_pm25_history(hours=48)
        meteo_df  = fetch_meteo(hours_back=48)

    if pm25_df is None or pm25_df.empty:
        st.warning("Could not retrieve live PM2.5 data from OpenAQ. Check that OPENAQ_API_KEY is set.")
        st.stop()
    if meteo_df is None or meteo_df.empty:
        st.warning("Could not retrieve meteorological data from Open-Meteo.")
        st.stop()

    try:
        feat_df = build_live_features(pm25_df, meteo_df)
    except Exception as e:
        st.error(f"Feature building failed: {e}")
        st.stop()

    if feat_df.empty:
        st.warning("Not enough overlapping data to build features. Try again shortly.")
        st.stop()

    forecasts      = make_forecasts(feat_df, models, feat_cols)
    current_pm25   = float(pm25_df["pm25"].iloc[-1])
    last_ts        = pm25_df.index[-1].astimezone(timezone.utc)

    # ── Metric cards ─────────────────────────────────────────────────────────
    st.markdown("---")
    col_now, col_6, col_12, col_24 = st.columns(4)

    for col, val, label_top, model_name in [
        (col_now, current_pm25, "Now (observed)", ""),
        (col_6,   forecasts[6],  "+6 h",          "XGBoost"),
        (col_12,  forecasts[12], "+12 h",          "Ridge"),
        (col_24,  forecasts[24], "+24 h",          "Ridge"),
    ]:
        color = aqi_color(val)
        qlabel = aqi_label(val)
        delta_str = ""
        if val != current_pm25:
            d = val - current_pm25
            delta_str = f"<div style='font-size:0.75rem;color:#888'>{'▲' if d >= 0 else '▼'} {abs(d):.0f} vs now</div>"
        sub = f"<div style='font-size:0.8rem;color:#aaa'>{model_name}</div>" if model_name else ""
        time_str = f"<div style='font-size:0.75rem;color:#888'>{last_ts.strftime('%H:%M UTC')}</div>" if val == current_pm25 else ""
        with col:
            st.markdown(
                f"<div style='text-align:center;padding:8px'>"
                f"<div style='font-size:0.9rem;color:#bbb'>{label_top}</div>"
                f"{sub}"
                f"<div style='font-size:3rem;font-weight:bold;color:{color}'>{val:.0f}</div>"
                f"<div style='font-size:0.85rem;color:{color}'>{qlabel}</div>"
                f"{delta_str}{time_str}"
                f"</div>",
                unsafe_allow_html=True,
            )

    # ── Tabs ──────────────────────────────────────────────────────────────────
    st.markdown("---")
    tab_forecast, tab_map, tab_history, tab_cities = st.tabs(
        ["📈 Forecast", "🗺️ Map", "📅 7-Day History", "🌍 Other Cities"]
    )

    # ── Tab 1: Forecast chart ─────────────────────────────────────────────────
    with tab_forecast:
        st.subheader("Observed & forecast PM2.5")

        cutoff = pm25_df.index[-1] - pd.Timedelta(hours=24)
        obs = pm25_df["pm25"][pm25_df.index >= cutoff]
        fc_times = [last_ts + pd.Timedelta(hours=h) for h in [6, 12, 24]]
        fc_vals  = [forecasts[h] for h in [6, 12, 24]]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=obs.index, y=obs.values,
            mode="lines", name="Observed",
            line=dict(color="#56B4E9", width=2),
        ))
        fig.add_trace(go.Scatter(
            x=fc_times, y=fc_vals,
            mode="markers+lines", name="Forecast",
            line=dict(color="#E69F00", width=2, dash="dash"),
            marker=dict(size=10, color="#E69F00"),
        ))
        fig.add_trace(go.Scatter(
            x=[last_ts, fc_times[0]], y=[current_pm25, fc_vals[0]],
            mode="lines", showlegend=False,
            line=dict(color="#E69F00", width=1.5, dash="dot"),
        ))
        fig.add_hline(y=15,  line_dash="dot", line_color="#2ECC71",
                      annotation_text="WHO 24h (15)", annotation_position="bottom right")
        fig.add_hline(y=75, line_dash="dot", line_color="#E74C3C",
                      annotation_text="Unhealthy (75)", annotation_position="top right")
        fig.update_layout(
            xaxis_title="Time (UTC)", yaxis_title="PM2.5 (μg/m³)",
            yaxis=dict(rangemode="tozero"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            height=380, margin=dict(l=20, r=20, t=20, b=20),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#FAFAFA"),
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── Tab 2: Map + Districts table ──────────────────────────────────────────
    with tab_map:
        col_map, col_table = st.columns([3, 2])

        with col_map:
            st.subheader("Station map")
            with st.spinner("Loading per-station data…"):
                stations_df = fetch_stations_current()

            m = build_map(stations_df, current_pm25)
            st_folium(m, width=None, height=480, returned_objects=[])

            # AQI legend
            legend_html = " ".join([
                f"<span style='background:{c};padding:2px 8px;"
                f"border-radius:4px;font-size:0.8rem'>{lbl}</span>"
                for _, lbl, c in AQI_LEVELS
            ])
            st.markdown(f"**AQI:** {legend_html}", unsafe_allow_html=True)

        with col_table:
            st.subheader("Districts overview")
            districts_df = build_districts_table(stations_df, forecasts, current_pm25)
            if not districts_df.empty:
                st.dataframe(
                    districts_df,
                    use_container_width=True,
                    hide_index=True,
                    height=460,
                )
            else:
                st.info("District data unavailable.")

    # ── Tab 3: 7-day history ──────────────────────────────────────────────────
    with tab_history:
        st.subheader("City-median PM2.5 — last 7 days")
        with st.spinner("Loading 7-day history…"):
            hist7 = fetch_pm25_history(hours=168)

        if hist7 is not None and not hist7.empty:
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=hist7.index, y=hist7["pm25"].values,
                mode="lines", name="PM2.5",
                line=dict(color="#56B4E9", width=1.5),
                fill="tozeroy", fillcolor="rgba(86,180,233,0.15)",
            ))
            # 24h rolling average
            roll = hist7["pm25"].rolling(24, center=True, min_periods=6).mean()
            fig2.add_trace(go.Scatter(
                x=roll.index, y=roll.values,
                mode="lines", name="24h rolling mean",
                line=dict(color="#E69F00", width=2),
            ))
            fig2.add_hline(y=15, line_dash="dot", line_color="#2ECC71",
                           annotation_text="WHO 24h (15)", annotation_position="bottom right")
            fig2.add_hline(y=75, line_dash="dot", line_color="#E74C3C",
                           annotation_text="Unhealthy (75)", annotation_position="top right")
            fig2.update_layout(
                xaxis_title="Date (UTC)", yaxis_title="PM2.5 (μg/m³)",
                yaxis=dict(rangemode="tozero"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                height=400, margin=dict(l=20, r=20, t=20, b=20),
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#FAFAFA"),
            )
            st.plotly_chart(fig2, use_container_width=True)

            # Summary stats
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("7d mean",   f"{hist7['pm25'].mean():.1f} μg/m³")
            c2.metric("7d max",    f"{hist7['pm25'].max():.1f} μg/m³")
            c3.metric("7d min",    f"{hist7['pm25'].min():.1f} μg/m³")
            c4.metric("Hours >75", str((hist7["pm25"] > 75).sum()))
        else:
            st.info("7-day history unavailable. Check OpenAQ API key.")

    # ── Tab 4: Other Cities ───────────────────────────────────────────────────
    with tab_cities:
        st.subheader("Pipeline reproducibility — other Central Asian cities")
        st.info(
            "The same data pipeline (OpenAQ + Open-Meteo) runs unchanged for any city. "
            "Only the coordinates in `src/config.py` need updating. "
            "Forecast models require retraining on local historical data."
        )

        city_name = st.selectbox(
            "Select city",
            [c[0] for c in OTHER_CITIES],
            index=0,
        )
        city_row  = next(c for c in OTHER_CITIES if c[0] == city_name)
        _, country, clat, clon = city_row

        col_info, col_map2 = st.columns([1, 2])

        with col_info:
            st.markdown(f"**{city_name}, {country}**")
            st.markdown(f"Coordinates: {clat:.4f}°N, {clon:.4f}°E")
            st.markdown(f"Search radius: 25 km")

            with st.spinner(f"Fetching OpenAQ sensors for {city_name}…"):
                city_df = fetch_city_stations(clat, clon)

            if city_df.empty:
                st.warning(f"No active PM2.5 sensors found in {city_name}. "
                           "Coverage may be limited in this area.")
            else:
                n_sensors   = len(city_df)
                with_data   = city_df.dropna(subset=["pm25"])
                median_pm25 = float(with_data["pm25"].median()) if not with_data.empty else None

                st.markdown("---")
                st.metric("PM2.5 sensors found", n_sensors)
                st.metric("Sensors with recent data", len(with_data))

                if median_pm25 is not None:
                    color = aqi_color(median_pm25)
                    label = aqi_label(median_pm25)
                    st.markdown(
                        f"<div style='text-align:left;padding:4px 0'>"
                        f"<span style='font-size:0.9rem;color:#bbb'>Current median PM2.5</span><br>"
                        f"<span style='font-size:2.4rem;font-weight:bold;color:{color}'>"
                        f"{median_pm25:.0f} μg/m³</span><br>"
                        f"<span style='font-size:0.85rem;color:{color}'>{label}</span>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.info("Sensor locations found but no recent hourly readings available.")
                st.markdown("---")
                st.markdown("**vs Almaty baseline**")
                st.markdown(f"- Almaty: 192 sensors, {current_pm25:.0f} μg/m³ now")
                pm25_str = f"{median_pm25:.0f} μg/m³" if median_pm25 else "no recent data"
                st.markdown(f"- {city_name}: {n_sensors} sensors, {pm25_str}")

        with col_map2:
            m2 = folium.Map(location=[clat, clon], zoom_start=11,
                            tiles="CartoDB dark_matter")
            if not city_df.empty:
                with_data = city_df.dropna(subset=["pm25"])
                # Heatmap only for stations with real readings
                if len(with_data) > 2:
                    HeatMap(
                        [[r.lat, r.lon, r.pm25] for r in with_data.itertuples()],
                        radius=20, blur=30, min_opacity=0.3,
                        gradient={0.0: "#2ECC71", 0.33: "#F1C40F",
                                  0.66: "#E74C3C", 1.0: "#8E44AD"},
                    ).add_to(m2)
                for row in city_df.itertuples():
                    has_val = row.pm25 is not None and not (isinstance(row.pm25, float) and np.isnan(row.pm25))
                    color   = aqi_color(row.pm25) if has_val else "#666666"
                    tip     = f"{row.name}: {row.pm25:.0f} μg/m³" if has_val else f"{row.name}: no recent data"
                    folium.CircleMarker(
                        location=[row.lat, row.lon],
                        radius=5, color=color, fill=True,
                        fill_color=color, fill_opacity=0.8,
                        tooltip=tip,
                    ).add_to(m2)
            else:
                # No sensors at all - show city centre pin
                folium.Marker(location=[clat, clon],
                              tooltip=f"{city_name}: no sensors found").add_to(m2)
            st_folium(m2, width=None, height=420, returned_objects=[])

        # Config snippet
        st.markdown("---")
        st.markdown("**To deploy a forecast for this city — change two lines in `src/config.py`:**")
        st.code(
            f"# src/config.py\n"
            f"CITY_NAME = \"{city_name}\"\n"
            f"LAT, LON  = {clat}, {clon}\n\n"
            f"# Then retrain:\n"
            f"uv run python scripts/train_models.py",
            language="python",
        )

    # ── About expander ────────────────────────────────────────────────────────
    st.markdown("---")
    with st.expander("About this forecast"):
        st.markdown(
            """
**Models:** XGBoost (6-hour horizon), Ridge regression (12- and 24-hour horizons).
Trained on 9,242 hours of OpenAQ LCS data and Open-Meteo meteorology
(October 2024 - April 2026).

**Key features:** boundary-layer height (BLH), PM2.5 lag features (1-24 h),
wind components, temperature gradient, and heating-season indicator.

**Test-set performance (winter 2025-26, 2,311 h):**

| Horizon | Model | RMSE | R² |
|---------|-------|------|-----|
| +6 h | XGBoost | 23.4 μg/m³ | 0.545 |
| +12 h | Ridge | 25.9 μg/m³ | 0.446 |
| +24 h | Ridge | 27.2 μg/m³ | 0.383 |

**Data sources:** [OpenAQ](https://openaq.org) (CC BY 4.0) · [Open-Meteo](https://open-meteo.com)

**Source:** KBTU Master's thesis - *Development of an intelligent system
for investigating and solving ecological problems*, 2026.
            """
        )
    st.caption(
        f"Last updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} · "
        "Free to use · No authentication required"
    )


if __name__ == "__main__":
    main()
