# Pre-defence speaking script — English

> Target: 10–12 minutes. Each slide has a full spoken text and short
> bullets as a fallback. Written in simple, direct English.

---

## What the system does — in one paragraph

The system is a small open-source program. Every hour it does four
things. First, it downloads fresh pollution readings from 192
sensors across Almaty. Second, it downloads the current weather for
the city. Third, it feeds both into a model trained on 18 months of
history. Fourth, it outputs a forecast of pollution for the next 6,
12, and 24 hours, and shows it on a public map anyone can open.
That is the whole product. **Open data in, open forecast out.**

---

## Short glossary

- **Inversion.** In winter, warm air sits on top of cold air like a
  lid. Pollution gets trapped under it.
- **Boundary-layer height (BLH).** How thick that trapped layer is.
  In Almaty in winter it can drop to ~45 m — the height of a
  15-storey building.
- **Low-cost sensor (LCS).** A cheap (~$200) pollution device. Less
  accurate than a government station, but many of them cover the
  city well.
- **Baseline.** A simple method we compare our model against. If we
  don't beat the baselines, our model is not useful.
- **CAMS.** The European global air-quality forecast. It works on a
  40 km grid, so all of Almaty fits in one cell.

---

## Slide 1 — Title

### Full speech
Good afternoon. My name is Alikhan Izimov. I am a master's student
at KBTU in Information Systems. My consultant is Professor
Naizabayeva Lyazat Kydyrgaliyevna. The title of my thesis is
*Development of an intelligent system for investigating and solving
ecological problems*. I show this with a real case — short-term
air-pollution forecasting for Almaty. Today I will explain why this
is needed, how the system works, and what it achieves.

### Bullets
- Alikhan Izimov, Information Systems, KBTU.
- Consultant: Prof. Naizabayeva L. K.
- Thesis: *Development of an intelligent system for investigating
  and solving ecological problems*.
- Case study: PM2.5 forecasting for Almaty.

---

## Slide 2 — Table of contents

### Full speech
Nine sections: relevance, goals, object/subject/methods,
significance, novelty, current research, results, conclusion,
publications.

### Bullets
- Nine sections. Problem → approach → results.

---

## Slide 3 — Relevance

### Full speech
Three reasons this work matters.

**One — Almaty has a serious winter pollution problem.** The city
sits in a bowl of mountains. In winter, warm air sits on top of cold
air and acts like a lid. Pollution from home heating and traffic
cannot rise and spread out. It gets trapped in a very thin layer
close to the ground — sometimes only 45 metres tall. That is as
high as a 15-storey building. This is called an *inversion*. It is
why Almaty's problem is different from most other cities in
air-quality research.

**Two — we only have cheap sensors.** There is almost no government
monitoring. Instead, the city has 192 low-cost sensors. Each one is
not very accurate, but together they cover the city well. This is
the only data we have, so we must work with it.

**Three — there is no open forecast.** Commercial apps give you a
number, but they do not show how it is made. You cannot check or
improve them. My thesis closes this gap.

### Bullets
- Winter inversion traps pollution in a thin layer (~45 m in Almaty).
- Only low-cost sensors available — no reference network.
- No open, reproducible forecast exists yet.

---

## Slide 4 — Goals and objectives

### Full speech
The goal is to build a smart system that takes open environmental
data and turns it into a useful short-term forecast. I test this on
Almaty PM2.5. The whole system runs on free and open tools, so
anyone can copy it or adapt it to another city.

**What the system does in practice — five steps:**

1. **Collect** the sensor readings and the weather data.
2. **Build features** — turn the raw numbers into inputs the model
   can learn from (recent pollution, rolling averages, wind, BLH).
3. **Train** the model on 18 months of history.
4. **Compare** the model against three simpler methods to prove it
   is really better.
5. **Deliver** the forecast to people, as a public web map.

### Bullets
- Goal: open data → useful forecast, on free tools only.
- Five steps: collect, build features, train, compare, deliver.

---

## Slide 5 — Object, subject, methods

### Full speech
Formally:

- **Object** — what I study: short-term PM2.5 pollution in Almaty.
- **Subject** — how I study it: machine-learning models on low-cost
  sensor data, in a city with strong winter inversions.

On methods — my main rule is simple: **do not trust the model on
its own word.** I compare it against three baselines:
1. "Today equals tomorrow" — the simplest possible forecast.
2. A classical statistical model.
3. CAMS — the European global forecast.

Only if my model beats all three, I claim it works.

I also **respect time**. The model is tested only on data *after*
its training data. I never shuffle the history. If I did, the model
would "see the future" during training, and the scores would be
fake.

### Bullets
- **Object:** short-term PM2.5 in Almaty.
- **Subject:** ML models on low-cost sensors, inversion city.
- **Rule 1:** beat at least three baselines.
- **Rule 2:** never shuffle time; test is always after train.

---

## Slide 6 — Theoretical and practical significance

### Full speech
**Theoretical side.** Most air-quality research is about European
and American cities. Almaty is a mountain-basin city in Central
Asia, and it is almost missing from the literature. This work adds
our kind of city to the record. It also gives one of the first open
comparisons between a local model and the global CAMS forecast in
this setting.

**Practical side.** Almaty residents get a free forecast they can
check before they go outside. Any city with similar sensors and
similar geography can reuse the pipeline — just change the
coordinates and the time window.

### Bullets
- **Theoretical:** fills a gap for Central-Asian mountain cities;
  shows when local models beat the global CAMS forecast.
- **Practical:** free public forecast for Almaty; reusable for
  similar cities.

---

## Slide 7 — Scientific novelty

### Full speech
Two points.

**Theoretical novelty.** This is the first public forecasting model
built specifically for Almaty's inversion weather and for its
low-cost sensor data. It also describes honestly when the model
fails — during long pollution episodes, which are exactly the ones
that matter most for health.

**Practical novelty.** The whole system is fully open and free to
run. No paid services. No private data. No servers to maintain.

### Bullets
- **Theoretical:** first open model for Almaty's inversion + LCS
  setting, with honest failure description.
- **Practical:** fully open, fully free to run, no paid services.

---

## Slide 8 — Overview of current research

### Full speech
A short tour.

**International.** There are four main ways to forecast air
quality: classical statistics, tabular machine learning, deep
neural networks, and hybrid physics + ML. For data sizes like ours
(about 18 months), tabular ML works best.

**The global baseline — CAMS.** This is the European air-quality
forecast. It uses a 40 km grid. All of Almaty fits inside one cell
of that grid, so CAMS cannot see the mountain-basin effect. But it
is the best open forecast, so I compare against it.

**Local research.** In Kazakhstan, the Kerimray group at Nazarbayev
University studies Almaty emissions and the COVID-lockdown
experiment. Kazhydromet publishes yearly reports. Almaty Air
Initiative runs the sensor network. But no one has published an
open short-term forecast. This thesis fills that gap.

### Bullets
- International: 4 approaches; tabular ML best at our data size.
- CAMS: European global forecast, 40 km grid, too coarse for
  Almaty, but used as external baseline.
- Local: Kerimray, Kazhydromet, Almaty Air Initiative — no
  forecasting product yet.

---

## Slide 9 — Architecture and data sources

### Full speech
Three open data sources:

- **OpenAQ** — public air-quality data, 192 sensors in a 25 km
  circle around the city centre.
- **Open-Meteo** — free weather data: temperature, humidity,
  pressure, wind, precipitation, and boundary-layer height.
- **CAMS forecast** — also from Open-Meteo, used as a baseline.

The data flows in a straight line: raw files on disk → SQLite
database → feature matrix → model → Streamlit web app.

No paid cloud. No servers. No containers. Just one Python project.
This makes it easy to copy and reproduce.

### Bullets
- OpenAQ + Open-Meteo + CAMS baseline.
- Flow: parquet → SQLite → features → XGBoost → Streamlit.
- No paid cloud, no servers — one Python repo.

---

## Slide 10 — Results

### Full speech
Three numbers to set the scale.

For the 24-hour forecast, my model's **average error** is about 28
micrograms per cubic metre of PM2.5. The naive "today equals
tomorrow" forecast has 45. A simple linear model has 35. CAMS has
39. So my model has the lowest error by a big margin — about 37%
better than "today equals tomorrow" and 28% better than CAMS.

How much of the pollution changes can my model explain? About 62%.
The naive forecast can only explain 21%, and CAMS only 33%. So the
model captures a lot more of the pattern.

Where does the improvement come from? The most important input is
recent pollution. Right after that comes **boundary-layer height** —
exactly the physical variable hypothesis H2 predicted. Then come
the 24-hour rolling average, wind speed, and hour of day.

**One honest weakness.** During long pollution episodes — the
multi-day ones — the model underestimates the peak. This happens
because the training rewards average accuracy, not peak accuracy. I
report this openly instead of hiding it.

### Bullets
- 24 h error (MAE, µg/m³): **my model 27.9**, persistence 44.6,
  linear 35.2, CAMS 38.7.
- Model explains 62% of pollution changes vs. 21% (persistence) and
  33% (CAMS).
- Top drivers: recent pollution, **BLH (H2 confirmed)**, rolling
  mean, wind speed, hour of day.
- Weakness: peaks on long episodes are underestimated. Reported
  openly.

---

## Slide 11 — Conclusion and future work

### Full speech
All three hypotheses from Chapter 1 are confirmed:

- **H1** — the model beats every baseline on every horizon. ✓
- **H2** — boundary-layer height is among the top drivers. ✓
- **H3** — the model underestimates peaks on long episodes. ✓
  (known weakness, reported honestly)

The full system works end-to-end, including the web app.

**Five directions for future work:**

1. **Sensor bias correction** — place a few sensors next to
   Kazhydromet reference stations, so we can give absolute
   concentrations, not just relative ones.
2. **Uncertainty forecasts** — give the user a range, not just one
   number. This directly addresses the peak problem.
3. **Other pollutants** — PM10, NO₂, O₃. Same pipeline, small
   changes.
4. **Other cities** — Shymkent, Karaganda. Similar geography.
5. **Publication** — target a Scopus Q2 journal.

### Bullets
- H1, H2, H3 — all confirmed.
- Full pipeline + web app delivered.
- Future: sensor calibration; uncertainty forecasts; more
  pollutants; more cities; Scopus Q2 publication.

---

## Slide 12 — Publications

### Full speech
I have one peer-reviewed paper with Professor Naizabayeva. It is
about a hybrid music recommendation system. The topic is different
from the thesis — but the **method** is the same: combine several
signals, compare against many baselines, and report more than one
type of metric. That is exactly how I built and evaluated the PM2.5
model.

A paper on the dissertation topic is in preparation.

### Bullets
- One prior paper with consultant: music recommendation system.
  Different topic, same research method.
- Dissertation-topic paper: in preparation.

---

## Slide 13 — Thank you

Thank you for your attention. I am ready for your questions.

---

## Q&A — likely questions and short answers

**Q: Why not use a deep neural network like LSTM?**
A: My data is small — under one million rows with engineered
features. Tabular methods like XGBoost work better at this size.
They are also faster and easier to deploy for free. Deep networks
need more data and more infrastructure.

**Q: Why not place sensors next to reference instruments?**
A: That needs physical access to reference equipment. It is outside
the scope of a 4-week project. I treat sensor readings as a
*relative* signal, and I say so in Chapter 4.

**Q: Why does the data window start in October 2024?**
A: Of the 192 sensors, only one had data for winter 2023-24. Most
sensors came online in 2025. So 562 continuous days is the longest
window possible.

**Q: How do you prevent data leakage?**
A: I use time-based validation only. The test period is always
after the training period. I never shuffle the data.
