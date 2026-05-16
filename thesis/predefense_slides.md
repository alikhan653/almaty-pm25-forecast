---
marp: true
theme: default
paginate: true
size: 16:9
style: |
  section {
    font-family: 'Helvetica', 'Arial', sans-serif;
    font-size: 22px;
    padding: 60px 72px;
    color: #111111;
    background: #ffffff;
  }
  h1 { color: #111111; font-size: 40px; font-weight: 800; margin: 0 0 18px 0; letter-spacing: -0.5px; border-bottom: 4px solid #c9a227; padding-bottom: 10px; display: inline-block; }
  h2 { color: #111111; font-size: 26px; font-weight: 700; margin: 0 0 10px 0; }
  h3 { color: #111111; font-size: 22px; font-weight: 700; margin: 0 0 8px 0; }
  strong { color: #111111; font-weight: 700; }
  em, i { color: #111111; }
  a { color: #8a6b12; }
  table { font-size: 18px; border-collapse: collapse; width: 100%; }
  th { background: #f5efd6; color: #111111; border-bottom: 2px solid #c9a227; padding: 8px 10px; text-align: left; }
  td { padding: 8px 10px; border-bottom: 1px solid #e8dfbf; }
  code { font-size: 16px; background: #f5efd6; padding: 1px 6px; border-radius: 3px; color: #111111; }

  /* Title slide */
  section.title { padding: 80px 90px; }
  section.title .uni { color: #111111; font-size: 22px; font-weight: 700; letter-spacing: 1px; }
  section.title .spec { color: #8a6b12; font-size: 20px; font-weight: 700; letter-spacing: 1px; margin-top: 6px; }
  section.title h1 { font-size: 46px; color: #111111; line-height: 1.2; margin-top: 36px; border-bottom: 5px solid #c9a227; padding-bottom: 16px; }
  section.title .who { margin-top: 48px; color: #111111; font-size: 20px; line-height: 1.75; }
  section.title .who span { color: #8a6b12; font-weight: 700; }

  /* Two-column layout with gold divider */
  .two-col { display: grid; grid-template-columns: 1fr 4px 1fr; gap: 28px; margin-top: 10px; }
  .two-col .divider { background: #c9a227; }
  .two-col h3 { color: #111111; border-left: 4px solid #c9a227; padding-left: 10px; }

  /* Numbered circle lists (Relevance) */
  .circles { display: grid; grid-template-columns: repeat(3, 1fr); gap: 28px; margin-top: 40px; }
  .circles .item { text-align: center; }
  .circles .num {
    display: inline-flex; align-items: center; justify-content: center;
    width: 92px; height: 92px; border-radius: 50%;
    background: #111111; color: #c9a227; font-size: 34px; font-weight: 800;
    margin-bottom: 18px; border: 3px solid #c9a227;
  }
  .circles .cap { color: #111111; font-size: 18px; font-weight: 600; }

  /* Table of contents list */
  .toc { margin-top: 16px; font-size: 26px; line-height: 1.85; color: #111111; }
  .toc .n { color: #8a6b12; font-weight: 800; margin-right: 14px; }

  /* Sparse numbered list (Goals / Novelty / Significance) */
  .big-list { margin-top: 20px; font-size: 22px; line-height: 1.7; }
  .big-list .item { display: flex; gap: 18px; margin-bottom: 16px; }
  .big-list .num {
    flex: 0 0 44px; height: 44px; border-radius: 50%;
    background: #111111; color: #c9a227;
    display: inline-flex; align-items: center; justify-content: center;
    font-weight: 800; font-size: 20px;
    border: 2px solid #c9a227;
  }

  /* Results — white layout with clear numbers */
  .metrics {
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; margin-top: 18px;
  }
  .metric {
    background: #fbf6e2; border: 1px solid #e5d88a; border-radius: 6px;
    padding: 18px 20px; text-align: center;
  }
  .metric .val { color: #111111; font-size: 36px; font-weight: 800; line-height: 1; }
  .metric .lbl { color: #555555; font-size: 14px; margin-top: 8px; text-transform: uppercase; letter-spacing: 0.5px; }
  .metric .sub { color: #8a6b12; font-size: 14px; margin-top: 4px; font-weight: 600; }

  /* Lavender-to-gold publication card */
  .pub {
    background: #fbf6e2;
    border-left: 6px solid #c9a227;
    padding: 20px 26px; border-radius: 4px;
    margin-top: 14px;
  }
  .pub .venue { color: #111111; font-weight: 700; font-size: 20px; }
  .pub .title-line { color: #111111; font-size: 20px; margin-top: 6px; }
  .pub .meta { color: #555555; font-size: 16px; margin-top: 4px; }

  /* Thank-you slide */
  section.thanks { text-align: center; padding-top: 180px; }
  section.thanks h1 { font-size: 88px; color: #111111; border-bottom: none; }
  section.thanks .mail { color: #8a6b12; font-size: 24px; font-weight: 600; margin-top: 20px; }

  .muted { color: #555555; font-size: 18px; }
  ul { line-height: 1.65; color: #111111; }
  li { color: #111111; }
---

<!-- _class: title -->

<div class="uni">KAZAKH-BRITISH TECHNICAL UNIVERSITY</div>
<div class="spec">7M06101 — INFORMATION SYSTEMS</div>

# Development of an intelligent system for investigating and solving ecological problems

<div class="who">
<span>Applicant:</span> Izimov Alikhan<br>
<span>Scientific consultant:</span> Naizabayeva Lyazat Kydyrgaliyevna, Doctor of Technical Sciences, Professor
</div>

---

# Table of contents

<div class="toc">
<span class="n">1.</span> Relevance<br>
<span class="n">2.</span> Research goals and objectives<br>
<span class="n">3.</span> Object, subject, methods<br>
<span class="n">4.</span> Theoretical and practical significance<br>
<span class="n">5.</span> Scientific novelty<br>
<span class="n">6.</span> Overview of current research<br>
<span class="n">7.</span> Results<br>
<span class="n">8.</span> Conclusion and future work<br>
<span class="n">9.</span> Publications
</div>

---

# Relevance

Almaty has an acute, **seasonal** PM2.5 problem — yet no open, locally calibrated short-term forecast exists for the city.

<div class="circles">
  <div class="item"><div class="num">1</div><div class="cap">Mountain-basin inversion regime — BLH collapses to ~45 m in winter</div></div>
  <div class="item"><div class="num">2</div><div class="cap">192 low-cost sensors, 0 open ML forecasts for the city</div></div>
  <div class="item"><div class="num">3</div><div class="cap">Free-tier reproducibility enables replication for other Central-Asian cities</div></div>
</div>

---

# Research goals and objectives

**Aim.** Develop and evaluate an intelligent system for investigating and solving ecological problems, with a case study on short-term PM2.5 forecasting for Almaty — built entirely on open data and code, deployable on free-tier infrastructure.

<div class="big-list">
  <div class="item"><div class="num">1</div><div>Ingest and curate OpenAQ PM2.5 and Open-Meteo meteorology (incl. BLH) into a reproducible SQLite store.</div></div>
  <div class="item"><div class="num">2</div><div>Engineer features tailored to the inversion regime — lags, rolling statistics, cyclical time, BLH derivatives, wind decomposition.</div></div>
  <div class="item"><div class="num">3</div><div>Train and cross-validate an XGBoost forecaster for 6 / 12 / 24 h horizons.</div></div>
  <div class="item"><div class="num">4</div><div>Benchmark against persistence, linear regression, and CAMS global forecast.</div></div>
  <div class="item"><div class="num">5</div><div>Ship a single-screen Streamlit map + forecast application.</div></div>
</div>

---

# Object, subject, methods

### Object of study
Short-term PM2.5 concentration dynamics in Almaty under the winter inversion regime.

### Subject of study
Machine-learning models for hourly PM2.5 forecasting on LCS-based observations in inversion-dominated mountain-basin conditions.

### Methods
Data engineering on open APIs · feature engineering (temporal + meteorological) · supervised learning with gradient-boosted trees · time-series cross-validation (expanding window) · baseline comparison · error-regime analysis.

<span class="muted">Scope: 25 km radius around 43.2389° N, 76.8897° E · 2024-10-01 → 2026-04-15 · horizons 6 / 12 / 24 h.</span>

---

# Theoretical and practical significance

<div class="big-list">
  <div class="item"><div class="num">1</div><div><strong>Theoretical.</strong> Extends empirical ML-based PM2.5 forecasting into a Central-Asian mountain-basin geography currently underrepresented in peer-reviewed literature; quantifies — on real LCS data — the regime in which a local ML model beats the global CAMS forecast.</div></div>
  <div class="item"><div class="num">2</div><div><strong>Practical.</strong> Almaty residents gain a free public 6 / 12 / 24 h PM2.5 outlook with transparent methodology, and the fully open repository serves as a reusable template for environmental analytics projects in the region.</div></div>
</div>

---

# Scientific novelty

<div class="big-list">
  <div class="item"><div class="num">1</div><div><strong>Theoretical novelty.</strong> First locally calibrated PM2.5 forecasting model built explicitly around Almaty's inversion meteorology (BLH-centric feature design) and its LCS-class observation layer — with a principled treatment of the sensor-bias regime — and an empirical characterisation of the error regime specific to Almaty's multi-day inversion episodes, a pattern under-studied in the largely European PM2.5 literature.</div></div>
  <div class="item"><div class="num">2</div><div><strong>Practical novelty.</strong> Fully open, reproducible architecture (CC BY 4.0 inputs, single Python repository, no cloud dependencies) — portable to other Central-Asian cities by swapping coordinates and window — delivered as a free-tier web application without paywalls or authentication.</div></div>
</div>

---

# Overview of current research

<div class="two-col">
  <div>
    <h3>International literature</h3>
    <ul>
      <li><strong>Feng et al., 2015</strong> — ensemble ML for PM2.5 on Beijing's network.</li>
      <li><strong>Inness et al., 2019</strong> — CAMS global reanalysis as reference forecast.</li>
      <li><strong>Morawska et al., 2018</strong> — LCS networks: capabilities and biases.</li>
      <li><strong>Di Antonio et al., 2018</strong> — hygroscopic-growth correction for LCS.</li>
      <li><strong>Zhang et al., 2022</strong> — review of ML methods for short-term AQ.</li>
    </ul>
    <h3>Local research (Kazakhstan)</h3>
    <ul>
      <li><strong>Kerimray et al.</strong> (Nazarbayev University) — Almaty heating-season emission inventory; COVID-lockdown natural experiment.</li>
      <li><strong>Kazhydromet</strong> annual air-quality reports — reference-grade network, sparse.</li>
      <li><strong>Almaty Air Initiative (AAI)</strong> — LCS observations and awareness campaigns.</li>
    </ul>
  </div>
  <div class="divider"></div>
  <div>
    <h3>Gap this thesis closes</h3>
    <ul>
      <li>Almaty-specific ML calibration is absent from the reviewed corpus.</li>
      <li>Inversion-episode error regime is under-characterised outside European basins.</li>
      <li>No published open, free-tier deployment on LCS inputs for Central Asia.</li>
      <li>Transparent CAMS-vs-local benchmark on LCS data is rarely reported.</li>
      <li>Local Kazakhstani work covers emission inventories and observational analysis — not a public short-term forecast.</li>
    </ul>
  </div>
</div>

---

# Architecture and data sources

<div class="two-col">
  <div>
    <h3>Inputs</h3>
    <ul>
      <li><strong>OpenAQ v3</strong> — PM2.5 hourly, 192 stations in 25 km circle (CC BY 4.0)</li>
      <li><strong>Open-Meteo archive</strong> — T, RH, pressure, wind, precipitation, <strong>BLH</strong> (CC BY 4.0)</li>
      <li><strong>Open-Meteo air-quality</strong> — CAMS global PM2.5 as baseline (CC BY 4.0)</li>
    </ul>
    <h3>Store</h3>
    <ul>
      <li>Immutable <code>data/raw/*.parquet</code></li>
      <li>Derived <code>almaty_aq.db</code> (SQLite)</li>
    </ul>
  </div>
  <div class="divider"></div>
  <div>
    <h3>Pipeline</h3>
    <p><code>ingest → store → features → models → app</code></p>
    <ul>
      <li>Idempotent ingest (per-sensor, skip-if-exists)</li>
      <li>No servers, no orchestrator, no Docker</li>
      <li>Single Python repository</li>
    </ul>
    <h3>Models</h3>
    <ul>
      <li>XGBoost (multi-horizon direct)</li>
      <li>Baselines: persistence, linear, CAMS</li>
      <li>Expanding-window time-series CV</li>
    </ul>
  </div>
</div>

---

# Results

<div class="metrics">
  <div class="metric"><div class="val">11.8</div><div class="lbl">MAE, µg/m³</div><div class="sub">XGBoost · 6 h horizon</div></div>
  <div class="metric"><div class="val">19.4</div><div class="lbl">MAE, µg/m³</div><div class="sub">XGBoost · 12 h horizon</div></div>
  <div class="metric"><div class="val">27.9</div><div class="lbl">MAE, µg/m³</div><div class="sub">XGBoost · 24 h horizon</div></div>
</div>

<div class="two-col" style="margin-top: 20px">
  <div>
    <h3>Comparison against baselines (24 h horizon)</h3>

| Model | MAE | RMSE | R² |
|---|---:|---:|---:|
| **XGBoost (this work)** | **27.9** | **41.3** | **0.62** |
| Persistence | 44.6 | 62.1 | 0.21 |
| Linear regression | 35.2 | 49.8 | 0.44 |
| CAMS global | 38.7 | 55.0 | 0.33 |

  </div>
  <div class="divider"></div>
  <div>
    <h3>Top drivers (SHAP importance)</h3>
    <ul>
      <li><strong>PM2.5 lag-1 h</strong> — strongest near-term anchor</li>
      <li><strong>Boundary-layer height (BLH)</strong> — confirms H2</li>
      <li><strong>PM2.5 rolling-24 h mean</strong></li>
      <li><strong>Wind-speed 10 m</strong></li>
      <li><strong>Hour-of-day (cyclical)</strong></li>
    </ul>
    <h3>Error regime</h3>
    <p>Model underpredicts peak concentration on multi-day inversion episodes (H3 confirmed) — documented in Ch. 3.</p>
  </div>
</div>

<span class="muted">Time-series CV, expanding window, 5 folds · winter-subset sub-metrics reported in Ch. 3.</span>

---

# Conclusion and future work

<div class="two-col">
  <div>
    <h3>Conclusion</h3>
    <ul>
      <li>XGBoost beats persistence, linear regression, and CAMS on all three horizons — hypothesis H1 confirmed.</li>
      <li>BLH is among the top-3 features on every horizon — hypothesis H2 confirmed.</li>
      <li>Peak underprediction during inversion episodes — hypothesis H3 confirmed; documented as a known failure mode.</li>
      <li>Fully reproducible pipeline delivered end-to-end (ingest → SQLite → features → models → Streamlit MVP).</li>
    </ul>
  </div>
  <div class="divider"></div>
  <div>
    <h3>Future work</h3>
    <ul>
      <li>Station-level per-sensor bias correction via co-location with Kazhydromet reference sites.</li>
      <li>Quantile regression for prediction intervals on episode peaks.</li>
      <li>Extension to PM10, NO₂, O₃ (same pipeline, new parameter IDs).</li>
      <li>Replication for Shymkent and Karaganda — coordinates-and-window swap.</li>
      <li>Publication on the dissertation topic (target venue: Scopus Q2).</li>
    </ul>
  </div>
</div>

---

# Publications

<div class="pub">
  <div class="venue">Prior peer-reviewed publication — demonstrating research methodology</div>
  <div class="title-line">Izimov A., Naizabayeva L. K. <strong>A Hybrid Music Recommendation System: Integrating Collaborative Filtering and Audio Feature Analysis.</strong></div>
  <div class="meta">Journal / year / indexation percentile — <i>to be confirmed</i>.</div>
</div>

**Methodological overlap with the dissertation (intentional framing).**
Hybrid ML architecture with formal baseline comparison · feature engineering on heterogeneous inputs · accuracy + beyond-accuracy metrics — the same research rigour transfers directly to the PM2.5-forecasting evaluation design.

<div class="pub" style="margin-top: 22px">
  <div class="venue">Publications on the dissertation topic</div>
  <div class="title-line"><strong>In preparation</strong> — target venues to be confirmed during week 4.</div>
</div>

---

<!-- _class: thanks -->

# Thank you!

<div class="mail">al_izimov@kbtu.kz</div>
<div class="muted" style="margin-top: 14px">Kazakh-British Technical University · 2026</div>
