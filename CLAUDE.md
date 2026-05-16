# Project: Almaty PM2.5 Forecasting — Master's Thesis (KBTU)

## Before writing any thesis content

**MANDATORY:** Read the relevant files from `requirements/` before writing or
revising any chapter, section, or paragraph of the dissertation.

| Task | Files to read first |
|---|---|
| Writing a chapter | `requirements/kbtu_structure.md` + `requirements/writing_style.md` |
| Checking formatting | `requirements/formatting.md` |
| Adding citations | `requirements/citations.md` |
| End of chapter review | `requirements/checklist.md` |
| Any writing task | `requirements/README.md` (for essential facts) |

## Project context

- **plan.md** is the authoritative project plan. Read it at the start of each session.
- **thesis/** contains all chapter drafts.
- **requirements/** contains binding formatting and style constraints.
- **src/** contains the Python pipeline (ingest → features → models → app).
- **data/almaty_aq.db** is the SQLite database (578,993 PM2.5 obs, 190 sensors).

## Key facts (do not re-derive these)

- University: Kazakh-British Technical University (KBTU), program 7M06106
- Thesis language: **English**
- Citation style: **APA 7th edition**
- Formatting standard: **GOST 7.32-2017**
- Margins: left 30 mm, right 15 mm, top/bottom 20 mm; font TNR 14 pt, 1.5 line spacing
- Anti-plagiarism: Antiplagiat.ru (includes AI-detection); target ≥ 90% originality
- Model results (held-out test, winter 2025–26):
  - XGBoost +6 h: RMSE = 23.44 μg/m³, R² = 0.545
  - XGBoost +12 h: RMSE = 28.67 μg/m³, R² = 0.318
  - XGBoost +24 h: RMSE = 31.48 μg/m³, R² = 0.175
  - CAMS (all horizons): R² ≤ −0.18 (negative — worse than mean predictor)

## Constraints (from plan.md §2 and §4)

Do NOT add without explicit author approval:
- Docker, Kubernetes, cloud infrastructure
- React/Vue/Next.js frontend
- PostgreSQL, Redis, Kafka
- Airflow, Prefect, Dagster
- Mobile app or push notifications

## Session start protocol

1. Read `plan.md` to know current day and status.
2. Read `requirements/README.md` for essential facts.
3. Report what day of the plan we are on and what is next.
